# Evidence Coder V5: concise 31B diagnostic

Uses the official 31B QAT base model, the shorter V4 workflow, 256 thinking tokens,
48 tool calls and the same 255-second agent deadline. Adds general reminders
about complete return paths, recursion termination, test assertions and file-tool
path restrictions after inspecting V3's actual trajectories. No task answers or
repository-specific patch instructions are included.

This diagnostic runs on the five tasks for which the independent published
reference control passed: fastapi_15661, rich_3894, rich_3772, rich_3535, rich_3278.
Its result must be compared with the same five V3/V4 tasks, not their raw 12-task
denominators. It is a selected diagnostic subset and not a hidden-rank estimate.

Completed result: 1/5 resolved (rich_3894). This is worse than V3's 2/5 on the
same tasks, so the shorter prompt and lower thinking budget are not an accuracy
improvement in this diagnostic. In particular, rich_3278 produced no captured
patch before its deadline. Keep this candidate as experiment evidence, not as
the preferred upload while a more accurate measured candidate is available.
