import os
from datetime import datetime

import ollama
import torch
from diffusers import AutoPipelineForText2Image, StableVideoDiffusionPipeline
from diffusers.utils import export_to_video

# --- AYARLAR ---
IMAGE_MODEL = "stabilityai/sdxl-turbo"
VIDEO_MODEL = "stabilityai/stable-video-diffusion-img2vid-xt"  # Video motoru
CHAT_MODEL = "gemma3:4b"

# Klasörleme
today = datetime.now().strftime("%Y-%m-%d")
save_dir = f"generated_media/{today}"
os.makedirs(save_dir, exist_ok=True)

print("🚀 Modeller ekran kartına yükleniyor (RTX 4070 Ti)...")

# Resim Modeli
img_pipe = AutoPipelineForText2Image.from_pretrained(IMAGE_MODEL, torch_dtype=torch.float16, variant="fp16")
vid_pipe = StableVideoDiffusionPipeline.from_pretrained(VIDEO_MODEL, torch_dtype=torch.float16, variant="fp16")
img_pipe.enable_sequential_cpu_offload()
vid_pipe.enable_sequential_cpu_offload()


def medya_uret(prompt, video_olsun_mu=False):
    timestamp = datetime.now().strftime("%H-%M-%S")
    print("prompt:", prompt, "is_video:", video_olsun_mu)

    # 1. Önce Resim Üretilir
    full_prompt = f"{prompt}, high quality, masterpiece, realistic, 8k"
    image = img_pipe(prompt=full_prompt, num_inference_steps=2, guidance_scale=0.0).images[0]

    img_path = f"{save_dir}/resim_{timestamp}.png"
    image.save(img_path)
    print(f"✅ Resim hazır: {img_path}")
    # Resim bittikten hemen sonra, video başlamadan önce:
    torch.cuda.empty_cache()

    if video_olsun_mu:
        print("🎬 Video işleniyor (bu biraz sürebilir)...")
        # Video için resmi uygun boyuta getir
        # image = image.resize((512, 512))
        image = image.resize((512, 896))

        # Video üretimi (RTX 4070 Ti ile yaklaşık 1 dakika)
        # frames = vid_pipe(image, decode_chunk_size=8, generator=torch.manual_seed(42)).frames[0]
        frames = vid_pipe(image,
                          decode_chunk_size=4,  # VRAM koruması için düşürüldü
                          num_frames=25,
                          motion_bucket_id=127,  # Hareket miktarını artırır
                          generator=torch.manual_seed(42)).frames[0]

        vid_path = f"{save_dir}/video_{timestamp}.mp4"
        # export_to_video(frames, vid_path, fps=7)
        export_to_video(frames, vid_path, fps=15)
        torch.cuda.empty_cache()  # Belleği temizle

        return vid_path

    return img_path


print("\n--- Video & Resim Asistanı Hazır! ---")

while True:
    user_input = input("\nSiz: ")
    if user_input.lower() in ['çıkış', 'exit']: break

    # Niyet Analizi
    check_prompt = f"Kullanıcı: '{user_input}'. Bu bir görsel/video isteği mi? Sadece EVET veya HAYIR yaz."
    intent = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': check_prompt}])

    if "EVET" in intent['message']['content'].upper():
        is_video = "video" in user_input.lower()

        describe_prompt = f"'{user_input}' için SADECE 20 kelimelik, çok kısa ve öz bir İngilizce görsel betimlemesi yaz. Başka hiçbir şey yazma."
        sd_prompt = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': describe_prompt}])

        yol = medya_uret(sd_prompt['message']['content'], video_olsun_mu=is_video)
        print(f"🎉 İşlem tamamlandı: {yol}")
    else:
        response = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': user_input}])
        print(f"AI: {response['message']['content']}")
