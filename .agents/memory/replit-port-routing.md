---
name: Replit port routing
description: Routing behavior for custom workflows alongside artifact services.
---

When adding explicit port mappings for a custom web workflow, map its listener to the intended external port and include every active artifact service port.

**Why:** explicit mappings disable automatic port detection; an internally healthy server can still return a public gateway error when its external port is not mapped.

**How to apply:** compare the workflow port and the user's Preview URL, update `.replit` through its validation flow, preserve mappings for existing services, then verify an HTTP response through the public route.
