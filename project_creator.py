import os
import json
import shutil
import subprocess
from github import Github


def create_project_folder(project_name):
    os.makedirs(project_name, exist_ok=True)


def create_github_repo(project_name, token):
    g = Github(token)
    user = g.get_user()
    repo = user.create_repo(project_name, private=True)
    return repo


def init_and_push_repo(project_name, repo):
    os.chdir(project_name)
    os.system("git init")
    os.system("git remote add origin {}".format(repo.ssh_url))
    os.system("git add .")
    os.system("git commit -m 'Initial commit'")
    os.system("git branch -M master")
    os.system("git push -u origin master")
    os.chdir("..")


def check_and_create_config():
    config_path = os.path.expanduser("~/.projectcreator")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        with open(os.path.join(config_path, "config.json"), "w") as config_file:
            json.dump({"github_token": ""}, config_file)
    return config_path


def get_github_token():
    config_path = check_and_create_config()
    with open(os.path.join(config_path, "config.json"), "r") as config_file:
        config = json.load(config_file)
    return config.get("github_token")


def list_templates():
    config_path = check_and_create_config()
    templates_path = os.path.join(config_path, "templates")
    if os.path.exists(templates_path):
        templates = os.listdir(templates_path)
        return templates
    return []


def list_cloud_templates(token):
    g = Github(token)
    user = g.get_user()
    repos = user.get_repos()
    templates = [
        repo.name for repo in repos if repo.name.endswith("-template")]
    return templates


def copy_template(template_name, project_name):
    config_path = check_and_create_config()
    template_path = os.path.join(config_path, "templates", template_name)
    if os.path.exists(template_path):
        shutil.copytree(template_path, project_name, dirs_exist_ok=True)
        return True
    return False


def clone_cloud_template(template_name, project_name, token):
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(template_name)
    if repo:
        os.system(f"git clone {repo.clone_url} {project_name}")
        os.chdir(project_name)
        os.system("git remote remove origin")
        os.chdir("..")
        return True
    return False


def create_readme(project_name):
    with open(os.path.join(project_name, "README.md"), "w") as readme:
        readme.write(f"# {project_name}\n")


def launch_vscode(project_name):
    subprocess.call(["code", project_name])


def main():
    project_name = input("Enter the project name: ")
    create_project_folder(project_name)

    print("\nAvailable local templates:")
    templates = list_templates()
    for template in templates:
        print(template)

    token = get_github_token()
    if token:
        print("\nAvailable cloud templates:")
        cloud_templates = list_cloud_templates(token)
        for template in cloud_templates:
            print(template)
    else:
        print("No GitHub token found in the config file.")
        return
    print("(You can add your own templates by copying them to ~/.projectcreator/templates")
    while True:
        template_name = input(
            "\nDo you want to use a template? (Type the template name, 'no'): ")
        if template_name.lower() == "no":
            create_readme(project_name)
            break
        elif copy_template(template_name, project_name):
            print("Local template copied successfully.")
            break
        elif clone_cloud_template(template_name, project_name, token):
            print("Cloud template cloned successfully.")
            break
        else:
            print("Template not found. Please try again.")

    create_git_repo_answer = input(
        "Do you want to create a git repo? (yes/no) ").lower()
    if create_git_repo_answer == "yes":
        if not token:
            print("No GitHub token found in the config file.")
            return
        repo = create_github_repo(project_name, token)
        init_and_push_repo(project_name, repo)

    launch_vscode_answer = input(
        "Do you want to launch Visual Studio Code? (yes/no) ").lower()
    if launch_vscode_answer == "yes":
        launch_vscode(project_name)


if __name__ == "__main__":
    main()
