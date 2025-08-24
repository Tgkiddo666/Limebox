#!/usr/bin/env python3

import subprocess
import json
import os
from utils import detect_project_type, install_dependencies, run_project

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
            # Add local project logic here
            pass
        elif choice == '2':
            # Add GitHub project logic here
            pass
        elif choice == '3':
            project_path = input("Enter project path: ")
            project_type = detect_project_type(project_path)
            install_dependencies(project_path, project_type)
            run_project(project_path, project_type, config)
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
