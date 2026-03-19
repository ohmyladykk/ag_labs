import requests
import datetime

def send_line():
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer J8jrevSQ635scMz51eW9jl1iinREh47n6FA5QB2NSPiVurZnr8bO4iirpOKUa658gJY8woe81LpsyVZsPJ3BXWNMA0GzlIZkghw8aTdINQZozIOgopxJOHdOAxAKGNyUOCoTe+fvT+qWg5l0/gOhdwdB04t89/1O/w1cDnyilFU="}
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    msg = f"\nおはようございます、社長！\nAG Labs システム正常稼働中。\n現在時刻: {now}"
    requests.post(url, headers=headers, data={"message": msg})

if __name__ == "__main__":
    send_line()
