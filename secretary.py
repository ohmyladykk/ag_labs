import os
import time
import requests
import urllib.parse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
import schedule
import sys
import io

# Windowsコンソールの絵文字エンコードエラー（cp932警告）対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 1. LINE設定
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN", "")
LINE_API_URL = "https://api.line.me/v2/bot/message/broadcast" 

def send_line_message_text(text: str):
    """LINEにテキストメッセージを直接送信する共通関数"""
    if not LINE_ACCESS_TOKEN:
        print("💡 [TEST-MODE] LINE_ACCESS_TOKEN が設定されていません。通知はスキップされます。")
        print("📩 送信内容:\n", text)
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "messages": [
            {"type": "text", "text": text}
        ]
    }
    
    try:
        response = requests.post(LINE_API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ 秘書：LINEへの通知が成功しました！")
        else:
            print(f"⚠️ 秘書：エラーが発生しました... {response.text}")
    except Exception as e:
        print("❌ 秘書：LINEへの通信で例外が発生:", e)

def send_line_error_message(msg: str):
    """【エラー報告ルール】スクレイピング失敗時にLINEへ即時エラー通知を行う。"""
    print(f"🚨 {msg}")
    send_line_message_text(msg)

def is_remote_job(title, company=""):
    text = (title + " " + company).lower()
    return any(kw in text for kw in ["在宅", "リモート", "remote", "テレワーク", "wfh"])

def fetch_kyujinbox(keyword, location, limit=5):
    jobs = []
    keyword_enc = urllib.parse.quote(keyword)
    location_enc = urllib.parse.quote(location)
    url = f"https://xn--pckua2a7gp15o89zb.com/?form%5Bkeyword%5D={keyword_enc}&form%5Bplace%5D={location_enc}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        items = soup.find_all('section')
        for item in items:
            title_elem = item.find('h2')
            if not title_elem: continue
            
            title = title_elem.text.strip()
            if "求人を" in title or "メリット" in title or "きっかけに" in title or "ピックアップ" in title or "ランキング" in title or "全国のお仕事" in title:
                continue
                
            link_elem = item.find('a', href=True)
            if not link_elem: continue
            href = link_elem.get('href', '')
            
            if not href or href == '#' or href.startswith('javascript'):
                continue
                
            company_elem = item.select_one('[class*="company"]')
            company = company_elem.text.strip() if company_elem else "会社名非公開"
            link = "https://xn--pckua2a7gp15o89zb.com" + href if href.startswith('/') else href
            
            if not is_remote_job(title, company): continue
            
            jobs.append({
                "title": title[:35],
                "company": company[:20],
                "url": link,
                "location": location,
                "source": "求人ボックス"
            })
            if len(jobs) >= limit: break
                
    except Exception as e:
        send_line_error_message(f"社長、[{location}]の求人ボックスの読み込みでエラーが発生しました🐾\n詳細: {type(e).__name__}")
            
    return jobs[:limit]

def fetch_stanby(keyword, location, limit=5):
    jobs = []
    keyword_enc = urllib.parse.quote(keyword)
    location_enc = urllib.parse.quote(location)
    url = f"https://jp.stanby.com/search?q={keyword_enc}&l={location_enc}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        items = soup.find_all('article')
        for item in items:
            title_elem = item.find('h2') or item.find('h3') or item.find('a', class_='title')
            if not title_elem: continue
            
            company_elem = item.select_one('.company-name, .company, .name')
            company = company_elem.text.strip() if company_elem else "会社名非公開"
            
            link_elem = item.find('a', href=True)
            if not link_elem: continue
            href = link_elem.get('href', '')
            
            if not href or href == '#' or href.startswith('javascript'):
                continue
            
            link = "https://jp.stanby.com" + href if href.startswith('/') else href
            if not link.startswith('http'): link = "https://jp.stanby.com/" + link
                
            title = title_elem.text.strip()
            if not is_remote_job(title, company): continue
            
            jobs.append({
                "title": title[:35],
                "company": company[:20],
                "url": link,
                "location": location,
                "source": "スタンバイ"
            })
            if len(jobs) >= limit: break
    except Exception as e:
        send_line_error_message(f"社長、[{location}]のスタンバイの読み込みでエラーが発生しました🐾\n詳細: {type(e).__name__}")
            
    return jobs[:limit]

def fetch_yahoo(keyword, location, limit=5):
    jobs = []
    keyword_enc = urllib.parse.quote(keyword)
    location_enc = urllib.parse.quote(location)
    url = f"https://job.yahoo.co.jp/search/?q={keyword_enc}&p={location_enc}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        items = soup.find_all('article')
        for item in items:
            title_elem = item.find('h2') or item.find('h3') or item.select_one('.JobListItem__Title')
            if not title_elem: continue
            
            company_elem = item.select_one('.JobListItem__Company, .company, [class*="company"]')
            company = company_elem.text.strip() if company_elem else "会社名非公開"
            
            link_elem = item.find('a', href=True)
            if not link_elem: continue
            href = link_elem.get('href', '')
            
            if not href or href == '#' or href.startswith('javascript'):
                continue
            
            link = href if href.startswith('http') else "https://job.yahoo.co.jp" + href
            if not link.startswith('http'): link = "https://job.yahoo.co.jp/" + link
                
            title = title_elem.text.strip()
            if not is_remote_job(title, company): continue
            
            jobs.append({
                "title": title[:35],
                "company": company[:20],
                "url": link,
                "location": location,
                "source": "Yahoo!しごと"
            })
            if len(jobs) >= limit: break
    except Exception as e:
        send_line_error_message(f"社長、[{location}]のYahoo!しごとの読み込みでエラーが発生しました🐾\n詳細: {type(e).__name__}")
            
    return jobs[:limit]

def fetch_indeed(keyword, location, limit=10):
    jobs = []
    keyword_enc = urllib.parse.quote(keyword)
    location_enc = urllib.parse.quote(location)
    url = f"https://jp.indeed.com/jobs?q={keyword_enc}&l={location_enc}"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page.goto(url, timeout=15000)
            page.wait_for_timeout(2000)
            
            elements = page.locator('.job_seen_beacon').all()
            for el in elements:
                title_el = el.locator('h2, .jobTitle').first
                title = title_el.inner_text().strip() if title_el else ""
                
                company_el = el.locator('.companyName, [data-testid="company-name"]').first
                company = company_el.inner_text().strip() if company_el else "会社名非公開"
                
                href = ""
                a_tag = el.locator('a').first
                if a_tag:
                    href = a_tag.get_attribute("href") or ""
                
                link = "https://jp.indeed.com" + href if href.startswith('/') else (href or url)
                
                if title and is_remote_job(title, company):
                    jobs.append({
                        "title": title[:35],
                        "company": company[:20],
                        "url": link,
                        "location": location,
                        "source": "Indeed"
                    })
                if len(jobs) >= limit: break
            browser.close()
    except Exception as e:
        send_line_error_message(f"社長、[{location}]のIndeedの読み込みでエラーが発生しました🐾\n詳細: {type(e).__name__}")
            
    return jobs[:limit]

def fetch_enhaken(keyword, location, limit=10):
    jobs = []
    area = "tokyo" if "東京" in location else "kanagawa" if "横浜" in location else "kanto"
    url = f"https://haken.en-japan.com/zaitaku/{area}/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        items = soup.find_all('div', class_=lambda c: c and 'jobItem' in c)
        if not items:
            for a in soup.find_all('a', href=True):
                h_tags = a.find_all(['h2', 'h3'])
                if h_tags:
                    title = h_tags[0].text.strip()
                    if len(title) > 5 and is_remote_job(title):
                        href = a['href']
                        link = "https://haken.en-japan.com" + href if href.startswith('/') else href
                        jobs.append({
                            "title": title[:35],
                            "company": "エン派遣 提供",
                            "url": link,
                            "location": location,
                            "source": "en haken"
                        })
                if len(jobs) >= limit: break
    except Exception as e:
        send_line_error_message(f"社長、[{location}]のエン派遣の読み込みでエラーが発生しました🐾\n詳細: {type(e).__name__}")
            
    return jobs[:limit]

def fetch_rikunabi(keyword, location, limit=10):
    jobs = []
    keyword_enc = urllib.parse.quote(f"{keyword} {location}")
    url = f"https://next.rikunabi.com/job_search/kw/{keyword_enc}/"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page.goto(url, timeout=15000)
            page.wait_for_timeout(2000)
            
            elements = page.locator('li.rnn-jobOfferList__item').all()
            if not elements:
                elements = page.locator('h2, h3').all()
                for el in elements:
                    title = el.inner_text().strip()
                    if len(title) > 5 and len(jobs) < limit and is_remote_job(title):
                        a_tag = el.locator('xpath=..//a').first
                        href = url
                        if a_tag:
                            href = a_tag.get_attribute("href") or url
                        link = "https://next.rikunabi.com" + href if href.startswith('/') else href
                        jobs.append({
                            "title": title[:35],
                            "company": "リクナビNEXT 提供",
                            "url": link,
                            "location": location,
                            "source": "リクナビ"
                        })
            else:
                for el in elements:
                    title_el = el.locator('h2, h3').first
                    title = title_el.inner_text().strip() if title_el else ""
                    
                    company_el = el.locator('.rnn-jobOfferList__item__company').first
                    company = company_el.inner_text().strip() if company_el else "会社名非公開"
                    
                    a_tag = el.locator('a').first
                    href = url
                    if a_tag:
                        href = a_tag.get_attribute("href") or url
                    
                    link = "https://next.rikunabi.com" + href if href.startswith('/') else href
                    
                    if title and is_remote_job(title, company):
                        jobs.append({
                            "title": title[:35],
                            "company": company[:20],
                            "url": link,
                            "location": location,
                            "source": "リクナビ"
                        })
                    if len(jobs) >= limit: break
            browser.close()
    except Exception as e:
        send_line_error_message(f"社長、[{location}]のリクナビの読み込みでエラーが発生しました🐾\n詳細: {type(e).__name__}")
            
    return jobs[:limit]

def fetch_hatarako(keyword, location, limit=10):
    jobs = []
    area = "tokyo" if "東京" in location else "kanagawa" if "横浜" in location else "kanto"
    url = f"https://www.hatarako.net/{area}/kdw86/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for a in soup.find_all('a', href=True):
            h_tags = a.find_all(['h2', 'h3'])
            if h_tags:
                title = h_tags[0].text.strip()
                if len(title) > 5 and 'を検索' not in title and is_remote_job(title):
                    href = a.get('href', url)
                    link = "https://www.hatarako.net" + href if href.startswith('/') else href
                    jobs.append({
                        "title": title[:35],
                        "company": "はたらこねっと 提供",
                        "url": link,
                        "location": location,
                        "source": "はたらこねっと"
                    })
            if len(jobs) >= limit: break
    except Exception as e:
        send_line_error_message(f"社長、[{location}]のはたらこねっとの読み込みでエラーが発生しました🐾\n詳細: {type(e).__name__}")
            
    return jobs[:limit]

def fetch_wwr_rss(limit=5):
    jobs = []
    url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        root = ET.fromstring(r.text)
        
        for item in root.findall('./channel/item')[:limit]:
            title = item.find('title').text
            link = item.find('link').text
            
            company = "We Work Remotely"
            if ":" in title:
                parts = title.split(":", 1)
                company = parts[0].strip()
                title = parts[1].strip()
                
            jobs.append({
                "title": title,
                "company": company,
                "url": link,
                "location": "海外/Remote",
                "source": "We Work Remotely"
            })
    except Exception as e:
        send_line_error_message(f"社長、[海外]のWe Work Remotelyの読み込みでエラーが発生しました🐾\n詳細: {type(e).__name__}")
        
    return jobs

def get_job_info():
    print("秘書：実際の求人サイトから情報を取得中...")
    jobs = []
    
    print("- 東京の案件を取得中...")
    jobs.extend(fetch_kyujinbox("在宅ワーク", "東京", 3))
    jobs.extend(fetch_stanby("在宅ワーク", "東京", 5))
    jobs.extend(fetch_indeed("在宅ワーク", "東京", 5))
    jobs.extend(fetch_enhaken("在宅ワーク", "東京", 5))
    jobs.extend(fetch_rikunabi("在宅ワーク", "東京", 5))
    jobs.extend(fetch_hatarako("在宅ワーク", "東京", 5))
    
    print("- 横浜の案件を取得中...")
    jobs.extend(fetch_kyujinbox("在宅ワーク", "横浜", 2))
    jobs.extend(fetch_stanby("在宅ワーク", "横浜", 5))
    jobs.extend(fetch_indeed("在宅ワーク", "横浜", 5))
    jobs.extend(fetch_enhaken("在宅ワーク", "横浜", 5))
    jobs.extend(fetch_rikunabi("在宅ワーク", "横浜", 5))
    jobs.extend(fetch_hatarako("在宅ワーク", "横浜", 5))
    
    print("- 海外の案件を取得中...")
    jobs.extend(fetch_wwr_rss(10))
    
    return jobs

def execute_daily_task():
    """日次のスケジュール実行タスク本体"""
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 日次タスク開始...")
    try:
        jobs = get_job_info()
        
        # 【絶対通知ルール】該当求人が0件だった場合の処理
        if not jobs:
            send_line_message_text("おはようございます！今日の条件に合う新着求人は0件でした🐾")
            print("本日の求人は0件のため、0件報告をLINEに送信しました。")
            return
            
        message_text = "🌸 おはようございます 🌸\n本日の【在宅ワーク＆海外リモート】求人情報をお届けします💌✨\n\n"
        for job in jobs:
            location_tag = f"【{job.get('location', '')}】"
            source_tag = f"[{job.get('source', '')}]"
            message_text += f"{location_tag} {source_tag}\n🏢 {job['company']}\n📌 {job['title']}\n🔗 {job['url']}\n・ー・ー・ー・ー・ー・ー・\n"
            
        message_text += "\n今日も素敵な1日になりますように！☕🍀"
        send_line_message_text(message_text)
        print("本日の求人報告をLINEに送信しました。")
        
    except Exception as e:
        send_line_error_message(f"社長、スクリプトの実行中に予期せぬエラーが発生しました🐾\n{e}")

if __name__ == "__main__":
    print("🤖 秘書ボット起動：24時間稼働モード（毎日 07:00 実行）")
    
    # 毎日7:00と12:00にスクレイピング＆通知を実行するようスケジュール
    schedule.every().day.at("07:00").do(execute_daily_task)
    schedule.every().day.at("12:00").do(execute_daily_task)
    
    # 無限ループでずっと起き続けてスケジュールを待機する
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except KeyboardInterrupt:
            print("手動でプログラムが停止されました。終了します。")
            break
        except Exception as e:
            # while Trueのループが例外で落ちることを防ぐ【常駐スケジュール機能の実装】
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] メインループ内でクリティカルエラー発生:", e)
            time.sleep(60)
