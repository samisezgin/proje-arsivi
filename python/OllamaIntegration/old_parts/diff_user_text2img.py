import torch
from diffusers import AutoPipelineForText2Image
import ollama
import os
from datetime import datetime

# --- AYARLAR ---
IMAGE_MODEL = "stabilityai/sdxl-turbo"  # 12GB VRAM için en hızlısı
CHAT_MODEL = "gemma3:4b"  # Ollama'da indirdiğin model

# Klasörleme yapısı
today = datetime.now().strftime("%Y-%m-%d")
save_dir = f"generated_photos/{today}"
os.makedirs(save_dir, exist_ok=True)

print("Modeller yükleniyor, lütfen bekleyin...")

# Resim motorunu yükle (Sadece 1 kez yüklenir)
pipe = AutoPipelineForText2Image.from_pretrained(IMAGE_MODEL, torch_dtype=torch.float16, variant="fp16")
pipe.to("cuda")  # RTX 4070 Ti gücü!


def resim_uret(prompt):
    timestamp = datetime.now().strftime("%H-%M-%S")
    file_path = f"{save_dir}/resim_{timestamp}.png"

    print(f"🎨 Resim çiziliyor: {prompt}")
    # SDXL Turbo ile 2 adımda hızlı üretim
    image = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
    image.save(file_path)
    print(f"✅ Resim kaydedildi: {file_path}")
    return file_path


# --- ANA DÖNGÜ ---
print("\n--- AI Asistan Hazır! ---")
print("Not: 'resim' veya 'çiz' derseniz resim üretirim, yoksa sohbet ederiz.")

while True:
    user_input = input("\nSiz: ")

    if user_input.lower() in ['exit', 'çıkış']: break

    # Eğer kullanıcı resim istiyorsa
    if "resim" in user_input.lower() or "çiz" in user_input.lower():
        # Ollama'dan resmi betimlemesini isteyebiliriz veya direkt inputu kullanabiliriz
        resim_uret(user_input)
    else:
        # Normal sohbet (Ollama)
        response = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': user_input}])
        print(f"AI: {response['message']['content']}")