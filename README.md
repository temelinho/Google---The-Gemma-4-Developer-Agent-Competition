# Gemma 4 Developer Agent Competition

Google DeepMind / Kaggle yarismasi. Amac: `gemma-4-31b-it-qat-w4a16-ct`
modelini, repo hatalarini otonom cozen bir ajana donusturmek.

## Klasor yapisi

```
submission/            -> submission.zip icine girecek olan her sey
├── agent.yaml         -> ZORUNLU: kok ajan config (ADK Agent Config)
├── prompts/system.md  -> system prompt
├── configs/           -> uretim parametreleri (sampling.yaml)
├── sub_agents/        -> alt ajanlar (opsiyonel)
├── adapters/          -> egitilmis LoRA ek beyinleri (.safetensors)
└── skills/            -> ADK skill klasorleri

training/              -> veri indirme + trajectory + LoRA egitim kodlari
docs/                  -> notlar, plan
```

## Is bolumu
- Temel  -> ajan tarafi (agent.yaml, prompt, araclar, skills)
- Arkadas -> egitim tarafi (training/: veri, trajectory, LoRA)

## Onemli
- Buyuk dosyalar (.safetensors, veri) GitHub'a KONMAZ -> Kaggle Dataset.
- agent.yaml formati Kaggle dataset'indeki HARNESS_README.md'ye gore
  dogrulanacak; su anki hali baseline iskelettir.

## Tarihler
- 25 Kasim 2026: giris + takim birlesme son tarihi
- 2 Aralik 2026: final submission
