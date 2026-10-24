# yt-subtitle-timeline-generator
An automated YouTube workflow that downloads audio, generates subtitles with Whisper, and creates timelines using local LLM.

# YouTube 影片轉字幕與 AI 時間軸生成工具
這個是一個利用 Python 寫的自動化工具。只要給它 YouTube 影片網址，就能自動下載音訊、用 Whisper 轉出字幕，最後用本機的 AI 模型生出影片的時間軸章節。

## 檔案說明
- video_to_text.py：負責從 YouTube 下載音訊，呼叫 Whisper 進行辨識，並產生字幕檔與用於ＡＩ生成時間軸的段落文字。
- text_to_timeline.py：負責讀取段落文字，串接本機的 Ollama，自動算出 YouTube 時間軸標題。

## 環境準備
1. 電腦需要先安裝：
   - FFmpeg（音訊解碼）
   - Ollama（模型不拘，但自己用下來llama會比gemma好用）

2. 需要安裝的 Python 套件：
   - yt-dlp (抓取yt音訊)
   - faster-whisper或openai-whisper(分析語音)
   - ollama（呼叫ollama）
   - setuptools

## 使用方法
步驟一：生成逐字稿與段落
打開 video_to_text.py，將裡面的 url 修改為你想要影片的 YouTube 網址，並將產生時間軸的間隔修改好後執行程式。完成後會產生 output.srt 與 paragraphs.txt。

步驟二：AI 生成 YouTube 影片章節
確認本機 Ollama 有啟動後，接著執行 text_to_timeline.py。他會自動讀取前一步的檔案，並產出時間軸檔案 timeline.txt。

備註：上有提供用 fast-whisper 以及原版 whisper 寫的兩個版本，我在專案裡有分開寫成不同的檔案上傳。
