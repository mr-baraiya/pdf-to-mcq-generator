"""Ollama installation and management utilities"""

import os
import sys
import subprocess
import logging
import platform

log = logging.getLogger(__name__)


def get_os_type():
    """Detect the operating system"""
    system = platform.system().lower()
    if system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return "unknown"


def is_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(
            ["which", "ollama"],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.returncode == 0
    except:
        return False


def is_ollama_running():
    """Check if Ollama service is running"""
    import requests
    ollama_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_installation_instructions():
    """Get OS-specific installation instructions"""
    os_type = get_os_type()
    
    instructions = {
        "linux": {
            "description": "Install Ollama on Linux",
            "auto_install_available": True,
            "manual_command": "curl -fsSL https://ollama.com/install.sh | sh",
            "steps": [
                "Run: curl -fsSL https://ollama.com/install.sh | sh",
                "Start Ollama: ollama serve",
                "Pull a model: ollama pull llama3.2"
            ]
        },
        "macos": {
            "description": "Install Ollama on macOS",
            "auto_install_available": False,
            "manual_command": "Download from https://ollama.com/download",
            "steps": [
                "Download Ollama from https://ollama.com/download",
                "Install the .dmg file",
                "Open Ollama app (runs in background)",
                "Pull a model: ollama pull llama3.2"
            ]
        },
        "windows": {
            "description": "Install Ollama on Windows",
            "auto_install_available": False,
            "manual_command": "Download from https://ollama.com/download",
            "steps": [
                "Download Ollama from https://ollama.com/download",
                "Run the installer",
                "Pull a model: ollama pull llama3.2"
            ]
        },
        "unknown": {
            "description": "Visit Ollama website",
            "auto_install_available": False,
            "manual_command": "Visit https://ollama.com/download",
            "steps": ["Visit https://ollama.com/download for your OS"]
        }
    }
    
    return instructions.get(os_type, instructions["unknown"])


def auto_install_ollama_linux():
    """Attempt to auto-install Ollama on Linux"""
    log.info("Attempting to auto-install Ollama on Linux...")
    
    try:
        # Download and run the installation script
        install_cmd = "curl -fsSL https://ollama.com/install.sh | sh"
        
        result = subprocess.run(
            install_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            log.info("✅ Ollama installed successfully!")
            return {
                "success": True,
                "message": "Ollama installed successfully! Please start it with: ollama serve"
            }
        else:
            log.error(f"Installation failed: {result.stderr}")
            return {
                "success": False,
                "message": f"Installation failed: {result.stderr}",
                "manual_steps": get_installation_instructions()
            }
            
    except subprocess.TimeoutExpired:
        log.error("Installation timeout")
        return {
            "success": False,
            "message": "Installation timed out. Please install manually.",
            "manual_steps": get_installation_instructions()
        }
    except Exception as e:
        log.error(f"Installation error: {str(e)}")
        return {
            "success": False,
            "message": f"Installation error: {str(e)}",
            "manual_steps": get_installation_instructions()
        }


def start_ollama_service():
    """Attempt to start Ollama service"""
    if is_ollama_running():
        return {"success": True, "message": "Ollama is already running"}
    
    try:
        log.info("Attempting to start Ollama service...")
        # Start ollama serve in background
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        
        import time
        time.sleep(3)  # Wait for service to start
        
        if is_ollama_running():
            log.info("✅ Ollama service started successfully!")
            return {"success": True, "message": "Ollama service started"}
        else:
            return {"success": False, "message": "Failed to start Ollama service"}
            
    except FileNotFoundError:
        return {
            "success": False,
            "message": "Ollama not found. Please install it first."
        }
    except Exception as e:
        log.error(f"Error starting Ollama: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


def get_ollama_status():
    """Get comprehensive Ollama status"""
    os_type = get_os_type()
    installed = is_ollama_installed()
    running = is_ollama_running()
    instructions = get_installation_instructions()
    
    return {
        "os": os_type,
        "installed": installed,
        "running": running,
        "can_auto_install": instructions["auto_install_available"],
        "installation_instructions": instructions,
        "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
        "host": os.getenv("OLLAMA_HOST", "http://localhost:11434")
    }
