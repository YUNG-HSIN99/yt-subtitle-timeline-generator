#把跟我一樣的舊擋清掉 一定要記得按喔喔喔
import os

for f in ["audio.webm", "audio.mp3", "audio.m4a"]:
    if os.path.exists(f):
        os.remove(f)

#下載
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "audio.%(ext)s",
    "noplaylist": False,

    # 禁止續傳
    "continuedl": False,

    # 防 cache
    "overwrites": True,
}

#改網址喔喔喔
import yt_dlp

url = "https://www.youtube.com/watch?v=ytZuGoYKJbc"

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=True)
    filename = ydl.prepare_filename(info)

#分析
from faster_whisper import WhisperModel

model_size = "small"

# Run with FP16
model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=4)

#新版 faster whisper 同時回傳 segments 和 info
segments, info = model.transcribe(filename, beam_size=3, vad_filter=True, language="en"  )

# 轉碼
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

# 生檔案
srt = ""

# 新版 segments 只能讀取一次
all_segments = []
for i, seg in enumerate(segments):
    all_segments.append(seg)

    # 新版的屬性是用. 不是舊版的字典 [] 
    srt += f"{i+1}\n"
    srt += f"{format_time(seg.start)} --> {format_time(seg.end)}\n"
    srt += seg.text.strip() + "\n\n"

paragraphs = []
current = []
start_time = None

for seg in all_segments:
    if start_time is None:
        start_time = seg.start

    current.append(seg.text.strip())

    # 每 180 秒切一段
    if seg.end - start_time > 180:
        text = " ".join(current)
        paragraphs.append(f"{format_gemma(start_time)} ||| {text}")
        current = []
        start_time = None

# 最後不足
if current:
    paragraphs.append(f"{format_gemma(start_time)} ||| {' '.join(current)}")

# 存檔
with open("output.srt", "w", encoding="utf-8") as f:
    f.write(srt)

with open("paragraphs.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(paragraphs))

print("done！")