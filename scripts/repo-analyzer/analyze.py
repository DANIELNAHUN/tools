"""Analyze git repositories for status, changes, and .env backups.

Usage:
    uv run analyze.py                              # analyze all repos in REPOS_PATH env or current dir
    uv run analyze.py --path /path/to/repos        # specific directory
    uv run analyze.py --repos repo1,repo2          # filter specific repos
    uv run analyze.py --path /repos --repos repo1  # combine both

Environment variables:
    REPOS_PATH  - Default path to repos directory (overridden by --path)
    OUTPUT_DIR  - Output directory for reports and backups (default: output)
"""

import argparse
import os
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def run_git(repo_path: Path, *args: str) -> str:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + list(args),
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def is_git_repo(path: Path) -> bool:
    """Check if a directory is a git repository."""
    return (path / ".git").is_dir()


def get_remote_url(repo_path: Path) -> str:
    """Get the remote URL of the repository."""
    return run_git(repo_path, "remote", "get-url", "origin")


def has_recent_commits(repo_path: Path, days: int = 30) -> bool:
    """Check if the repo has commits in the last N days."""
    since = f"--since={days} days ago"
    count = run_git(repo_path, "rev-list", "--count", since, "HEAD")
    try:
        return int(count) > 0
    except ValueError:
        return False


def get_last_commit_date(repo_path: Path) -> str:
    """Get the date of the last commit."""
    return run_git(repo_path, "log", "-1", "--format=%ci")


def get_local_changes(repo_path: Path) -> dict:
    """Get local changes (uncommitted + unpushed)."""
    status = run_git(repo_path, "status", "--porcelain")
    unpushed = run_git(repo_path, "log", "--oneline", "@{upstream}..HEAD")

    modified = [l.strip() for l in status.splitlines() if l.startswith(" M")]
    untracked = [l.strip() for l in status.splitlines() if l.startswith("??")]

    return {
        "modified": modified,
        "untracked": untracked,
        "unpushed_commits": unpushed.splitlines() if unpushed else [],
    }


def find_env_files(repo_path: Path) -> list[Path]:
    """Find all .env files in the repository."""
    env_files = []
    for item in repo_path.rglob(".env*"):
        if item.is_file() and item.name != ".env.example":
            env_files.append(item)
    return env_files


def backup_env_files(repo_path: Path, output_dir: Path) -> Path | None:
    """Backup .env files to a zip archive."""
    env_files = find_env_files(repo_path)
    if not env_files:
        return None

    backup_name = f"{repo_path.name}_env_backup.zip"
    backup_path = output_dir / backup_name

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for env_file in env_files:
            arcname = env_file.relative_to(repo_path)
            zf.write(env_file, arcname)

    return backup_path


def analyze_repo(repo_path: Path) -> dict:
    """Analyze a single repository."""
    result = {
        "name": repo_path.name,
        "path": str(repo_path),
        "is_valid": False,
        "remote_url": "",
        "last_commit": "",
        "active": False,
        "local_changes": {},
        "env_backup": None,
    }

    if not is_git_repo(repo_path):
        return result

    result["is_valid"] = True
    result["remote_url"] = get_remote_url(repo_path)
    result["last_commit"] = get_last_commit_date(repo_path)
    result["active"] = has_recent_commits(repo_path)
    result["local_changes"] = get_local_changes(repo_path)

    # Backup .env files
    output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    result["env_backup"] = backup_env_files(repo_path, output_dir)

    return result


def generate_report(results: list[dict], output_dir: Path) -> Path:
    """Generate a summary report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"repo_analysis_{timestamp}.md"

    lines = [
        "# Repository Analysis Report",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\nTotal repositories: {len(results)}",
        f"Valid git repos: {sum(1 for r in results if r['is_valid'])}",
        f"Active repos: {sum(1 for r in results if r['active'])}",
        "\n---\n",
    ]

    for r in results:
        status = "ACTIVE" if r["active"] else "INACTIVE"
        valid = "OK" if r["is_valid"] else "NOT A GIT REPO"
        lines.append(f"## {r['name']}")
        lines.append(f"- Status: **{status}** ({valid})")
        lines.append(f"- Path: `{r['path']}`")
        if r["remote_url"]:
            lines.append(f"- Remote: `{r['remote_url']}`")
        if r["last_commit"]:
            lines.append(f"- Last commit: {r['last_commit']}")

        changes = r["local_changes"]
        has_changes = (
            changes.get("modified")
            or changes.get("untracked")
            or changes.get("unpushed_commits")
        )
        if has_changes:
            lines.append("- **Local changes:**")
            if changes.get("modified"):
                lines.append(f"  - Modified: {', '.join(changes['modified'])}")
            if changes.get("untracked"):
                lines.append(f"  - Untracked: {', '.join(changes['untracked'])}")
            if changes.get("unpushed_commits"):
                lines.append(f"  - Unpushed: {len(changes['unpushed_commits'])} commits")

        if r["env_backup"]:
            lines.append(f"- .env backup: `{r['env_backup']}`")

        lines.append("")

    report_path.write_text("\n".join(lines))
    return report_path


def main():
    parser = argparse.ArgumentParser(
        description="Analyze git repositories for status and changes"
    )
    parser.add_argument(
        "--path",
        default=os.getenv("REPOS_PATH", "."),
        help="Directory containing git repositories (default: REPOS_PATH env var or current dir)",
    )
    parser.add_argument(
        "--repos",
        default=None,
        help="Comma-separated list of repo names to analyze (default: all)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Days to consider a repo as active (default: 30)",
    )
    args = parser.parse_args()

    base_path = Path(args.path).resolve()
    if not base_path.is_dir():
        print(f"Error: Directory not found: {args.path}")
        sys.exit(1)

    # Collect repos to analyze
    filter_repos = None
    if args.repos:
        filter_repos = [r.strip() for r in args.repos.split(",")]

    repos = []
    for item in sorted(base_path.iterdir()):
        if not item.is_dir():
            continue
        if filter_repos and item.name not in filter_repos:
            continue
        if is_git_repo(item):
            repos.append(item)

    if not repos:
        print("No git repositories found.")
        sys.exit(0)

    print(f"Analyzing {len(repos)} repositories...\n")

    results = []
    for repo in repos:
        print(f"  Analyzing: {repo.name}")
        result = analyze_repo(repo)
        results.append(result)

        status = "ACTIVE" if result["active"] else "INACTIVE"
        changes = result["local_changes"]
        has_changes = (
            changes.get("modified")
            or changes.get("untracked")
            or changes.get("unpushed_commits")
        )
        extra = " [CHANGES]" if has_changes else ""
        print(f"    -> {status}{extra}")

    # Generate report
    output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = generate_report(results, output_dir)

    print(f"\nReport saved to: {report_path}")
    print(f"Backups saved to: {output_dir}/")


if __name__ == "__main__":
    main()
