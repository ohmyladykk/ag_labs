import requests
import datetime
import os

def send_line():
    url = "https://notify-api.line.me/api/notify"
    
    # 環境変数からトークンを取得（GitHub Secretsで設定）
    token = os.environ.get("LINE_NOTIFY_TOKEN")
    if not token:
        print("エラー: LINE_NOTIFY_TOKEN の環境変数が設定されていません。")
        return

    headers = {"Authorization": f"Bearer {token}"}
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    msg = f"\n【勤怠連絡】\nおはようございます。本日は在宅勤務(テレワーク)にて業務を開始いたします。\n現在時刻: {now}\nよろしくお願いいたします。"
    
    try:
        response = requests.post(url, headers=headers, data={"message": msg})
        response.raise_for_status()
        print("LINE notification sent successfully.")
    except Exception as e:
        print(f"Failed to send LINE notification: {e}")

if __name__ == "__main__":
    send_line()
