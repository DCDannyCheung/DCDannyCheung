"""
GitHub Snake Animation Generator
Reads the user's contribution graph and renders it as an animated SVG snake.

Requires a GitHub token (PAT with read:user scope) and the user's contribution
data. For a simpler path, use Platane/snk instead of running this locally:

  https://github.com/Platane/snk

This script expects a JSON contribution file at ../contributions.json with the
shape:  [["YYYY-MM-DD", count], ...]
"""

import json
import os
import subprocess
from pathlib import Path

REPO = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(REPO, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# Fetch contribution data via gh CLI
def fetch_contributions(username):
    """Use the GitHub GraphQL API via gh to grab contribution counts."""
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays { date contributionCount }
            }
          }
        }
      }
    }
    """
    cmd = [
        "gh", "api", "graphql",
        "-f", f"query={query}",
        "-F", f"login={username}",
        "--jq",
        ".data.user.contributionsCollection.contributionCalendar.weeks[].contributionDays[] "
        "| [.date, .contributionCount] | @json"
    ]
    out = subprocess.check_output(cmd, text=True)
    rows = [json.loads(line) for line in out.strip().splitlines() if line]
    return rows

def main():
    username = os.environ.get("GITHUB_USERNAME", "DCDannyCheung")

    # Try to fetch live data; fall back to a placeholder file
    contrib_file = os.path.join(REPO, "..", "contributions.json")
    try:
        rows = fetch_contributions(username)
        with open(contrib_file, "w", encoding="utf-8") as f:
            json.dump(rows, f)
        print(f"Fetched {len(rows)} contribution days for {username}")
    except Exception as exc:
        print(f"Could not fetch contributions ({exc}); using local file if present")
        if not os.path.exists(contrib_file):
            print("No contributions.json found — skipping generation.")
            return

    # Delegate the SVG rendering to Platane/snk
    snk = "github.com/Platane/snk/snk.sh"
    for theme, name in (("github-dark", "github-snake-dark.svg"),
                        ("github", "github-snake.svg")):
        cmd = [
            "bash", "-c",
            f"curl -sL {snk} | bash -s {theme} -o {name}",
        ]
        subprocess.run(cmd, cwd=OUT_DIR, check=False)
        print(f"Generated {os.path.join(OUT_DIR, name)}")


if __name__ == "__main__":
    main()
