# Project Creator

This Python program helps you create a new project directory, copy templates into it, create a git repository (on GitHub) for the project, and launch Visual Studio Code.

## Requirements

* Python 3.x
* A GitHub account with a personal access token (PAT)

## Installation

1. Clone this repository.
2. Install the required packages: \`pip install -r requirements.txt\`
3. Run the program: \`python project_creator.py\`

## Usage

1. Run the program: \`python project_creator.py\`
2. Enter the project name when prompted.
3. Choose a template to use (if desired), either a local one or one from your GitHub account.
4. Decide whether to create a Git repository for the project (if you have a GitHub PAT).
5. Decide whether to launch Visual Studio Code to work on the project.

## Configuration

The program will look for a config file at \`~/.projectcreator/config.json\`, and will create one if it doesn't exist. This file should contain your GitHub PAT, like so:

\`\`\`json
{
    "github_token": "your_token_here"
}
\`\`\`

You can also add your own templates to \`~/.projectcreator/templates\` by copying them there. The program will automatically detect any templates you add.

## Credits

This program was created by [ChatGPT](https://github.com/ChatGPT) using the GitHub API and the following packages:

* [PyGithub](https://github.com/PyGithub/PyGithub)
* [Shutil](https://docs.python.org/3/library/shutil.html)
* [Subprocess](https://docs.python.org/3/library/subprocess.html)

## License

This program is licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use and modify it as you see fit.
