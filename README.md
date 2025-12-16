![Mini-Git image](repository-img.png "Mini Git Image")

# Mini-Git ![Static Badge](https://img.shields.io/badge/Python-3.10%2B-green)

Mini-Git is a lightweight implementation of a Git-like version control system in Python. It allows you to initialize a repository, create commits, and checkout previous commits using SHA-256 based object storage.

---

## Goal

This project is only intended as a learning exercise to explore how Git works internally. This is missing a lot of features and optimizations that Git supports, and thus is not meant to be used as a substitute for Git. However, if you insist, give it a try for sure!

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

The CLI interface provides the following commands: 
- `init` 
- `commit`
- `checkout`
- `log`
- `cat-file`

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

### Log commit history

```bash
python main.py log
```

### Cat-file

```bash
python main.py cat-file <object-id>
```

- `<object-id>`: SHA-256 hash of the object to view the contents of

---

## File Structure

- `blob.py` – Handles object hashing, storage, and retrieval.

- `tree_entry.py` – Dataclass representing a tree entry (file or directory).

- `tree.py` – Creates and reads tree objects representing directories.

- `config.py` – Reads username/email configuration.

- `commit.py` – Creates and reads commit objects.

- `log.py` - Displays the commit history of the current repository.

- `cat_file.py` - Displays the contents of a stored object.

- `checkout.py` – Restores the working directory to a specific commit.

- `init.py` – Initializes a new repository and stores configuration.

- `main.py` – Command-line interface to interact with the repository.

---

## Coming soon ...

- Branch Refs
- Detached HEAD vs symbolic HEAD
- Diffing trees
- Partial checkouts
- Packfiles
- Executable version so that you can run it as a standalone program
- Test suite (eventually 😅)

---

## License

MIT License