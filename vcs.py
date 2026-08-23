import subprocess


def run_git_command(command):

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout.strip()

    except subprocess.CalledProcessError:

        return ""


def get_current_branch():

    return run_git_command(
        ["git", "branch", "--show-current"]
    )


def get_commit_count():

    result = run_git_command(
        ["git", "rev-list", "--count", "HEAD"]
    )

    if result:
        return int(result)

    return 0


def get_file_count():

    result = run_git_command(
        ["git", "ls-files"]
    )

    if not result:
        return 0

    return len(result.splitlines())


def get_status():

    result = run_git_command(
        ["git", "status", "--short"]
    )

    if result:

        return "Changes detected"

    return "Working tree clean"


def get_recent_commits():

    result = run_git_command([
        "git",
        "log",
        "-5",
        "--pretty=format:%h|%s|%an"
    ])

    commits = []

    if result:

        for line in result.splitlines():

            parts = line.split("|", 2)

            if len(parts) == 3:

                commits.append({

                    "hash": parts[0],

                    "message": parts[1],

                    "author": parts[2]

                })

    return commits


def get_vcs_data():

    return {

        "branch": get_current_branch(),

        "commits": get_commit_count(),

        "files": get_file_count(),

        "status": get_status(),

        "recent_commits": get_recent_commits()

    }