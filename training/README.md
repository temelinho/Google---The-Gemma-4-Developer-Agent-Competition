# Fine-tune hatti (RFT = rejection sampling fine-tuning)

Amac: Gemma 4'u, testi gecen cozum kayitlariyla egitip bir LoRA adapter uretmek.

## Fikir
129 gorevin cevabi (patch + test) belli. Bir ogretmen ajani bu gorevlerde
kosturup SADECE testi gecen (resolved=True) trajectory'leri toplariz, onlarla
Gemma'ya LoRA egitiriz. Uretim motoru = yarismanin kendi degerlendiricisi.

## En saglam yol: resmi notebook'u temel al
Resmi starter notebook her seyi kuruyor (swegemma kurulumu + vLLM + Evaluator):
  kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent
Yap: "Copy & Edit" -> asagidaki degisiklikleri yap -> kosup traces uret.

### Notebook'tan dogrulanan gercekler (bunlara guven)
- Kurulum: swegemma + bagimliliklar "Gemma 4 Developer Agent Wheelhouse"
  dataset'inden offline pip ile kuruluyor. "Gemma 4" modeli ayri ek.
- vLLM: VllmConfig(model=MODEL_PATH, tool_call_parser='gemma4',
  reasoning_parser='gemma4', max_model_len=32768, enable_lora=True,
  max_loras=8, max_lora_rank=128, tensor_parallel_size=4, gpu_mem_util~0.90)
- Degerlendirme: EvalConfig(tasks_path, snapshots_dir, results_dir,
  submission_dir) + SUBPROCESS sandbox (Kaggle'da Docker yok).
- Sonuc objesi alanlari: result.resolved (bool), result.agent_patch (str),
  result.test_exit_code, result.tool_calls, result.duration_seconds
- Trajectory kayitlari: results_dir/traces/  (adim adim).

### Uretim icin notebook'ta degistirilecekler
1. SAMPLE_TASKS = tasks[:2]  ->  tasks (hepsi, 129)   # TUM gorevler
2. sampling.yaml temperature 0.2 -> 0.7-1.0           # cesitlilik icin
3. Ayni kosuyu birkac kez farkli results_dir ile kos  # trajectory havuzu buyut
   (ornek: results/gen_01, gen_02, ... her biri farkli seed)
4. results_dir'i Kaggle Output olarak kaydet (sonra indirip suzecegiz)

## Adimlar (dosyalar)
1. (notebook)              -> traces + resolved uretir  (Kaggle L4x4, ~saatler)
2. 02_filter_build_sft.py -> resolved=True olanlari suz, SFT jsonl'e cevir
3. 03_train_lora.py       -> SFT jsonl ile LoRA egit -> adapters/main_lora

## Onemli: GPU execution arkadasin Kaggle hesabinda kosar
Bu hatti Claude burada "calistiramaz" - saatlerce L4x4 GPU gerekir, o da sizin
Kaggle notebook'unuzda calisir. Buradaki dosyalar hazir reçete; kosmak sizde.

## Ogretmen secimi
Baslangic: Gemma 4 31B'nin KENDISI (self-distillation, yuksek temperature).
Not: base Gemma bazi gorevleri cozemez -> o gorevlerden trajectory cikmaz, normal.
Gecenleri tut, havuzu birden fazla kosu ile buyut.
