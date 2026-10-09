"""
SFT jsonl ile Gemma 4 uzerine LoRA egitir. peft + transformers + trl.
Kaggle L4x4 (96GB) icin; base model offline erisilebilir olmali.
Hiperparametreler SWE-smith/SWE-Lego referanslarindan baslangic degerleri.
"""
# from datasets import load_dataset
# from peft import LoraConfig
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from trl import SFTTrainer, SFTConfig

MODEL = "gemma-4-31b-it-qat-w4a16-ct"   # yarisma modeli
LORA = dict(r=32, lora_alpha=64, lora_dropout=0.05,
            target_modules=["q_proj","k_proj","v_proj","o_proj",
                            "gate_proj","up_proj","down_proj"])
TRAIN = dict(learning_rate=5e-5, num_train_epochs=3,
             max_seq_length=32768, per_device_train_batch_size=1,
             gradient_accumulation_steps=16)

# TODO:
# 1) ds = load_dataset("json", data_files="training/sft.jsonl")
# 2) trace -> chat messages (tool-call formatinda) donusturucu
# 3) SFTTrainer ile egit
# 4) model.save_pretrained("submission/adapters/main_lora")  # adapter cikti
print("LoRA egitim iskeleti. Hiperparametreler:", LORA, TRAIN)
