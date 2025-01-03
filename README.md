# LazyHub

LazyHub is a Python automation tool designed to monitor changes in a local Git repository and push those changes to GitHub daily. It respects `.gitignore` rules and includes detailed commit messages with file changes and Git statistics.

## Features

- Automatically checks for changes in the repository daily.
- Commits changes with detailed commit messages:
  - Lists changed files.
  - Includes Git statistics (lines added, removed, etc.).
- Pushes committed changes to a remote GitHub repository.
- Can be run manually or scheduled as a `systemd` service.

## Requirements

- Python 3.7 or higher
- Libraries:
  - `GitPython`
  - `schedule`

## Installation

1. Clone the repository:
   git clone https://github.com/MrVulpesTech/LazyHub.git
   cd LazyHub
2. Install required Python libraries:
    pip install -r requirements.txt

## Usage

1. Run Manually
    You can run the script manually to check for and push changes:
    python lazyhub.py
2. Automate with systemd
    To automate the script, create a systemd service and timer:
        > Create a service file: /etc/systemd/system/lazyhub.service:
            [Unit]
            Description=LazyHub: Automatically commit and push changes to GitHub
            After=network.target

            [Service]
            ExecStart=/usr/bin/python3 /path/to/lazyhub.py
            WorkingDirectory=/path/to/repository
            Restart=always
        > Create a timer file: /etc/systemd/system/lazyhub.timer:
            [Unit]
            Description=Run LazyHub daily

            [Timer]
            OnCalendar=*-*-* 00:00:00
            Persistent=true

            [Install]
            WantedBy=timers.target
        > Enable and start the timer:
            sudo systemctl enable lazyhub.timer
            sudo systemctl start lazyhub.timer

## Configuration

    Edit the script variables as needed:

        REPO_PATH: Path to your local Git repository.
        GITHUB_REMOTE: Name of the GitHub remote (default is origin).

## License

    This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

    Feel free to fork the project and submit pull requests.

## Acknowledgments

    Built using GitPython and schedule.