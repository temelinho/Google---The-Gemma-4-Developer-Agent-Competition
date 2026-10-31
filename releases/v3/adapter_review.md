# External adapter review

No external adapter has been added to this candidate.

- [eexian weighted reasoning LoRA](https://huggingface.co/eexian/gemma4-31b-w4-weighted-reasoning-lora)
  declares the correct QAT W4 base and reports serving/activation checks. Its card
  explicitly distinguishes those checks from repair accuracy, which was still
  under evaluation when inspected. It also points to mixed upstream training
  terms rather than providing a blanket relicensing statement. Adding roughly
  490 MB without a measured gain would introduce an untested variable.
- [KikoCis Agent V6 MLX](https://huggingface.co/KikoCis/gemma-4-31b-agent-v6-MLX)
  has an Apache-2.0 model-card license and reports agent experiments, but its
  adapter format and tested runtime are MLX on Apple Silicon. Its card does not
  establish that these files work as a PEFT adapter on the competition's vLLM
  QAT model.

These observations do not establish that the adapters are unusable. They explain
why neither is silently bundled as a proven improvement in this experiment.
