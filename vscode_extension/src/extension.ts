import * as vscode from 'vscode';
import * as http from 'http';

export function activate(context: vscode.ExtensionContext) {
    console.log('🤖 Agent System VSCode Extension is now active!');

    // Register Webview Sidebar View Provider
    const provider = new AgentSidebarWebviewProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(AgentSidebarWebviewProvider.viewType, provider)
    );

    // Status Bar Item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = '$(robot) Agent System: Active';
    statusBarItem.tooltip = 'Click to show Agent System Token Stats';
    statusBarItem.command = 'agentSystem.showStats';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Command 1: Run Task on Selected Code
    let disposableRunTask = vscode.commands.registerCommand('agentSystem.runTask', async () => {
        const editor = vscode.window.activeTextEditor;
        const selectedText = editor ? (editor.document.getText(editor.selection) || editor.document.getText()) : '';

        const promptInput = await vscode.window.showInputBox({
            prompt: 'Enter instructions for the Agent System',
            placeHolder: 'e.g. Refactor this function or audit hardware pinouts'
        });

        if (!promptInput) { return; }

        runTaskApi(promptInput, selectedText);
    });

    // Command 2: Multi-Model Consensus Voting
    let disposableConsensus = vscode.commands.registerCommand('agentSystem.runConsensus', async () => {
        const promptInput = await vscode.window.showInputBox({
            prompt: 'Enter hardware/software decision prompt for Consensus Voting',
            placeHolder: 'e.g. Should I use ESP32-S3 or STM32F4 for low-power IoT?'
        });

        if (!promptInput) { return; }

        runConsensusApi(promptInput);
    });

    // Command 3: Audit Pinout Conflicts
    let disposablePinout = vscode.commands.registerCommand('agentSystem.checkPinout', async () => {
        const sda = await vscode.window.showInputBox({ prompt: 'Enter I2C SDA Pin', value: 'GPIO21' });
        const scl = await vscode.window.showInputBox({ prompt: 'Enter I2C SCL Pin', value: 'GPIO22' });
        const outPin = await vscode.window.showInputBox({ prompt: 'Enter Output Pin', value: 'GPIO34' });

        if (!sda || !scl || !outPin) { return; }

        const config = vscode.workspace.getConfiguration('agentSystem');
        const apiUrl = config.get<string>('apiUrl') || 'http://127.0.0.1:8000';

        try {
            const result = await getJson(`${apiUrl}/api/v1/pinout?sda=${sda}&scl=${scl}&output_pin=${outPin}`);
            if (result.conflicts && result.conflicts.length > 0) {
                vscode.window.showErrorMessage(`🔴 Pin Conflict: ${result.conflicts.join(' | ')}`);
            } else {
                vscode.window.showInformationMessage('✅ Clean Pinout Assignment! No hardware collisions detected.');
            }
        } catch (err: any) {
            vscode.window.showErrorMessage(`Pinout check failed: ${err.message}`);
        }
    });

    // Command 4: Show Live Stats
    let disposableStats = vscode.commands.registerCommand('agentSystem.showStats', async () => {
        const config = vscode.workspace.getConfiguration('agentSystem');
        const apiUrl = config.get<string>('apiUrl') || 'http://127.0.0.1:8000';

        try {
            const stats = await getJson(`${apiUrl}/api/stats`);
            vscode.window.showInformationMessage(
                `📊 Agent System: Total Calls: ${stats.total_calls} | Total Tokens: ${stats.total_tokens} | Cost: $${stats.total_cost_usd}`
            );
        } catch (err: any) {
            vscode.window.showErrorMessage(`Failed to fetch stats: ${err.message}`);
        }
    });

    context.subscriptions.push(disposableRunTask, disposableConsensus, disposablePinout, disposableStats);
}

export function deactivate() {}

// ------------------------------------------------------------------
// Webview Sidebar Provider Implementation
// ------------------------------------------------------------------

class AgentSidebarWebviewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'agentSystemSidebarView';

    constructor(private readonly _extensionUri: vscode.Uri) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        webviewView.webview.onDidReceiveMessage(async data => {
            switch (data.type) {
                case 'runTask':
                    runTaskApi(data.prompt, '');
                    break;
                case 'runConsensus':
                    runConsensusApi(data.prompt);
                    break;
            }
        });
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent System Dashboard</title>
    <style>
        body { font-family: var(--vscode-font-family); padding: 10px; color: var(--vscode-foreground); }
        .card { background: var(--vscode-sideBar-background); border: 1px solid var(--vscode-panel-border); padding: 12px; margin-bottom: 12px; border-radius: 6px; }
        h3 { margin-top: 0; color: var(--vscode-symbolIcon-keywordForeground); }
        button { background: var(--vscode-button-background); color: var(--vscode-button-foreground); border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; width: 100%; margin-top: 6px; font-weight: bold; }
        button:hover { background: var(--vscode-button-hoverBackground); }
        textarea { width: 100%; height: 60px; background: var(--vscode-input-background); color: var(--vscode-input-foreground); border: 1px solid var(--vscode-input-border); border-radius: 4px; padding: 6px; box-sizing: border-box; }
        .badge { display: inline-block; padding: 2px 6px; background: var(--vscode-badge-background); color: var(--vscode-badge-foreground); border-radius: 4px; font-size: 11px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h3>🤖 Autonomous Agent OS</h3>
        <p>Active Agent: <span class="badge">ORCHESTRATOR</span></p>
        <p>Model: <span class="badge">OpenAI gpt-4o</span></p>
        <p>Backend: <span class="badge" style="background: green; color: white;">Port 8000 (Active)</span></p>
    </div>

    <div class="card">
        <h3>⚡ Quick Prompt Execution</h3>
        <textarea id="promptInput" placeholder="Enter instructions for Agent System..."></textarea>
        <button onclick="runTask()">🚀 Run Task</button>
    </div>

    <div class="card">
        <h3>🗳️ Consensus Voting</h3>
        <button onclick="runConsensus()">Run Multi-Model Consensus</button>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        function runTask() {
            const prompt = document.getElementById('promptInput').value;
            if (prompt) {
                vscode.postMessage({ type: 'runTask', prompt: prompt });
            }
        }
        function runConsensus() {
            const prompt = document.getElementById('promptInput').value || 'Compare ESP32 vs STM32';
            vscode.postMessage({ type: 'runConsensus', prompt: prompt });
        }
    </script>
</body>
</html>`;
    }
}

// ------------------------------------------------------------------
// API Helper Functions
// ------------------------------------------------------------------

async function runTaskApi(promptInput: string, codeContext: string) {
    const config = vscode.workspace.getConfiguration('agentSystem');
    const apiUrl = config.get<string>('apiUrl') || 'http://127.0.0.1:8000';
    const agentName = config.get<string>('defaultAgent') || 'orchestrator';
    const modelName = config.get<string>('defaultModel') || 'gpt-4o';

    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `🤖 Agent System [${agentName.toUpperCase()}] processing task...`,
        cancellable: false
    }, async () => {
        try {
            const fullPrompt = codeContext ? `${promptInput}\n\nCODE CONTEXT:\n\`\`\`\n${codeContext}\n\`\`\`` : promptInput;
            const result = await postJson(`${apiUrl}/api/v1/agent/run`, {
                prompt: fullPrompt,
                agent_name: agentName,
                model_name: modelName
            });

            const outputChannel = vscode.window.createOutputChannel('Agent System Output');
            outputChannel.appendLine(`=== AGENT RESPONSE [${agentName.toUpperCase()}] ===`);
            outputChannel.appendLine(result.output);
            outputChannel.show();

            vscode.window.showInformationMessage('✅ Agent task completed successfully!');
        } catch (err: any) {
            vscode.window.showErrorMessage(`Failed to run agent task: ${err.message}`);
        }
    });
}

async function runConsensusApi(promptInput: string) {
    const config = vscode.workspace.getConfiguration('agentSystem');
    const apiUrl = config.get<string>('apiUrl') || 'http://127.0.0.1:8000';

    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: '🗳️ Running Multi-Model Consensus Voting...',
        cancellable: false
    }, async () => {
        try {
            const result = await postJson(`${apiUrl}/api/v1/consensus`, { prompt: promptInput });
            const outputChannel = vscode.window.createOutputChannel('Agent System Consensus');
            outputChannel.appendLine(result.consensus_synthesis);
            outputChannel.show();
        } catch (err: any) {
            vscode.window.showErrorMessage(`Consensus voting failed: ${err.message}`);
        }
    });
}

function postJson(urlStr: string, bodyObj: any): Promise<any> {
    return new Promise((resolve, reject) => {
        const u = new URL(urlStr);
        const data = JSON.stringify(bodyObj);
        const req = http.request({
            hostname: u.hostname,
            port: u.port,
            path: u.pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(data)
            }
        }, (res) => {
            let buf = '';
            res.on('data', chunk => buf += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(buf)); } catch (e) { resolve(buf); }
            });
        });
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}

function getJson(urlStr: string): Promise<any> {
    return new Promise((resolve, reject) => {
        http.get(urlStr, (res) => {
            let buf = '';
            res.on('data', chunk => buf += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(buf)); } catch (e) { resolve(buf); }
            });
        }).on('error', reject);
    });
}
