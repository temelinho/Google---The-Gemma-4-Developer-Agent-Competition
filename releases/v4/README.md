# Evidence Coder V4: speed comparison candidate

Tests the official 12B QAT model with a shorter prompt, 256 thinking tokens and
48 tool calls against the V3 31B candidate on the same 12 public development tasks.
The 255-second agent deadline is unchanged. No LoRA or reference answers are
included. This is a latency/accuracy hypothesis, not a proven improvement.

Completed result: 0/12 raw resolved and 0/5 on the same reference-passing
diagnostic subset. This candidate is not selected for upload. The real run
verified the exact local ZIP hash and completed successfully as a notebook;
notebook execution success does not mean task repair success.
