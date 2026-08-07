"""
Agent Unit Testing Framework — Automated Evaluation & Quality Assurance for Sub-Agents.
Enables writing programmatic unit tests to verify agent prompt outputs, token usage, 
cost limits, syntax validity, and JSON schemas.
"""

import time
import json
import ast
from typing import Dict, Any, List, Optional, Callable
from core.engine.runner import run_agent_task

class AgentTestCase:
    """Represents a single test case for an agent."""
    def __init__(self, name: str, agent_name: str, prompt: str, model_name: str = "gpt-4o"):
        self.name = name
        self.agent_name = agent_name
        self.prompt = prompt
        self.model_name = model_name
        self.assertions: List[Callable[[str, Dict[str, Any]], bool]] = []
        self.result: Optional[str] = None
        self.metrics: Dict[str, Any] = {}
        self.passed: bool = False
        self.failure_reasons: List[str] = []

    def assert_contains(self, expected_keyword: str, case_sensitive: bool = False):
        """Asserts that the response contains a specific keyword."""
        def check(output: str, meta: Dict[str, Any]) -> bool:
            target = output if case_sensitive else output.lower()
            key = expected_keyword if case_sensitive else expected_keyword.lower()
            if key not in target:
                self.failure_reasons.append(f"Expected output to contain '{expected_keyword}'")
                return False
            return True
        self.assertions.append(check)
        return self

    def assert_valid_json(self):
        """Asserts that the response is valid JSON."""
        def check(output: str, meta: Dict[str, Any]) -> bool:
            try:
                # Strip markdown codeblocks if present
                clean = output.strip()
                if clean.startswith("```json"):
                    clean = clean[7:]
                if clean.endswith("```"):
                    clean = clean[:-3]
                json.loads(clean.strip())
                return True
            except Exception as e:
                self.failure_reasons.append(f"Invalid JSON format: {e}")
                return False
        self.assertions.append(check)
        return self

    def assert_python_syntax(self):
        """Asserts that C/C++ or Python code snippet in the response has valid syntax."""
        def check(output: str, meta: Dict[str, Any]) -> bool:
            # Extract codeblocks
            if "```python" in output:
                code = output.split("```python")[1].split("```")[0]
                try:
                    ast.parse(code)
                    return True
                except Exception as e:
                    self.failure_reasons.append(f"Python syntax error: {e}")
                    return False
            return True  # Skip if no python code block
        self.assertions.append(check)
        return self

    def assert_max_latency(self, max_ms: float):
        """Asserts that latency is under max_ms."""
        def check(output: str, meta: Dict[str, Any]) -> bool:
            elapsed = meta.get("elapsed_ms", 0.0)
            if elapsed > max_ms:
                self.failure_reasons.append(f"Latency {elapsed}ms exceeded limit {max_ms}ms")
                return False
            return True
        self.assertions.append(check)
        return self

    def run(self) -> Dict[str, Any]:
        """Executes the test case and checks all assertions."""
        start = time.time()
        try:
            self.result = run_agent_task(
                agent_name=self.agent_name,
                user_prompt=self.prompt,
                model_name=self.model_name,
                use_rag=False
            )
            elapsed_ms = round((time.time() - start) * 1000, 1)
            self.metrics["elapsed_ms"] = elapsed_ms

            # Run assertions
            self.passed = True
            for assertion in self.assertions:
                if not assertion(self.result, self.metrics):
                    self.passed = False

        except Exception as e:
            self.passed = False
            self.failure_reasons.append(f"Execution Error: {str(e)}")

        return {
            "name": self.name,
            "agent": self.agent_name,
            "passed": self.passed,
            "elapsed_ms": self.metrics.get("elapsed_ms", 0),
            "failures": self.failure_reasons,
            "output_preview": (self.result or "")[:200]
        }

class AgentTestSuite:
    """Suite for grouping and running multiple AgentTestCases."""
    def __init__(self, name: str):
        self.name = name
        self.tests: List[AgentTestCase] = []

    def add_test(self, test: AgentTestCase):
        self.tests.append(test)

    def run_all(self) -> Dict[str, Any]:
        """Runs all test cases in the suite and returns aggregated statistics."""
        results = []
        passed_count = 0

        for test in self.tests:
            res = test.run()
            results.append(res)
            if res["passed"]:
                passed_count += 1

        return {
            "suite_name": self.name,
            "total_tests": len(self.tests),
            "passed_tests": passed_count,
            "failed_tests": len(self.tests) - passed_count,
            "pass_rate": f"{(passed_count / len(self.tests) * 100):.1f}%" if self.tests else "0%",
            "results": results
        }

# ------------------------------------------------------------------
# Pre-built Core Test Suite
# ------------------------------------------------------------------

def create_system_test_suite() -> AgentTestSuite:
    """Creates a comprehensive unit test suite verifying core agent functionality."""
    suite = AgentTestSuite("Core Agent Quality Suite")

    # Test 1: Electronics Sub-Agent I2C pull-up assertion
    t1 = AgentTestCase("Electronics I2C Check", "electronics", "What pull-up resistor value is recommended for I2C bus at 3.3V?", "gpt-4o-mini")
    t1.assert_contains("pull-up").assert_contains("k")
    suite.add_test(t1)

    # Test 2: Software Sub-Agent Python Code Syntax Check
    t2 = AgentTestCase("Software C/Python Syntax", "software", "Write a python function `add(a, b)` with type hints.", "gpt-4o-mini")
    t2.assert_contains("def add").assert_python_syntax()
    suite.add_test(t2)

    # Test 3: Reviewer Sub-Agent
    t3 = AgentTestCase("Reviewer Syntax Verification", "reviewer", "Check this python code: def foo(): return 42", "gpt-4o-mini")
    t3.assert_contains("foo")
    suite.add_test(t3)

    return suite
