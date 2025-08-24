#!/usr/bin/env python3

import subprocess
import json
import os
from utils import detect_project_type, install_dependencies, run_project, get_github_repo

CONFIG_FILE = 'config.json'

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def add_local_project():
    project_path = input("Enter the absolute path to the project: ")
    project_name = input("Enter a name for this project: ")
    
    if not os.path.exists(project_path):
        print("Error: Project path does not exist.")
        return
    
    config = load_config()
    config[project_name] = project_path
    save_config(config)
    print(f"Project '{project_name}' added successfully.")

def add_github_project():
    repo_url = input("Enter the GitHub repository URL: ")
    project_name = input("Enter a name for this project: ")
    
    try:
        project_path = get_github_repo(repo_url)
        config = load_config()
        config[project_name] = project_path
        save_config(config)
        print(f"Project '{project_name}' added successfully.")
    except Exception as e:
        print(f"Error adding GitHub project: {e}")

def main():
    config = load_config()

    while True:
        print("\n⟟ LIMEBOX ⟟ - Terminal Project Runner")
        print("1. Add Local Project")
        print("2. Add GitHub Project")
        print("3. Run Project")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_local_project()
        elif choice == '2':
            add_github_project()
        elif choice == '3':
            project_name = input("Enter project name: ")
            if project_name not in config:
                print(f"Error: Project '{project_name}' not found.")
                continue
            project_path = config[project_name]
            project_type = detect_project_type(project_path)
            install_dependencies(project_path, project_type)
            run_project(project_path, project_type, config)
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
