import torch
from diffusers import AutoPipelineForText2Image
import ollama
import os
from datetime import datetime

# --- AYARLAR ---
IMAGE_MODEL = "stabilityai/sdxl-turbo"
CHAT_MODEL = "gemma3:4b"  #

# Klasörleme
today = datetime.now().strftime("%Y-%m-%d")
save_dir = f"generated_photos/{today}"
os.makedirs(save_dir, exist_ok=True)

# Modelleri Yükle
pipe = AutoPipelineForText2Image.from_pretrained(IMAGE_MODEL, torch_dtype=torch.float16, variant="fp16")
pipe.to("cuda")  #


def resim_ciz(prompt):
    timestamp = datetime.now().strftime("%H-%M-%S")
    file_path = f"{save_dir}/ai_resim_{timestamp}.png"
    # Pozitif prompt ekleyerek kaliteyi artırıyoruz
    full_prompt = f"{prompt}, high quality, masterpiece, realistic, 4k"
    image = pipe(prompt=full_prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
    image.save(file_path)
    return file_path


print("\n--- Akıllı Asistan Hazır! ---")

while True:
    user_input = input("\nSiz: ")
    if user_input.lower() in ['çıkış', 'exit']: break

    # 1. ADIM: Ollama'ya soruyoruz (Kullanıcı resim mi istiyor?)
    # Gemma'ya kullanıcının niyetini analiz ettiriyoruz
    check_prompt = (
        f"Kullanıcı şunu dedi: '{user_input}'.\n"
        "GÖREV: Bu bir resim çizme, görsel oluşturma veya sanat isteği mi?\n"
        "KURAL: Sadece 'EVET' veya 'HAYIR' yaz. Başka hiçbir açıklama yapma, cümle kurma."
    )
    intent = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': check_prompt}])

    if "EVET" in intent['message']['content'].upper():
        # 2. ADIM: Gemma'dan resmi İngilizce ve detaylı betimlemesini istiyoruz (SDXL İngilizceyi daha iyi anlar)
        describe_prompt = f"'{user_input}' komutu için profesyonel, detaylı bir İngilizce görsel betimlemesi (prompt) yaz. Sadece betimlemeyi yaz."
        sd_prompt = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': describe_prompt}])

        print(f"🤖 Yapay Zeka Planlıyor: {sd_prompt['message']['content'][:50]}...")
        yol = resim_ciz(sd_prompt['message']['content'])
        print(f"✅ İstediğin resmi çizdim ve şuraya kaydettim: {yol}")
    else:
        # Normal Sohbet
        response = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': user_input}])
        print(f"AI: {response['message']['content']}")