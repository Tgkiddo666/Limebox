#!/usr/bin/env python3
"""
LimeBox Utilities
Helper functions for project detection, dependency installation, and running
"""

import os
import json
import subprocess
import threading
import time
import sys
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

console = Console()
LIME_GREEN = "#00FF00"

def clear_terminal():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

class ProjectDetector:
    """Detect project type and framework"""
    
    def __init__(self, project_path):
        self.path = Path(project_path)
        
    def detect_framework(self):
        """Auto-detect the project framework/language"""
        
        # Check for specific files that indicate framework
        detectors = [
            (self._is_nextjs, "Next.js"),
            (self._is_react, "React"),
            (self._is_vue, "Vue.js"),
            (self._is_angular, "Angular"),
            (self._is_svelte, "Svelte"),
            (self._is_nodejs, "Node.js"),
            (self._is_python_flask, "Flask"),
            (self._is_python_django, "Django"),
            (self._is_python_fastapi, "FastAPI"),
            (self._is_python, "Python"),
            (self._is_php, "PHP"),
            (self._is_static, "Static HTML"),
        ]
        
        for detector, framework in detectors:
            if detector():
                return framework
                
        return "Unknown"
    
    def _is_nextjs(self):
        package_json = self.path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    return 'next' in deps
            except:
                pass
        return False
        
    def _is_react(self):
        package_json = self.path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    return 'react' in deps and 'next' not in deps
            except:
                pass
        return False
        
    def _is_vue(self):
        package_json = self.path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    return 'vue' in deps
            except:
                pass
        return False
        
    def _is_angular(self):
        package_json = self.path / "package.json"
        angular_json = self.path / "angular.json"
        if package_json.exists() or angular_json.exists():
            try:
                if angular_json.exists():
                    return True
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    return '@angular/core' in deps
            except:
                pass
        return False
        
    def _is_svelte(self):
        package_json = self.path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    return 'svelte' in deps
            except:
                pass
        return False
        
    def _is_nodejs(self):
        files = ['package.json', 'server.js', 'app.js', 'index.js']
        return any((self.path / f).exists() for f in files)
        
    def _is_python_django(self):
        files = ['manage.py', 'django_project']
        requirements = self.path / "requirements.txt"
        if requirements.exists():
            try:
                with open(requirements) as f:
                    content = f.read().lower()
                    if 'django' in content:
                        return True
            except:
                pass
        return any((self.path / f).exists() for f in files)
        
    def _is_python_flask(self):
        files = ['app.py', 'main.py']
        requirements = self.path / "requirements.txt"
        if requirements.exists():
            try:
                with open(requirements) as f:
                    content = f.read().lower()
                    if 'flask' in content:
                        return True
            except:
                pass
        # Check for common Flask app patterns
        for file in files:
            filepath = self.path / file
            if filepath.exists():
                try:
                    with open(filepath) as f:
                        content = f.read()
                        if 'from flask import' in content or 'import flask' in content:
                            return True
                except:
                    pass
        return False
        
    def _is_python_fastapi(self):
        files = ['main.py', 'app.py']
        requirements = self.path / "requirements.txt"
        if requirements.exists():
            try:
                with open(requirements) as f:
                    content = f.read().lower()
                    if 'fastapi' in content:
                        return True
            except:
                pass
        # Check for FastAPI imports
        for file in files:
            filepath = self.path / file
            if filepath.exists():
                try:
                    with open(filepath) as f:
                        content = f.read()
                        if 'from fastapi import' in content or 'import fastapi' in content:
                            return True
                except:
                    pass
        return False
        
    def _is_python(self):
        files = ['main.py', 'app.py', 'requirements.txt', 'setup.py', 'pyproject.toml']
        return any((self.path / f).exists() for f in files)
        
    def _is_php(self):
        files = ['index.php', 'composer.json']
        return any((self.path / f).exists() for f in files)
        
    def _is_static(self):
        files = ['index.html', 'index.htm']
        return any((self.path / f).exists() for f in files)

class ProjectRunner:
    """Run projects with dependency management"""
    
    def __init__(self, project_path, project_type):
        self.path = Path(project_path)
        self.type = project_type
        self.process = None
        self.stop_event = threading.Event()
        
    def install_dependencies(self):
        """Install project dependencies based on type"""
        console.print(f"[lime]📦 Installing dependencies for {self.type}...[/lime]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            if self.type in ["Next.js", "React", "Vue.js", "Angular", "Svelte", "Node.js"]:
                task = progress.add_task("Installing npm packages...", total=None)
                self._run_command(["npm", "install"], "npm install")
                
            elif self.type in ["Flask", "Django", "FastAPI", "Python"]:
                task = progress.add_task("Installing pip packages...", total=None)
                if (self.path / "requirements.txt").exists():
                    self._run_command(["pip", "install", "-r", "requirements.txt"], "pip install")
                elif (self.path / "pyproject.toml").exists():
                    self._run_command(["pip", "install", "-e", "."], "pip install")
                    
            elif self.type == "PHP":
                if (self.path / "composer.json").exists():
                    task = progress.add_task("Installing composer packages...", total=None)
                    self._run_command(["composer", "install"], "composer install")
                    
        console.print("[lime]✅ Dependencies installed![/lime]")
        
    def _run_command(self, cmd, description):
        """Run a command safely"""
        try:
            result = subprocess.run(
                cmd, 
                cwd=self.path, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ {description} failed: {e.stderr}[/red]")
            raise
        except FileNotFoundError:
            console.print(f"[red]❌ Command not found: {cmd[0]}[/red]")
            console.print(f"[yellow]Please install {cmd[0]} first[/yellow]")
            raise
            
    def get_run_command(self, expose=False):
        """Get the command to run the project"""
        commands = {
            "Next.js": ["npm", "run", "dev"],
            "React": ["npm", "start"],
            "Vue.js": ["npm", "run", "serve"],
            "Angular": ["ng", "serve"],
            "Svelte": ["npm", "run", "dev"],
            "Node.js": ["npm", "start"],
            "Flask": ["python", "app.py"],
            "Django": ["python", "manage.py", "runserver"],
            "FastAPI": ["uvicorn", "main:app", "--reload"],
            "Python": ["python", "main.py"],
            "PHP": ["php", "-S", "localhost:8000"],
            "Static HTML": ["python", "-m", "http.server", "8000"]
        }
        
        return commands.get(self.type, ["echo", "Unknown project type"])
        
    def run(self, expose=False, project_name="Project"):
        """Run the project with live logging"""
        clear_terminal()
        
        # Install dependencies first
        try:
            self.install_dependencies()
        except Exception:
            console.print("[red]❌ Dependency installation failed![/red]")
            return
            
        # Get run command
        cmd = self.get_run_command(expose)
        
        console.print(Panel(
            f"[lime]🚀 Starting {project_name} ({self.type})[/lime]\n"
            f"[dim]Command: {' '.join(cmd)}[/dim]\n"
            f"[dim]Path: {self.path}[/dim]\n"
            f"[yellow]Press Ctrl+C to stop[/yellow]",
            title="[bold lime]Running Project[/bold lime]",
            border_style="lime"
        ))
        
        # Start the project
        try:
            self.process = subprocess.Popen(
                cmd,
                cwd=self.path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Display logs with lime highlighting
            console.print("\n[bold lime]📋 Live Logs:[/bold lime]")
            console.print("-" * 60)
            
            for line in iter(self.process.stdout.readline, ''):
                if not line:
                    break
                    
                # Highlight important info in lime
                if any(keyword in line.lower() for keyword in ['error', 'failed', 'exception']):
                    console.print(f"[red]{line.rstrip()}[/red]")
                elif any(keyword in line.lower() for keyword in ['server', 'listening', 'ready', 'compiled', 'running']):
                    console.print(f"[lime]{line.rstrip()}[/lime]")
                elif any(keyword in line.lower() for keyword in ['warning', 'warn']):
                    console.print(f"[yellow]{line.rstrip()}[/yellow]")
                else:
                    console.print(f"[white]{line.rstrip()}[/white]")
                    
        except KeyboardInterrupt:
            console.print(f"\n[lime]🛑 Stopping {project_name}...[/lime]")
            if self.process:
                self.process.terminate()
                self.process.wait()
        except Exception as e:
            console.print(f"[red]❌ Error running project: {e}[/red]")
        finally:
            if self.process:
                self.process.terminate()
                
        console.print(f"[lime]✅ {project_name} stopped.[/lime]")

def get_system_info():
    """Get system information for setup"""
    info = {
        'os': os.name,
        'platform': sys.platform,
        'python_version': sys.version,
        'cwd': os.getcwd()
    }
    return info

def check_dependencies():
    """Check if required system dependencies are available"""
    deps = {
        'git': 'git --version',
        'node': 'node --version',
        'npm': 'npm --version',
        'python': 'python --version',
        'pip': 'pip --version'
    }
    
    available = {}
    for name, cmd in deps.items():
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            available[name] = result.returncode == 0
        except FileNotFoundError:
            available[name] = False
            
    return available