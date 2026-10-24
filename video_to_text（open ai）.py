# 把跟我一樣的舊擋清掉 一定要記得按喔喔喔
import os

for f in ["audio.webm", "audio.mp3", "audio.m4a"]:
    if os.path.exists(f):
        os.remove(f)

# 下載 
import yt_dlp

url = "https://www.youtube.com/watch?v=FsP9kzW-gUA"
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "audio.%(ext)s",
    "noplaylist": False,
    "continuedl": False,
    "overwrites": True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    filename = ydl.prepare_filename(info)

import whisper

model_size = "small"  
model = whisper.load_model(model_size, device="mps")
result = model.transcribe(filename, beam_size=1, language="en") 

#轉碼
def format_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def format_gemma(seconds):
    seconds = int(seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

srt = ""
for i, seg in enumerate(result["segments"]):
    srt += f"{i+1}\n"
    srt += f"{format_time(seg['start'])} --> {format_time(seg['end'])}\n"
    srt += seg['text'].strip() + "\n\n"

paragraphs = []
current = []
start_time = None

for seg in result["segments"]:
    if start_time is None:
        start_time = seg["start"]

    current.append(seg["text"].strip())

    # 每 180 秒切一個
    if seg["end"] - start_time > 180:
        text = " ".join(current)
        paragraphs.append(f"{format_gemma(start_time)} ||| {text}")
        current = []
        start_time = None

if current and start_time is not None:
    paragraphs.append(f"{format_gemma(start_time)} ||| {' '.join(current)}")

with open("output.srt", "w", encoding="utf-8") as f:
    f.write(srt)

with open("paragraphs.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(paragraphs))

print("done！")