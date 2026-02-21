---
description: how to run the Hugo site locally for development
---

// turbo-all

1. From the repo root, run the Hugo development server:

```powershell
hugo server -D
```

The `-D` flag includes draft content. The site will be available at <http://localhost:1313>.

1. Hugo will watch for file changes and hot-reload automatically.

2. To stop the server, press `Ctrl+C`.

> **Note**: The `public/` and `resources/` directories are generated at build time and are gitignored. Do not commit them.
