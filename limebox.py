#!/usr/bin/env python3
"""
LimeBox - Terminal-based Project Runner
A sleek terminal app for running projects locally or exposing them online
"""

import os
import sys
import json
import subprocess
import threading
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
import argparse
from utils import ProjectDetector, ProjectRunner, clear_terminal

# Initialize console with lime theme
console = Console()
LIME_GREEN = "#00FF00"
DARK_LIME = "#32CD32"

class LimeBox:
    def __init__(self):
        self.config_file = "config.json"
        self.projects = {}
        self.load_config()

    def load_config(self):
        """Load configuration from config.json"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.projects = data.get('projects', {})
            else:
                self.save_config()
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")

    def save_config(self):
        """Save configuration to config.json"""
        try:
            data = {
                'projects': self.projects,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            console.print(f"[red]Error saving config: {e}[/red]")

    def show_banner(self):
        """Display the LimeBox ASCII banner"""
        clear_terminal()

        banner = """
██╗     ██╗███╗   ███╗███████╗██████╗  ██████╗ ██╗  ██╗
██║     ██║████╗ ████║██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝
██║     ██║██╔████╔██║█████╗  ██████╔╝██║   ██║ ╚███╔╝ 
██║     ██║██║╚██╔╝██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ 
███████╗██║██║ ╚═╝ ██║███████╗██████╔╝╚██████╔╝██╔╝ ██╗
╚══════╝╚═╝╚═╝     ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
        """

        console.print(Panel(
            Text(banner, style=f"bold {LIME_GREEN}"),
            title=f"[bold {LIME_GREEN}]Terminal Project Runner[/bold {LIME_GREEN}]",
            subtitle="[dim]v1.0.0 - Run any project, anywhere[/dim]",
            border_style=LIME_GREEN,
            padding=(1, 2)
        ))

    def show_menu(self):
        """Display the main menu"""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Option", style=f"bold {LIME_GREEN}", width=4)
        table.add_column("Description", style="white")

        options = [
            ("1", "📁 Add Local Project"),
            ("2", "🌐 Clone from GitHub"),
            ("3", "🚀 Run Project"),
            ("4", "📋 List Projects"),
            ("5", "🗑️  Remove Project"),
            ("6", "⚙️  Settings"),
            ("0", "🚪 Exit")
        ]

        for option, desc in options:
            table.add_row(option, desc)

        console.print("\n")
        console.print(Panel(
            table,
            title=f"[bold {LIME_GREEN}]Main Menu[/bold {LIME_GREEN}]",
            border_style=LIME_GREEN
        ))

    def add_local_project(self):
        """Add a local project to LimeBox"""
        console.print(f"\n[bold {LIME_GREEN}]Add Local Project[/bold {LIME_GREEN}]")

        path = Prompt.ask("Enter project path", default=".")
        path = os.path.abspath(path)

        if not os.path.exists(path):
            console.print("[red]❌ Path does not exist![/red]")
            return

        name = Prompt.ask("Project name", default=os.path.basename(path))

        # Detect project type
        detector = ProjectDetector(path)
        project_type = detector.detect_framework()

        console.print(f"[{LIME_GREEN}]✓ Detected: {project_type}[/{LIME_GREEN}]")

        self.projects[name] = {
            'path': path,
            'type': project_type,
            'source': 'local',
            'added': datetime.now().isoformat()
        }

        self.save_config()
        console.print(f"[{LIME_GREEN}]✅ Added project '{name}' successfully![/{LIME_GREEN}]")
        input("\nPress Enter to continue...")

    def clone_github_project(self):
        """Clone a project from GitHub"""
        console.print(f"\n[bold {LIME_GREEN}]Clone from GitHub[/bold {LIME_GREEN}]")

        repo_url = Prompt.ask("GitHub repository URL")
        if not repo_url:
            return

        # Extract repo name
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        name = Prompt.ask("Project name", default=repo_name)

        clone_path = os.path.join(os.getcwd(), name)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Cloning repository...", total=None)

            try:
                result = subprocess.run(
                    ['git', 'clone', repo_url, clone_path],
                    capture_output=True,
                    text=True,
                    check=True
                )

                # Detect project type
                detector = ProjectDetector(clone_path)
                project_type = detector.detect_framework()

                self.projects[name] = {
                    'path': clone_path,
                    'type': project_type,
                    'source': 'github',
                    'repo_url': repo_url,
                    'added': datetime.now().isoformat()
                }

                self.save_config()
                console.print(f"[{LIME_GREEN}]✅ Cloned and added '{name}' ({project_type})[/{LIME_GREEN}]")

            except subprocess.CalledProcessError as e:
                console.print(f"[red]❌ Failed to clone: {e.stderr}[/red]")
            except FileNotFoundError:
                console.print("[red]❌ Git not found! Please install git first.[/red]")

        input("\nPress Enter to continue...")

    def list_projects(self):
        """Display all projects"""
        console.print(f"\n[bold {LIME_GREEN}]Your Projects[/bold {LIME_GREEN}]")

        if not self.projects:
            console.print("[yellow]No projects added yet.[/yellow]")
            input("\nPress Enter to continue...")
            return

        table = Table(show_header=True, header_style=f"bold {LIME_GREEN}")
        table.add_column("Name", style="white", width=20)
        table.add_column("Type", style="cyan", width=15)
        table.add_column("Source", style="yellow", width=10)
        table.add_column("Path", style="dim", no_wrap=False)

        for name, info in self.projects.items():
            source_icon = "🌐" if info['source'] == 'github' else "📁"
            table.add_row(
                name,
                info['type'],
                f"{source_icon} {info['source']}",
                info['path']
            )

        console.print(table)
        input("\nPress Enter to continue...")

    def run_project(self):
        """Run a selected project"""
        if not self.projects:
            console.print("[yellow]No projects available. Add some first![/yellow]")
            input("\nPress Enter to continue...")
            return

        console.print(f"\n[bold {LIME_GREEN}]Run Project[/bold {LIME_GREEN}]")

        # Show projects list
        projects_list = list(self.projects.keys())
        for i, name in enumerate(projects_list, 1):
            info = self.projects[name]
            console.print(f"[{LIME_GREEN}]{i}[/{LIME_GREEN}]. {name} ([cyan]{info['type']}[/cyan])")

        try:
            choice = int(Prompt.ask("Select project", choices=[str(i) for i in range(1, len(projects_list) + 1)]))
            project_name = projects_list[choice - 1]
            project_info = self.projects[project_name]

            # Ask for run mode
            expose = Confirm.ask("Expose online? (No = localhost only)", default=False)

            # Run the project
            runner = ProjectRunner(project_info['path'], project_info['type'])
            runner.run(expose=expose, project_name=project_name)

        except (ValueError, KeyboardInterrupt):
            console.print("[yellow]Cancelled.[/yellow]")

        input("\nPress Enter to continue...")

    def remove_project(self):
        """Remove a project from LimeBox"""
        if not self.projects:
            console.print("[yellow]No projects to remove.[/yellow]")
            input("\nPress Enter to continue...")
            return

        console.print(f"\n[bold {LIME_GREEN}]Remove Project[/bold {LIME_GREEN}]")

        projects_list = list(self.projects.keys())
        for i, name in enumerate(projects_list, 1):
            console.print(f"[{LIME_GREEN}]{i}[/{LIME_GREEN}]. {name}")

        try:
            choice = int(Prompt.ask("Select project to remove", choices=[str(i) for i in range(1, len(projects_list) + 1)]))
            project_name = projects_list[choice - 1]

            if Confirm.ask(f"Remove '{project_name}'?", default=False):
                del self.projects[project_name]
                self.save_config()
                console.print(f"[{LIME_GREEN}]✅ Removed '{project_name}'[/{LIME_GREEN}]")

        except (ValueError, KeyboardInterrupt):
            console.print("[yellow]Cancelled.[/yellow]")

        input("\nPress Enter to continue...")

    def show_settings(self):
        """Show settings and configuration"""
        console.print(f"\n[bold {LIME_GREEN}]Settings[/bold {LIME_GREEN}]")

        settings_table = Table(show_header=False, box=None)
        settings_table.add_column("Setting", style=LIME_GREEN, width=20)
        settings_table.add_column("Value", style="white")

        settings_table.add_row("Config File", self.config_file)
        settings_table.add_row("Total Projects", str(len(self.projects)))
        settings_table.add_row("Working Directory", os.getcwd())

        console.print(Panel(settings_table, title=f"[bold {LIME_GREEN}]Current Settings[/bold {LIME_GREEN}]", border_style=LIME_GREEN))
        input("\nPress Enter to continue...")

    def run(self):
        """Main application loop"""
        while True:
            self.show_banner()
            self.show_menu()

            try:
                choice = Prompt.ask(f"\n[bold {LIME_GREEN}]Select option[/bold {LIME_GREEN}]", 
                                  choices=["0", "1", "2", "3", "4", "5", "6"])

                if choice == "0":
                    clear_terminal()
                    console.print(f"[{LIME_GREEN}]Thanks for using LimeBox! 🚀[/{LIME_GREEN}]")
                    break
                elif choice == "1":
                    self.add_local_project()
                elif choice == "2":
                    self.clone_github_project()
                elif choice == "3":
                    self.run_project()
                elif choice == "4":
                    self.list_projects()
                elif choice == "5":
                    self.remove_project()
                elif choice == "6":
                    self.show_settings()

            except KeyboardInterrupt:
                clear_terminal()
                console.print(f"\n[{LIME_GREEN}]Goodbye! 👋[/{LIME_GREEN}]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                input("Press Enter to continue...")

def main():
    parser = argparse.ArgumentParser(description="LimeBox - Terminal Project Runner")
    parser.add_argument('action', nargs='?', choices=['start', 'run'], default='start',
                       help='Action to perform (start or run)')

    args = parser.parse_args()

    # Check if running in terminal
    if not sys.stdout.isatty():
        print("LimeBox requires a terminal environment!")
        sys.exit(1)

    app = LimeBox()
    app.run()

if __name__ == "__main__":
    main()