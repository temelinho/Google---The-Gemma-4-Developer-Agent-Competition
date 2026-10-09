# Kaggle resmi sample_submission - okunan config'ler (referans)

Data sekmesinden okundu (tarayici onizleme). Yapimizi buna gore hizaladik.

## sample_submission/agent.yaml (438 B)
```yaml
name: swe_baseline_agent
model: gemma-4-31b-it-qat-w4a16-ct
adapter: main_lora
instruction: !include prompts/system.md
tools:
  - run_command
  - read_file
  - edit_file
  - write_file
  - get_status
  - submit_patch
  - get_code_neighbors
  - search_similar_code
  - get_code_subgraph
  - agent_tool:
      config_path: sub_agents/code_analyzer.yaml
      skip_summarization: true
generate_content_config: !include configs/sampling.yaml
```

## sample_submission/sub_agents/code_analyzer.yaml (361 B)
```yaml
name: code_analyzer_agent
description: Analyzes repository source files ...
model: gemma-4-31b-it-qat-w4a16-ct
adapter: tool_lora
instruction: !include ../prompts/analyzer.md
tools:
  - read_file
  - search_similar_code
  - get_code_neighbors
  - get_code_subgraph
generate_content_config: !include ../configs/sampling.yaml
```

## Onemli stratejik notlar (Data sekmesinden)
- Egitim seti: 129 gorev, SADECE 4 repo: fastapi, rich, requests, httpx.
- Test seti: ~120 gorev, yari public/yari private; OZEL (private) repolardan derlenmis.
  -> Test repolari egitim repolarindan FARKLI. Ezber degil, GENELLEME gerekir.
- Toplam veri 22.42 GB (snapshots + wheels buyuk kisim).
- Resmi ornek 2 adapter kullaniyor: main_lora (ana), tool_lora (analist).
