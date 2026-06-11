from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


WORD_RE = re.compile(r"[\w\u0080-\uffff]+", re.UNICODE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass
class Match:
    score: int
    path: Path
    heading: str
    snippet: str


def words(text: str) -> list[str]:
    return [word.lower() for word in WORD_RE.findall(text)]


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def find_heading(lines: list[str], line_number: int) -> str:
    for index in range(line_number, -1, -1):
        match = HEADING_RE.match(lines[index])
        if match:
            return match.group(2).strip()
    return "(no heading)"


def make_snippet(lines: list[str], line_number: int, query_terms: set[str]) -> str:
    start = max(0, line_number - 1)
    end = min(len(lines), line_number + 2)
    text = " ".join(line.strip() for line in lines[start:end] if line.strip())
    text = re.sub(r"\s+", " ", text)

    if len(text) > 280:
        text = text[:277].rstrip() + "..."

    for term in sorted(query_terms, key=len, reverse=True):
        if not term:
            continue
        text = re.sub(
            re.escape(term),
            lambda found: f"[{found.group(0)}]",
            text,
            flags=re.IGNORECASE,
        )
    return text


def score_line(line: str, query_terms: set[str]) -> int:
    lower = line.lower()
    score = 0
    for term in query_terms:
        if term in lower:
            score += 10 + lower.count(term)
    return score


def search_file(path: Path, vault: Path, query_terms: set[str]) -> Match | None:
    text = read_text(path)
    lines = text.splitlines()

    best_line_number = -1
    best_score = 0

    for line_number, line in enumerate(lines):
        line_score = score_line(line, query_terms)
        if HEADING_RE.match(line):
            line_score *= 2
        if line_score > best_score:
            best_score = line_score
            best_line_number = line_number

    if best_score == 0:
        return None

    file_name_score = score_line(path.stem, query_terms) * 3
    total_score = best_score + file_name_score
    heading = find_heading(lines, best_line_number)
    snippet = make_snippet(lines, best_line_number, query_terms)

    return Match(
        score=total_score,
        path=path.relative_to(vault),
        heading=heading,
        snippet=snippet,
    )


def search_vault(vault: Path, query: str, limit: int) -> list[Match]:
    query_terms = set(words(query))
    if not query_terms:
        return []

    matches: list[Match] = []
    markdown_paths = {
        path.resolve()
        for pattern in ("*.md", "*.MD")
        for path in vault.rglob(pattern)
        if path.is_file()
    }

    for path in sorted(markdown_paths):
        if path.is_file():
            match = search_file(path, vault, query_terms)
            if match:
                matches.append(match)

    matches.sort(key=lambda item: item.score, reverse=True)
    return matches[:limit]


def print_results(matches: list[Match]) -> None:
    if not matches:
        print("No matching notes found.")
        return

    for number, match in enumerate(matches, start=1):
        print(f"\n{number}. {match.path}")
        print(f"   Heading: {match.heading}")
        print(f"   Snippet: {match.snippet}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search Markdown files in an Obsidian vault."
    )
    parser.add_argument(
        "vault",
        nargs="?",
        default=".",
        help="Path to your copied Obsidian vault. If omitted, searches this folder.",
    )
    parser.add_argument(
        "-q",
        "--query",
        help="Search text. If omitted, the tool asks you for it.",
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=10,
        help="Maximum number of results to show.",
    )
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    if not vault.exists() or not vault.is_dir():
        print(f"Vault folder not found: {vault}")
        return

    query = args.query
    if not query:
        query = input("What do you want to search for? ").strip()

    print(f"Searching Markdown notes in: {vault}")
    matches = search_vault(vault, query, args.limit)
    print_results(matches)


if __name__ == "__main__":
    main()
