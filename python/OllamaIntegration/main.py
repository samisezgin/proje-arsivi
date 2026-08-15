import os
import ollama
import time

from moviepy import VideoFileClip, concatenate_videoclips

from ai_engine import generate_media
from youtube_uploader import upload_to_youtube

CHAT_MODEL = "gemma3:4b"


def autonomous_production_loop():
    # --- AYARLAR ---
    global concept
    CLIPS_PER_VIDEO = 3  # Bir Shorts videosu kaç farklı klipten oluşsun?
    produced_clips = []

    print(f"\n--- 🤖 Video Stitching Factory Active! Target: {CLIPS_PER_VIDEO} Clips ---")

    while len(produced_clips) < CLIPS_PER_VIDEO:
        try:
            # 1. Gemma brainstorms
            topic_req = (
                "ACT AS AN AVANT-GARDE CREATIVE DIRECTOR. "
                "Imagine a completely random and unique visual genre. "
                "Output ONLY a surreal 5-word concept that includes a dynamic action (e.g. melting, flying, growing). NO intro."
            )
            idea_res = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': topic_req}],
                                   options={'temperature': 1.0})
            concept = idea_res['message']['content'].strip().split('\n')[0].replace('*', '').replace('"', '')

            print(f"\n💡 Clip {len(produced_clips) + 1} Concept: {concept}")

            # 2. Visual Prompt
            sd_res = ollama.chat(model=CHAT_MODEL, messages=[{'role': 'user', 'content': f"Keywords for: {concept}"}])
            prompt_text = sd_res['message']['content'].strip().split('\n')[0]

            # 3. Production (Sadece Klip Üretimi)
            print("🎨 Producing clip...")
            clip_path = generate_media(prompt_text, is_video=True)
            produced_clips.append(clip_path)

            print(f"✅ Clip added to queue. ({len(produced_clips)}/{CLIPS_PER_VIDEO})")
            time.sleep(10)  # Bellek soğuması

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(30)

    # 4. VİDEO BİRLEŞTİRME VE YÜKLEME
    try:
        print("\n🎬 Stitching all clips together...")
        video_objects = [VideoFileClip(c) for c in produced_clips]
        final_video = concatenate_videoclips(video_objects, method="compose")

        final_output = f"generated_media/final_shorts_{int(time.time())}.mp4"
        final_video.write_videofile(final_output, codec="libx264", audio=False)  # Sessiz birleştirme

        print(f"🚀 Uploading Final Mashup to YouTube...")
        video_id = upload_to_youtube(final_output, f"{concept} Art Experience")
        print(f"🎬 Published! ID: {video_id}")

        # Orijinal kısa klipleri temizle (Disk dolmasın)
        #for c in produced_clips: os.remove(c)

    except Exception as e:
        print(f"⚠️ Stitching/Upload Error: {e}")

    # 5. Kapatma
    print("🌙 Work complete. Shutting down...")
    os.system("shutdown /s /f /t 60")


if __name__ == "__main__":
    autonomous_production_loop()