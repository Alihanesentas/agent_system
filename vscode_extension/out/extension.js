"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const http = require("http");
function activate(context) {
    console.log('🤖 Agent System VSCode Extension is now active!');
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
        if (!editor) {
            vscode.window.showErrorMessage('No active code editor found.');
            return;
        }
        const selection = editor.selection;
        const selectedText = editor.document.getText(selection) || editor.document.getText();
        const promptInput = await vscode.window.showInputBox({
            prompt: 'Enter instructions for the Agent System',
            placeHolder: 'e.g. Refactor this function or audit hardware pinouts'
        });
        if (!promptInput) {
            return;
        }
        const config = vscode.workspace.getConfiguration('agentSystem');
        const apiUrl = config.get('apiUrl') || 'http://127.0.0.1:8000';
        const agentName = config.get('defaultAgent') || 'orchestrator';
        const modelName = config.get('defaultModel') || 'gpt-4o';
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `🤖 Agent System [${agentName.toUpperCase()}] processing code...`,
            cancellable: false
        }, async () => {
            try {
                const fullPrompt = `${promptInput}\n\nCODE CONTEXT:\n\`\`\`\n${selectedText}\n\`\`\``;
                const result = await postJson(`${apiUrl}/api/v1/agent/run`, {
                    prompt: fullPrompt,
                    agent_name: agentName,
                    model_name: modelName
                });
                const outputChannel = vscode.window.createOutputChannel('Agent System');
                outputChannel.appendLine(`=== AGENT RESPONSE [${agentName.toUpperCase()}] ===`);
                outputChannel.appendLine(result.output);
                outputChannel.show();
                vscode.window.showInformationMessage('✅ Agent task completed successfully!');
            }
            catch (err) {
                vscode.window.showErrorMessage(`Failed to run agent task: ${err.message}`);
            }
        });
    });
    // Command 2: Multi-Model Consensus Voting
    let disposableConsensus = vscode.commands.registerCommand('agentSystem.runConsensus', async () => {
        const promptInput = await vscode.window.showInputBox({
            prompt: 'Enter hardware/software decision prompt for Consensus Voting',
            placeHolder: 'e.g. Should I use ESP32-S3 or STM32F4 for low-power IoT?'
        });
        if (!promptInput) {
            return;
        }
        const config = vscode.workspace.getConfiguration('agentSystem');
        const apiUrl = config.get('apiUrl') || 'http://127.0.0.1:8000';
        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: '🗳️ Running Multi-Model Consensus Voting (OpenAI + Claude + Gemini)...',
            cancellable: false
        }, async () => {
            try {
                const result = await postJson(`${apiUrl}/api/v1/consensus`, { prompt: promptInput });
                const outputChannel = vscode.window.createOutputChannel('Agent System Consensus');
                outputChannel.appendLine(result.consensus_synthesis);
                outputChannel.show();
            }
            catch (err) {
                vscode.window.showErrorMessage(`Consensus voting failed: ${err.message}`);
            }
        });
    });
    // Command 3: Audit Pinout Conflicts
    let disposablePinout = vscode.commands.registerCommand('agentSystem.checkPinout', async () => {
        const sda = await vscode.window.showInputBox({ prompt: 'Enter I2C SDA Pin', value: 'GPIO21' });
        const scl = await vscode.window.showInputBox({ prompt: 'Enter I2C SCL Pin', value: 'GPIO22' });
        const outPin = await vscode.window.showInputBox({ prompt: 'Enter Output Pin', value: 'GPIO34' });
        if (!sda || !scl || !outPin) {
            return;
        }
        const config = vscode.workspace.getConfiguration('agentSystem');
        const apiUrl = config.get('apiUrl') || 'http://127.0.0.1:8000';
        try {
            const result = await getJson(`${apiUrl}/api/v1/pinout?sda=${sda}&scl=${scl}&output_pin=${outPin}`);
            if (result.conflicts && result.conflicts.length > 0) {
                vscode.window.showErrorMessage(`🔴 Pin Conflict Detected: ${result.conflicts.join(' | ')}`);
            }
            else {
                vscode.window.showInformationMessage('✅ Clean Pinout Assignment! No hardware collisions detected.');
            }
        }
        catch (err) {
            vscode.window.showErrorMessage(`Pinout check failed: ${err.message}`);
        }
    });
    // Command 4: Show Live Stats
    let disposableStats = vscode.commands.registerCommand('agentSystem.showStats', async () => {
        const config = vscode.workspace.getConfiguration('agentSystem');
        const apiUrl = config.get('apiUrl') || 'http://127.0.0.1:8000';
        try {
            const stats = await getJson(`${apiUrl}/api/stats`);
            vscode.window.showInformationMessage(`📊 Agent System: Total Calls: ${stats.total_calls} | Total Tokens: ${stats.total_tokens} | Cost: $${stats.total_cost_usd}`);
        }
        catch (err) {
            vscode.window.showErrorMessage(`Failed to fetch stats: ${err.message}`);
        }
    });
    context.subscriptions.push(disposableRunTask, disposableConsensus, disposablePinout, disposableStats);
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
// Helper HTTP POST JSON
function postJson(urlStr, bodyObj) {
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
                try {
                    resolve(JSON.parse(buf));
                }
                catch (e) {
                    resolve(buf);
                }
            });
        });
        req.on('error', reject);
        req.write(data);
        req.end();
    });
}
// Helper HTTP GET JSON
function getJson(urlStr) {
    return new Promise((resolve, reject) => {
        http.get(urlStr, (res) => {
            let buf = '';
            res.on('data', chunk => buf += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(buf));
                }
                catch (e) {
                    resolve(buf);
                }
            });
        }).on('error', reject);
    });
}
//# sourceMappingURL=extension.js.map