# Markdown Conventions

These rules are enforced by the markdownlint VS Code extension for all `.md` files in this repo.

## Code Blocks

- **Style**: Always use fenced blocks (` ``` `), never indented blocks.
- **Fence character**: Backticks only — not tildes.
- **Language required**: Every fenced block must declare one of the allowed languages (see below).

### Allowed Fenced Code Languages

| Language     | Use for                                      |
| ------------ | -------------------------------------------- |
| `bash`       | Shell commands, `.env` file contents         |
| `html`       | HTML markup                                  |
| `javascript` | JavaScript                                   |
| `typescript` | TypeScript                                   |
| `css`        | Stylesheets                                  |
| `json`       | JSON data                                    |
| `markdown`   | Markdown examples                            |
| `text`       | Plain/neutral output with no highlighting    |
| `xml`        | XML markup                                   |
| `python`     | Python scripts                               |
| `powershell` | PowerShell commands                          |
| `csharp`     | C# code                                      |
| `kusto`      | KQL / Azure Data Explorer queries            |
| `mermaid`    | Mermaid diagrams                             |

No other language identifiers are permitted.

## Headings

- Use ATX style (`#`, `##`, etc.) — not underline (setext) style.
- Duplicate heading names are allowed **within the same section level**, but not among siblings at the same level.

## Emphasis and Bold

- Use `*asterisks*` for *italic* — not underscores.
- Use `**asterisks**` for **bold** — not underscores.

## Horizontal Rules

- Use `---` only.

## Links and Images

- Use full inline or reference-link syntax.
- **No** collapsed reference links (`[text][]`).
- **No** shortcut reference links (`[text]`).
- **No** bare inline URLs — always wrap in `[label](url)` syntax.
- Reference-link shortcut syntax is allowed for images.

## Lists

- **Unordered lists**: Use `-` (dash) — not `*` or `+`.
- **Ordered lists**: Use sequential numbers (`1.`, `2.`, `3.`) — not repeated `1.`.

## Line Length

- No enforced line length limit (MD013 is disabled).

## Extended ASCII / Special Characters

- Use ASCII characters only in Markdown prose.
- Emojis in commit messages are fine (those live in git, not Markdown body text).

## Proper Names

The following names must be capitalized/spelled exactly as shown (outside code blocks):

- `CommonMark`
- `JavaScript`
- `Markdown`
- `markdown-it`
- `markdownlint`
- `Node.js`
