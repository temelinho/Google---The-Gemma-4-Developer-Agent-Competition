# Public reference verification control

The independent reference run completed all 12 fixed development tasks in
approximately five minutes. Five passed: fastapi_15661 and all four Rich tasks.
Seven failed. These are reference-patch results, not agent accuracy.

Observed failures:

| Tasks | Evidence |
| --- | --- |
| fastapi_11355, fastapi_14512, fastapi_14953 | Test collection fails because inline_snapshot is unavailable. |
| requests_7505, requests_6757 | Broad test setup failures include recursive dependency involving the httpbin fixture; inspect complete logs for all failures. |
| requests_7427 | Seven ordinary assertion failures, including proxy boundary behavior; this is not established to be a dependency-only failure. |
| httpx_3672 | Collection fails because the imported httpx module lacks Stream. |

Therefore the full 12-task raw totals remain useful operational diagnostics but
are not a clean accuracy benchmark. The five reference-passing tasks provide a
conditional diagnostic comparison. They are selected after reference checking
and are not a representative hidden-test sample. A reference failure does not
establish that any agent patch is correct. No test/harness bypass or dependency
modification is shipped in any submission.

Source: private Kaggle notebook Gemma Public Reference Control, version 363377968,
using the official swegemma 0.2.11 verify_task function and published task.patch.
The candidate agent never sees reference patches.
