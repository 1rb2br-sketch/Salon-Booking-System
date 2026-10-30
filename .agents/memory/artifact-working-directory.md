---
name: Artifact service working directories
description: Working-directory difference between artifact development workflows and production run commands.
---

Artifact development workflow commands run from the artifact directory, while production run arguments resolve from the workspace root.

**Why:** A root-level Python command failed in the managed development workflow because it looked for the script inside the artifact directory.

**How to apply:** Use a relative path from the artifact directory for development commands and a workspace-root path for production run arguments; verify both startup modes.
