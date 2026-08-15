import torch
import warnings
import os
from datetime import datetime
from diffusers import AutoPipelineForText2Image, StableVideoDiffusionPipeline
from diffusers.utils import export_to_video

# Suppress warnings for clean output
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

IMAGE_MODEL = "stabilityai/sdxl-turbo"
VIDEO_MODEL = "stabilityai/stable-video-diffusion-img2vid-xt"

print("🚀 Loading models into VRAM (Optimized for RTX 4070 Ti)...")

# Modelleri döngü dışında, global olarak bir kez yüklüyoruz
img_pipe = AutoPipelineForText2Image.from_pretrained(
    IMAGE_MODEL, torch_dtype=torch.float16, variant="fp16"
)
vid_pipe = StableVideoDiffusionPipeline.from_pretrained(
    VIDEO_MODEL, torch_dtype=torch.float16, variant="fp16"
)

# RAM ve VRAM arasında akıllı trafik yönetimi
img_pipe.enable_sequential_cpu_offload()
vid_pipe.enable_sequential_cpu_offload()


def generate_media(prompt, is_video=False):
    today = datetime.now().strftime("%Y-%m-%d")
    save_dir = f"generated_media/{today}"
    os.makedirs(save_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%H-%M-%S")

    # 1. Generate Image
    full_prompt = f"{prompt}, high quality, masterpiece, realistic, 8k"
    image = img_pipe(prompt=full_prompt, num_inference_steps=2, guidance_scale=0.0).images[0]

    img_path = f"{save_dir}/image_{timestamp}.png"
    image.save(img_path)

    # Clear cache after image generation
    torch.cuda.empty_cache()

    if is_video:
        # 2. Generate Video
        # Resize to vertical format for YouTube Shorts
        image.resize((576, 1024))
        random_seed = torch.seed()
        generator = torch.manual_seed(random_seed)
        # Parallel processing with chunk size 4
        frames = vid_pipe(
            image,
            decode_chunk_size=4,
            num_frames=10,
            motion_bucket_id=180,
            noise_aug_strength=0.2,
            generator=generator
        ).frames[0]

        vid_path = f"{save_dir}/video_{timestamp}.mp4"
        export_to_video(frames, vid_path, fps=5)

        # Final cache cleanup
        torch.cuda.empty_cache()
        return vid_path

    return img_path