import os

print("========================================")
print(" 👑 Antigravity 自動構築システム (LINE Pro版) 起動")
print("========================================")

# ① 社長に「トークン」と「ユーザーID」の2つを聞く！
token = input("J8jrevSQ635scMz51eW9jl1iinREh47n6FA5QB2NSPiVurZnr8bO4iirpOKUa658gJY8woe81LpsyVZsPJ3BXWNMA0GzlIZkghw8aTdINQZozIOgopxJOHdOAxAKGNyUOCoTe+fvT+qWg5l0/gOhdwdB04t89/1O/w1cDnyilFU= ")
user_id = input("U16e74422b2564c0ad8f98149c146e976 ")

# ② Antigravityが「LINE本家APIプログラム」を自動で書き上げる
bot_code = f"""import requests
import datetime

def send_line_pro():
    url = "https://api.line.me/v2/bot/message/push"
    headers = {{
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}"
    }}
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    msg = f"🌅 おはようございます、社長！\\nAG Labs システム正常稼働中。\\n現在時刻: {{now}}"
    
    data = {{
        "to": "{user_id}",
        "messages": [{{
            "type": "text",
            "text": msg
        }}]
    }}
    
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ LINE本家APIからの送信成功！スマホを確認してください！")
    else:
        print(f"⚠️ エラー: {{res.status_code}} - {{res.text}}")

if __name__ == "__main__":
    send_line_pro()
"""

# ファイルとして保存する（名前も pro に変わります）
bot_path = r"C:\ag_labs\ag_line_pro_bot.py"
with open(bot_path, "w", encoding="utf-8") as f:
    f.write(bot_code)
print(f"\n✅ 1/2: 本家LINE送信用プログラム ({bot_path}) を自動生成しました！")

# ③ Windowsのタスクスケジューラに強制登録（古い設定を上書き）
print("⏳ 2/2: Windowsに毎朝7時のタイマーを仕込んでいます...")
setup_cmd = f'schtasks /create /tn "AG_Morning_Report" /tr "python {bot_path}" /sc daily /st 07:00 /f'
os.system(setup_cmd)

print("\n🎉 【構築完了】すべてAntigravityが設定しました！")