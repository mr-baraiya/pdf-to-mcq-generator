# Ollama Auto-Install & Management

Auto-installation and management features for Ollama integration.

## Overview

The backend now automatically:
1. **Detects** if Ollama is installed
2. **Provides** installation instructions
3. **Auto-installs** Ollama on Linux systems
4. **Starts** Ollama service when needed

## New API Endpoints

### 1. GET `/ollama-status`
Check Ollama installation status and get OS-specific setup instructions.

**Response:**
```json
{
  "os": "linux",
  "installed": true,
  "running": false,
  "can_auto_install": true,
  "installation_instructions": {
    "description": "Install Ollama on Linux",
    "auto_install_available": true,
    "manual_command": "curl -fsSL https://ollama.com/install.sh | sh",
    "steps": [
      "Run: curl -fsSL https://ollama.com/install.sh | sh",
      "Start Ollama: ollama serve",
      "Pull a model: ollama pull llama3.2"
    ]
  },
  "model": "llama3.2",
  "host": "http://localhost:11434"
}
```

### 2. POST `/ollama-install`
Automatically install Ollama (Linux only).

**Usage:**
```bash
curl -X POST http://localhost:8000/ollama-install
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Ollama installed successfully! Please start it with: ollama serve"
}
```

**Response (Already Installed):**
```json
{
  "success": true,
  "message": "Ollama is already installed",
  "installed": true,
  "running": false
}
```

**Response (macOS/Windows):**
```json
{
  "success": false,
  "message": "Auto-install not available for macos",
  "installation_instructions": {
    "description": "Install Ollama on macOS",
    "manual_command": "Download from https://ollama.com/download",
    "steps": [...]
  }
}
```

**Important:**
- Takes 2-5 minutes to complete
- Only works on Linux
- Requires internet connection
- Requires system permissions

### 3. POST `/ollama-start`
Start Ollama service if it's installed but not running.

**Usage:**
```bash
curl -X POST http://localhost:8000/ollama-start
```

**Response:**
```json
{
  "success": true,
  "message": "Ollama service started"
}
```

## Startup Detection

The backend automatically checks Ollama status on startup:

```
INFO:     ✅ Vercel Blob is ready
INFO:     ⚠️  Ollama installed but not running. Start with: POST /ollama-start
INFO:     Application startup complete.
```

**Status Messages:**
- ✅ **Ollama is ready** - Installed and running
- ⚠️ **Ollama installed but not running** - Need to start service
- ⚠️ **Ollama not installed (Linux)** - Auto-install available
- ⚠️ **Ollama not installed (macOS/Windows)** - Manual install required

## Frontend Integration

### Check and Install Flow

```javascript
// 1. Check Ollama status on page load
async function checkOllama() {
  const status = await fetch('/ollama-status').then(r => r.json());
  
  if (!status.installed && status.can_auto_install) {
    // Show install button for Linux users
    return showOllamaInstallUI(status);
  }
  
  if (!status.installed && !status.can_auto_install) {
    // Show manual instructions for macOS/Windows
    return showManualInstructions(status.installation_instructions);
  }
  
  if (status.installed && !status.running) {
    // Show start button
    return showOllamaStartUI();
  }
  
  // Ollama ready!
  return enableOllamaFeatures();
}

// 2. Auto-install (Linux only)
async function installOllama() {
  showLoadingSpinner('Installing Ollama... (2-5 minutes)');
  
  const result = await fetch('/ollama-install', {
    method: 'POST'
  }).then(r => r.json());
  
  if (result.success) {
    showSuccess('Ollama installed! Starting service...');
    await startOllama();
  } else {
    showError(result.message);
    showManualInstructions(result.installation_instructions);
  }
}

// 3. Start Ollama service
async function startOllama() {
  const result = await fetch('/ollama-start', {
    method: 'POST'
  }).then(r => r.json());
  
  if (result.success) {
    showSuccess('Ollama is ready!');
    enableOllamaFeatures();
  } else {
    showError('Failed to start Ollama');
  }
}
```

### UI Recommendations

**For Linux Users:**
```
╔════════════════════════════════════════╗
║  Ollama Not Installed                  ║
║  Local AI generation requires Ollama   ║
║                                        ║
║  [ Auto-Install Ollama (2-5 min) ]    ║
║  [ Manual Instructions ]               ║
╚════════════════════════════════════════╝
```

**For macOS/Windows Users:**
```
╔════════════════════════════════════════╗
║  Ollama Not Installed                  ║
║  Download from ollama.com/download     ║
║                                        ║
║  [ Open Download Page ]                ║
║  [ View Instructions ]                 ║
╚════════════════════════════════════════╝
```

**When Installed but Not Running:**
```
╔════════════════════════════════════════╗
║  Ollama Not Running                    ║
║  Click to start the service            ║
║                                        ║
║  [ Start Ollama ]                      ║
╚════════════════════════════════════════╝
```

## Technical Details

### Installation Process

**Linux (Ubuntu/Debian):**
1. Downloads official install script from `https://ollama.com/install.sh`
2. Executes script with shell
3. Takes 2-5 minutes depending on connection
4. Installs to `/usr/local/bin/ollama`

**macOS:**
1. Shows link to download .dmg file
2. User installs manually
3. Ollama runs as background app

**Windows:**
1. Shows link to download installer
2. User installs manually
3. Ollama runs as service

### Service Management

**Starting Ollama:**
- Runs `ollama serve` in background
- Waits 3 seconds for service to initialize
- Verifies service is responding at `localhost:11434`

**Checking Status:**
- Verifies binary exists with `which ollama`
- Tests service with GET request to `/api/tags`
- Returns installation state and running state

## Limitations

1. **Auto-install only on Linux** - macOS/Windows require manual installation
2. **Requires internet** - Downloads from ollama.com
3. **Takes time** - Installation can take 2-5 minutes
4. **System permissions** - May require sudo on some systems
5. **Model download** - Users still need to `ollama pull llama3.2` after install

## Best Practices

### For Frontend Developers:

1. **Check status on page load** - Call `/ollama-status` first
2. **Show appropriate UI** - Different for Linux vs macOS/Windows
3. **Display progress** - Installation takes time, show spinner
4. **Provide alternatives** - Offer Groq/Gemini while Ollama installs
5. **Cache status** - Don't check every second, once per minute is enough

### For Users:

1. **Use auto-install on Linux** - Easiest way to get started
2. **Download manually on macOS/Windows** - Visit ollama.com
3. **Pull a model after install** - Run `ollama pull llama3.2`
4. **Keep Ollama running** - Service needs to stay active

## Example Workflow

```javascript
// Complete setup flow
async function setupOllama() {
  // 1. Check status
  const status = await fetch('/ollama-status').then(r => r.json());
  console.log('OS:', status.os);
  console.log('Installed:', status.installed);
  console.log('Running:', status.running);
  
  // 2. Install if needed (Linux only)
  if (!status.installed && status.can_auto_install) {
    console.log('Installing Ollama...');
    const install = await fetch('/ollama-install', {
      method: 'POST'
    }).then(r => r.json());
    
    if (!install.success) {
      console.error('Install failed:', install.message);
      return false;
    }
    console.log('✅ Installed!');
  }
  
  // 3. Start if not running
  if (status.installed && !status.running) {
    console.log('Starting Ollama...');
    const start = await fetch('/ollama-start', {
      method: 'POST'
    }).then(r => r.json());
    
    if (!start.success) {
      console.error('Start failed:', start.message);
      return false;
    }
    console.log('✅ Started!');
  }
  
  // 4. Verify it's ready
  const aiStatus = await fetch('/ai-status').then(r => r.json());
  if (aiStatus.ollama.available) {
    console.log('✅ Ollama is ready!');
    return true;
  }
  
  console.error('❌ Ollama not available');
  return false;
}
```

## Troubleshooting

**Installation fails:**
- Check internet connection
- Try manual installation: `curl -fsSL https://ollama.com/install.sh | sh`
- Check disk space (needs ~500MB)

**Service won't start:**
- Check if port 11434 is available
- Try manual start: `ollama serve`
- Check logs for errors

**Model not found:**
- Need to pull model: `ollama pull llama3.2`
- Check available models: `ollama list`

## Related Documentation

- [API_ENDPOINTS.md](./API_ENDPOINTS.md) - All API endpoints
- [OLLAMA_SETUP.md](./docs/OLLAMA_SETUP.md) - Manual Ollama setup
- [Official Ollama Docs](https://ollama.com/docs) - Complete Ollama guide

---

**Summary:** The backend now handles Ollama installation and management automatically, making it much easier for users to get started with local AI generation!
