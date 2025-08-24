import os
import subprocess
import json
import requests
from zipfile import ZipFile
from io import BytesIO

def detect_project_type(project_path):
    package_json_path = os.path.join(project_path, "package.json")
    requirements_txt_path = os.path.join(project_path, "requirements.txt")

    if os.path.exists(package_json_path):
        try:
            with open(package_json_path, 'r') as f:
                package_json = json.load(f)
                if "dependencies" in package_json:
                    return "node"
        except json.JSONDecodeError:
            pass
    elif os.path.exists(requirements_txt_path):
        return "python"
    return "unknown"

def install_dependencies(project_path, project_type):
    if project_type == "node":
        try:
            subprocess.run(["npm", "install"], cwd=project_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing Node.js dependencies: {e}")
    elif project_type == "python":
        try:
            subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=project_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing Python dependencies: {e}")
    else:
        print("No dependencies to install for this project type.")

def run_project(project_path, project_type, config):
    print(f"Running project at {project_path}")
    if project_type == "node":
        try:
            subprocess.run(["npm", "start"], cwd=project_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running Node.js project: {e}")
    elif project_type == "python":
        try:
            subprocess.run(["python", "-m", "main"], cwd=project_path, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running Python project: {e}")
    else:
        print("Unknown project type. Cannot run.")

def get_github_repo(repo_url):
    try:
        #extract owner and repo name
        owner, repo = repo_url.split('/')[-2:]
        #download repository from github api
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/zipball", stream = True)
        response.raise_for_status()
        with ZipFile(BytesIO(response.content)) as zf:
            zf.extractall('./temp')
        #get directory name
        folder_name = os.listdir('./temp')[0]
        final_path = os.path.join('./temp', folder_name)
        return final_path
    except Exception as e:
        raise Exception(f"Error downloading or extracting GitHub repo: {e}")
