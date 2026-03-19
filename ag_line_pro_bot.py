import requests
import datetime

def send_line_pro():
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer J8jrevSQ635scMz51eW9jl1iinREh47n6FA5QB2NSPiVurZnr8bO4iirpOKUa658gJY8woe81LpsyVZsPJ3BXWNMA0GzlIZkghw8aTdINQZozIOgopxJOHdOAxAKGNyUOCoTe+fvT+qWg5l0/gOhdwdB04t89/1O/w1cDnyilFU="
    }
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    msg = f"🌅 おはようございます、社長！\nAG Labs システム正常稼働中。\n現在時刻: {now}"
    
    data = {
        "to": "U16e74422b2564c0ad8f98149c146e976",
        "messages": [{
            "type": "text",
            "text": msg
        }]
    }
    
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        print("✅ LINE本家APIからの送信成功！スマホを確認してください！")
    else:
        print(f"⚠️ エラー: {res.status_code} - {res.text}")

if __name__ == "__main__":
    send_line_pro()
