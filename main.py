"""Command-line interface to interact with the repository."""

import argparse
from pathlib import Path

import init
import tree
import commit
import checkout

def main():
    parser = argparse.ArgumentParser(description="Mini-git CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new repository")
    init_parser.add_argument(
        "-d", "--directory", type=str, default=".", help="Directory to initialize repo in"
        )
    init_parser.add_argument("--name", type=str, default="null", help="Author/committer name")
    init_parser.add_argument("--email", type=str, default="null", help="Email for commits")

    # commit command
    commit_parser = subparsers.add_parser("commit", help="Create a new commit")
    commit_parser.add_argument("-m", "--message", type=str, required=True, help="Commit message")
    commit_parser.add_argument(
        "-d", "--directory", type=str, default=".", help="Directory to commit"
        )

    # checkout command
    checkout_parser = subparsers.add_parser("checkout", help="Checkout a commit")
    checkout_parser.add_argument("commit_id", type=str, help="Commit hash to checkout")
    checkout_parser.add_argument(
        "-d", "--directory", type=str, default=".", help="Directory to restore files into"
        )

    args = parser.parse_args()

    if args.command == "init":
        init.init_repo(Path(args.directory), name=args.name, email=args.email)

    elif args.command == "commit":
        repo_dir = Path(args.directory) / ".minigit"
        if not repo_dir.exists():
            print("Error: No repository found. Run 'init' first.")
            return

        # 1. Create tree from working directory
        tree_id = tree.write_tree(Path(args.directory))

        # 2. Get parent commit if HEAD exists
        head_file = repo_dir / "HEAD"
        parent = head_file.read_text().strip() if head_file.exists() and head_file.read_text().strip() else None

        # 3. Write commit
        commit_id = commit.write_commit(tree_id, args.message, parent)
        print(f"Committed: {commit_id}")

    elif args.command == "checkout":
        commit_id = args.commit_id
        checkout.checkout(commit_id, Path(args.directory))
        print(f"Checked out commit: {commit_id}")


if __name__ == "__main__":
    main()
