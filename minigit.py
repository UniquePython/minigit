import os
import sys
import hashlib
from datetime import datetime


def check_init():
	if not os.path.exists(".minigit"):
		print("Not a minigit repository. Run 'init' first.")
		sys.exit(1)


def init():
	if not os.path.exists(".minigit"):
		# For storing file versions (blobs)
		os.makedirs(".minigit/objects")
		# For storing commit info
		os.makedirs(".minigit/commits")
		# Stores latest commit hash
		with open(".minigit/HEAD", "w") as HEAD:
			HEAD.write("")
		# To-do list for files ready to commit
		with open(".minigit/index", "w") as index:
			index.write("")
		print("Initialized empty MiniGit repository in .minigit/")
	else:
		print("Repository already initialized.")


def hash_content(content):
	return hashlib.sha256(content.encode()).hexdigest()


def add(file_path):
	if not os.path.exists(file_path):
		print(f"File {file_path} does not exist.")
		return

	with open(file_path, "r") as file:
		content = file.read()

	hashed = hash_content(content)
	object_path = f".minigit/objects/{hashed}"

	if not os.path.exists(object_path):
		with open(object_path, "w") as file:
			file.write(content)

	with open(".minigit/index", "a") as index:
		index.write(f"{hashed} {file_path}\n")

	print(f"Added {file_path} to staging area.")


def commit(message):
	if not os.path.exists(".minigit/index"):
		print("Nothing to commit.")
		return

	with open(".minigit/index", "r") as index:
		entries = index.readlines()

	if not entries:
		print("Nothing to commit.")
		return

	timestamp = datetime.now().isoformat()
	commit_content = f"message: {message}\ntimestamp: {timestamp}\n"
	for line in entries:
		commit_content += line

	commit_hash = hash_content(commit_content)

	# Write commit to file
	with open(f".minigit/commits/{commit_hash}", "w") as commit_file:
		commit_file.write(commit_content)

	# Update HEAD
	with open(".minigit/HEAD", "w") as HEAD:
		HEAD.write(commit_hash)

	# Clear index
	with open(".minigit/index", "w") as index:
		index.write("")

	print(f"[{commit_hash[:7]}] {message}")


def status():
    # Get list of files in the working directory (excluding .minigit)
    working_files = set(os.listdir("."))
    working_files.discard(".minigit")  # Remove .minigit directory

    # Get list of staged files from the index
    with open(".minigit/index", "r") as index_file:
        staged_files = set(index_file.read().splitlines())

    # Get list of committed files from the last commit
    last_commit_file = ".minigit/HEAD"
    committed_files = set()
    if os.path.exists(last_commit_file):
        with open(last_commit_file, "r") as commit_file:
            commit_data = commit_file.read()
            lines = commit_data.splitlines()
            for line in lines:
                # Files are listed after the commit metadata (message, timestamp)
                if line:
                    committed_files.add(line.split(" ")[-1])  # Take file path

    # Identify changes to be committed, changes not staged, and untracked files
    to_commit = staged_files - committed_files  # Files in the index but not committed
    not_staged = working_files - staged_files - committed_files  # Modified files that aren't staged
    untracked = working_files - staged_files  # Files in working dir but not tracked

    print("Changes to be commited:")
    for file in to_commit:
        print(f"    new file: {file}")

    print("\nChanges not staged for commit:")
    for file in not_staged:
        print(f"    modified: {file}")

    print("\nUntracked files:")
    for file in untracked:
        print(f"    {file}")


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: python3 minigit.py <command>")
		sys.exit(1)

	command = sys.argv[1]

	if command == "init":
		init()
	elif command == "add":
		check_init()
		if len(sys.argv) != 3:
			print("Usage: python3 minigit.py add <file>")
		else:
			add(sys.argv[2])
	elif command == "commit":
		check_init()
		message = " ".join(sys.argv[2:])
		commit(message)
	elif command == "status":
		check_init()
		status()
	else:
		print(f"Command '{command}' not found.")
