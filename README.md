# Mini-Git

Mini-Git is a lightweight implementation of a Git-like version control system in Python. It allows you to initialize a repository, create commits, and checkout previous commits using SHA-256 based object storage.

---

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/UniquePython/minigit.git
cd minigit
```

No external dependencies are required beyond the Python standard library.

---

## Usage

The CLI interface provides three main commands: `init`, `commit`, and `checkout`.

### Initialize a repository

```bash
python main.py init -d <directory> --name "Your Name" --email "you@example.com"
```

- `-d` or `--directory`: Directory to initialize the repository (default: current directory)

- `--name`: Author/committer name

- `--email:` Author/committer email

### Commit changes

```bash
python main.py commit -m "Commit message" -d <directory>
```

- `-m` or `--message`: Commit message (required)

- `-d` or `--directory`: Directory to commit (default: current directory)

### Checkout a commit

```bash
python main.py checkout <commit_id> -d <directory>
```

- `<commit_id>`: SHA-256 hash of the commit to restore

- `-d` or `--directory`: Directory to restore files into (default: current directory)

---

## File Structure

- `blob.py` – Handles object hashing, storage, and retrieval.

- `TreeEntry.py` – Dataclass representing a tree entry (file or directory).

- `tree.py` – Creates and reads tree objects representing directories.

- `config.py` – Reads username/email configuration.

- `commit.py` – Creates and reads commit objects.

- `checkout.py` – Restores the working directory to a specific commit.

- `init.py` – Initializes a new repository and stores configuration.

- `main.py` – Command-line interface to interact with the repository.

---

## License

MIT License