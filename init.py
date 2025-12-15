from pathlib import Path
from configparser import ConfigParser

def init_repo(dir: Path, name: str = "null", email: str = "null") -> None:
    """
    Initialize a new mini-git repository in the current directory.

    Args:
        dir (Path): The path in which the repository is to be initialized 
        name (str): Author/committer name
        email (str): Optional email for commits
    """
    repo_dir = dir / ".minigit"
    objects_dir = repo_dir / "objects"
    config_file = repo_dir / "config"
    head_file = repo_dir / "HEAD"

    # Create directories
    objects_dir.mkdir(parents=True, exist_ok=True)

    # Initialize HEAD (empty repository)
    head_file.write_text("")

    # Create config with user info
    config = ConfigParser()
    config["minigit"] = {"name": name, "email": email}
    with config_file.open("w") as f:
        config.write(f)

    print(f"Initialized empty mini-git repository in {repo_dir.resolve()}")
