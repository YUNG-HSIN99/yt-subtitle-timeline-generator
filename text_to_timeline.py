with open("paragraphs.txt", "r", encoding="utf-8") as f:
    paragraphs = [line.strip() for line in f.read().split('\n') if line.strip()]

timeline_results = []

import re
from ollama import chat

for i, block in enumerate(paragraphs):
    if not block.strip() or " ||| " not in block:
        continue
    # 用 ||| 把時間戳 文字拆開
    time_tag, pure_content = block.split(" ||| ")
    
    print(f"   正在分析章節 [{time_tag}] ({i+1}/{len(paragraphs)})...")
    
    # ＡＩ分析
    response = chat(
        model="llama3.2:3b", 
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text into a single concise YouTube chapter title in English (MAXIMUM 10 words). Do not include any timestamps, markdown, or punctuation.\n\nContent:\n{pure_content}"
            }
        ],
        options={"num_predict": 50, "temperature": 0.1}
    )
    
    ai_title = response["message"].content.strip()
    if not ai_title:
        ai_title = response["message"].thinking.strip()

    # 調格式
    clean_title = re.sub(r'["\'「」『』《》]', '', ai_title).replace('\n', ' ').strip()

    # 抓前 10 個
    clean_title = " ".join(clean_title.split()[:10])

    # 黏回去
    final_line = f"{time_tag} {clean_title}"
    timeline_results.append(final_line)

# 存檔
with open("timeline.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(timeline_results))