"""
Multi-Agent DAG Pipeline — Directed Acyclic Graph Task Orchestration.
Allows defining agent workflows where outputs from one agent 
feed into the next, with parallel execution support.
"""

import time
from typing import Dict, Any, List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.runner import run_agent_task

class PipelineNode:
    """A single node in the agent pipeline DAG."""
    def __init__(self, name: str, agent_name: str, model_name: str = "gpt-4o",
                 prompt_template: str = "{input}", depends_on: Optional[List[str]] = None):
        self.name = name
        self.agent_name = agent_name
        self.model_name = model_name
        self.prompt_template = prompt_template
        self.depends_on = depends_on or []
        self.result: Optional[str] = None
        self.elapsed_ms: float = 0.0
        self.status: str = "pending"

class AgentPipeline:
    """
    DAG-based multi-agent orchestration pipeline.
    
    Example:
        pipeline = AgentPipeline()
        pipeline.add_node("plan", "planner", prompt_template="Plan: {input}")
        pipeline.add_node("code", "software", depends_on=["plan"], 
                          prompt_template="Implement: {plan}")
        pipeline.add_node("review", "reviewer", depends_on=["code"],
                          prompt_template="Review: {code}")
        results = pipeline.execute("Build an I2C driver for STM32")
    """

    def __init__(self):
        self.nodes: Dict[str, PipelineNode] = {}

    def add_node(self, name: str, agent_name: str, model_name: str = "gpt-4o",
                 prompt_template: str = "{input}", depends_on: Optional[List[str]] = None):
        """Adds a node to the pipeline DAG."""
        self.nodes[name] = PipelineNode(
            name=name, agent_name=agent_name, model_name=model_name,
            prompt_template=prompt_template, depends_on=depends_on
        )

    def _get_execution_order(self) -> List[List[str]]:
        """Topological sort into parallel execution layers."""
        layers = []
        completed = set()

        while len(completed) < len(self.nodes):
            layer = []
            for name, node in self.nodes.items():
                if name not in completed:
                    if all(dep in completed for dep in node.depends_on):
                        layer.append(name)
            if not layer:
                raise ValueError("Circular dependency detected in pipeline DAG!")
            layers.append(layer)
            completed.update(layer)

        return layers

    def _execute_node(self, node: PipelineNode, context: Dict[str, str]) -> PipelineNode:
        """Executes a single pipeline node."""
        # Build prompt from template using context from dependencies
        prompt = node.prompt_template
        for key, value in context.items():
            prompt = prompt.replace(f"{{{key}}}", value)

        start = time.time()
        try:
            node.result = run_agent_task(
                agent_name=node.agent_name,
                user_prompt=prompt,
                model_name=node.model_name,
                use_rag=False
            )
            node.status = "success"
        except Exception as e:
            node.result = f"Pipeline Error: {str(e)}"
            node.status = "error"

        node.elapsed_ms = round((time.time() - start) * 1000, 1)
        return node

    def execute(self, initial_input: str) -> Dict[str, Any]:
        """
        Executes the full pipeline DAG.
        Nodes in the same layer run in parallel (ThreadPoolExecutor).
        """
        layers = self._get_execution_order()
        context = {"input": initial_input}
        total_start = time.time()
        results = {}

        for layer in layers:
            if len(layer) == 1:
                # Single node — run directly
                node = self.nodes[layer[0]]
                self._execute_node(node, context)
                context[node.name] = node.result or ""
                results[node.name] = {
                    "agent": node.agent_name,
                    "status": node.status,
                    "elapsed_ms": node.elapsed_ms,
                    "output": (node.result or "")[:500]
                }
            else:
                # Multiple nodes — run in parallel
                with ThreadPoolExecutor(max_workers=len(layer)) as executor:
                    futures = {
                        executor.submit(self._execute_node, self.nodes[name], context.copy()): name
                        for name in layer
                    }
                    for future in as_completed(futures):
                        name = futures[future]
                        node = future.result()
                        context[node.name] = node.result or ""
                        results[node.name] = {
                            "agent": node.agent_name,
                            "status": node.status,
                            "elapsed_ms": node.elapsed_ms,
                            "output": (node.result or "")[:500]
                        }

        total_elapsed = round((time.time() - total_start) * 1000, 1)

        return {
            "status": "completed",
            "total_elapsed_ms": total_elapsed,
            "layers_executed": len(layers),
            "node_results": results
        }

# ------------------------------------------------------------------
# Preset Pipelines
# ------------------------------------------------------------------

def embedded_dev_pipeline() -> AgentPipeline:
    """Pre-built pipeline for embedded systems development tasks."""
    pipeline = AgentPipeline()
    pipeline.add_node("plan", "planner", model_name="gpt-4o-mini",
                      prompt_template="Create a step-by-step plan for: {input}")
    pipeline.add_node("hardware", "electronics", model_name="gpt-4o",
                      prompt_template="Based on this plan, specify hardware requirements and pinout:\n{plan}")
    pipeline.add_node("software", "software", model_name="gpt-4o",
                      prompt_template="Based on this plan, write the firmware code:\n{plan}")
    pipeline.add_node("review", "reviewer", model_name="gpt-4o-mini",
                      depends_on=["hardware", "software"],
                      prompt_template="Review the following hardware spec and code for consistency:\n\nHardware:\n{hardware}\n\nSoftware:\n{software}")
    return pipeline
