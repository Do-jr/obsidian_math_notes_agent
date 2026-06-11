# Local Obsidian Search Tool

This adds a small local search tool for your copied Obsidian vault.

It only reads Markdown notes. It does not edit, delete, rename, or move your notes.

## Files created

- `obsidian_search.py` - the Python search tool.
- `SEARCH_TOOL_README.md` - these instructions.

## How to run it

1. Open PowerShell.

2. Go to the folder where the tool was created:

```powershell
cd "C:\Users\ddjr\Documents\obsidian_notes_control"
```

3. Run the search tool on your copied vault.

On this computer, PowerShell did not recognize the short command `python`, so use this longer command:

```powershell
& "C:\Users\ddjr\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\obsidian_search.py "C:\Users\ddjr\Desktop\obsidian notes.valut"
```

If you later install Python normally, this shorter command should also work:

```powershell
python .\obsidian_search.py "C:\Users\ddjr\Desktop\obsidian notes.valut"
```

4. When it asks what you want to search for, type your question or keywords, then press Enter.

Example:

```text
What do you want to search for? compactness theorem
```

The tool will show matching note paths, the nearest heading, and a short snippet.

## One-line search

You can also put the search words directly in the command:

```powershell
& "C:\Users\ddjr\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\obsidian_search.py "C:\Users\ddjr\Desktop\obsidian notes.valut" --query "compactness theorem"
```

## Show more results

This shows up to 20 results:

```powershell
& "C:\Users\ddjr\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" .\obsidian_search.py "C:\Users\ddjr\Desktop\obsidian notes.valut" --query "compactness theorem" --limit 20
```

## Notes

- Your copied vault path is currently:

```text
C:\Users\ddjr\Desktop\obsidian notes.valut
```

- I found 608 Markdown notes there during setup.
- The folder name says `valut`, not `vault`, so the commands above use that exact spelling.
