# 🤖 Autonomous Agent System — VSCode & Cursor Extension

Connects **VSCode** and **Cursor IDE** directly to your local **Autonomous Agent System REST API Gateway** (`http://127.0.0.1:8000`).

---

## ✨ Features

- **⚡ Run Agent Task on Selected Code (`Cmd+Alt+A` / `Ctrl+Alt+A`)**: Highlight any block of C/C++, Python, or KiCad code and run sub-agent refactoring, hardware pinout checks, or code reviews instantly inside VSCode.
- **🗳️ Multi-Model Consensus Voting (`Agent System: Multi-Model Consensus Voting`)**: Query OpenAI, Claude, and Gemini models simultaneously on critical architecture decisions.
- **📌 Audit Hardware Pinouts (`Agent System: Audit Pinout Conflicts`)**: Interactively check GPIO collisions and ESP32/STM32 strapping hazards.
- **📊 Real-time Token & Cost Status Bar**: Shows token usage and cost estimations right in the VSCode status bar (`🤖 Agent System: Active`).

---

## 🚀 Quickstart & Installation Guide

### 1. Compile Extension
```bash
cd vscode_extension
npm install
npm run compile
```

### 2. Run / Debug in VSCode
- Open the `vscode_extension` folder in VSCode.
- Press **F5** (or click `Run Extension` from the Debug panel).
- A new VSCode window (Extension Development Host) will open with the Agent System extension active!

### 3. Package to `.vsix`
```bash
npx vsce package
```
Then install in VSCode via `Extensions -> Install from VSIX...`.
