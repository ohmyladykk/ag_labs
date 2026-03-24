import customtkinter as ctk
import threading
import time
import requests
from bs4 import BeautifulSoup
from plyer import notification
import winsound
import os
import sys
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# --- PyInstaller用のパス解決関数 ---
def resource_path(relative_path):
    """EXE化しても画像を正しく読み込むための魔法の関数"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = ctk.CTk()
app.geometry("450x700") # ロゴが入る分、少し縦長にしました
app.title("🐼 Panda Asset Sentinel Pro - 貴金属Edition")

try:
    app.iconbitmap(resource_path("redpanda_logo.ico"))
except Exception:
    pass

my_font = ("Helvetica", 14)
title_font = ("Helvetica", 18, "bold")
sub_font = ("Helvetica", 12)

# ==========================================
# 🐼 ここから！ロゴ画像を一番上に配置する処理
# ==========================================
try:
    # 画像ファイル名を社長の言う通り「redpanda_logo.png」に完全指定！
    logo_path = resource_path("redpanda_logo.png")
    logo_img_data = Image.open(logo_path)
    
    # 画像の表示サイズ（200x200くらいが綺麗です）
    logo_image = ctk.CTkImage(light_image=logo_img_data, dark_image=logo_img_data, size=(200, 200))
    
    # 画面の一番上にドーンと配置
    logo_label = ctk.CTkLabel(app, image=logo_image, text="")
    logo_label.pack(pady=15)
    
except Exception as e:
    print(f"⚠️ 画像読み込みエラー: {e}")
    # 万が一画像が読み込めなかった時の保険
    ctk.CTkLabel(app, text="🐼 Panda Asset Sentinel Pro", font=("Helvetica", 18, "bold")).pack(pady=20)
# ==========================================

input_frame = ctk.CTkFrame(app, fg_color="#2C2C2E", corner_radius=12)
input_frame.pack(pady=5, padx=30, fill="x")

gold_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
gold_frame.pack(fill="x", padx=10, pady=(10, 2))
ctk.CTkLabel(gold_frame, text="🟨 金 (Gold) [g]:", font=my_font).pack(side="left")
gold_entry = ctk.CTkEntry(gold_frame, width=70, justify="right", font=my_font, corner_radius=6)
gold_entry.insert(0, "60")
gold_entry.pack(side="right")

silver_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
silver_frame.pack(fill="x", padx=10, pady=2)
ctk.CTkLabel(silver_frame, text="🪙 銀 (Silver) [g]:", font=my_font).pack(side="left")
silver_entry = ctk.CTkEntry(silver_frame, width=70, justify="right", font=my_font, corner_radius=6)
silver_entry.insert(0, "20")
silver_entry.pack(side="right")

plat_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
plat_frame.pack(fill="x", padx=10, pady=2)
ctk.CTkLabel(plat_frame, text="⚙ プラチナ (Pt) [g]:", font=my_font).pack(side="left")
plat_entry = ctk.CTkEntry(plat_frame, width=70, justify="right", font=my_font, corner_radius=6)
plat_entry.insert(0, "60")
plat_entry.pack(side="right")

thresh_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
thresh_frame.pack(fill="x", padx=10, pady=(2, 10))
ctk.CTkLabel(thresh_frame, text="🚨 暴落アラート (%):", font=my_font).pack(side="left")
thresh_entry = ctk.CTkEntry(thresh_frame, width=70, justify="right", font=my_font, text_color="#FF5252", corner_radius=6)
thresh_entry.insert(0, "3.0")
thresh_entry.pack(side="right")

toggle_frame = ctk.CTkFrame(app, fg_color="transparent")
toggle_frame.pack(pady=5, padx=30, fill="x")

notify_switch = ctk.CTkSwitch(toggle_frame, text="デスクトップ通知📢", font=my_font, progress_color="#FF7043", button_hover_color="#D84315", switch_width=35, switch_height=18)
notify_switch.select()
notify_switch.pack(anchor="w", pady=2)

sound_switch = ctk.CTkSwitch(toggle_frame, text="音声アラート🔊", font=my_font, progress_color="#FF7043", button_hover_color="#D84315", switch_width=35, switch_height=18)
sound_switch.select()
sound_switch.pack(anchor="w", pady=2)

# 新機能: アラート音の種類を選ぶコンボボックス
sound_type_combo = ctk.CTkComboBox(toggle_frame, values=["サイレン (大音量)", "システムエラー音", "電子音 (シンプル)"], font=my_font, width=160, dropdown_font=my_font)
sound_type_combo.set("サイレン (大音量)")
sound_type_combo.pack(anchor="w", pady=(2, 2), padx=(30, 0))

status_label = ctk.CTkLabel(app, text="状態: 停止中🐾", font=my_font, text_color="gray")
status_label.pack(pady=(10, 2))
price_label = ctk.CTkLabel(app, text="[現在価格] 未取得", font=sub_font)
price_label.pack(pady=0)

def update_ui(label_widget, new_text, new_color=None):
    if new_color:
        app.after(0, lambda: label_widget.configure(text=new_text, text_color=new_color))
    else:
        app.after(0, lambda: label_widget.configure(text=new_text))

def get_tanaka_prices():
    url = "https://gold.tanaka.co.jp/commodity/souba/d-gold.php"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        prices = {"gold": 0, "silver": 0, "platinum": 0}
        for class_name, key in [('gold', 'gold'), ('silver', 'silver'), ('platinum', 'platinum')]:
            tr = soup.find('tr', class_=class_name)
            if tr:
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    val = tds[1].text.replace(',', '').replace('円', '').strip()
                    if val.isdigit():
                        prices[key] = int(val)
        if all(v == 0 for v in prices.values()):
            raise ValueError()
        return prices
    except Exception:
        return None

def play_alert_sound(sound_type):
    try:
        if sound_type == "サイレン (大音量)":
            for _ in range(4):
                winsound.Beep(1200, 300)
                winsound.Beep(800, 300)
        elif sound_type == "システムエラー音":
            for _ in range(3):
                winsound.MessageBeep(winsound.MB_ICONHAND)
                time.sleep(0.5)
        else:
            for _ in range(3):
                winsound.Beep(1500, 400)
                time.sleep(0.1)
    except Exception as e:
        print(f"Sound error: {e}")

def monitoring_loop(gold_g, silver_g, plat_g, threshold, use_notify, use_sound, sound_type):
    last_prices = None
    while True:
        update_ui(status_label, "⏳ 監視中... (レッドパンダ出動中🐾)", "#FF7043")
        
        current_prices = get_tanaka_prices()
        if current_prices:
            price_text = f"🟨 金: {current_prices['gold']:,}円 | 🪙 銀: {current_prices['silver']:,}円 | ⚙ Pt: {current_prices['platinum']:,}円"
            update_ui(price_label, price_text)
            
            total_assets = (current_prices['gold'] * gold_g) + (current_prices['silver'] * silver_g) + (current_prices['platinum'] * plat_g)
            print(f"💰 推定総資産: {total_assets:,}円")

            if last_prices:
                for metal in ["gold", "silver", "platinum"]:
                    if last_prices[metal] > 0 and current_prices[metal] > 0:
                        drop_ratio = (last_prices[metal] - current_prices[metal]) / last_prices[metal] * 100
                        if drop_ratio >= threshold:
                            msg = f"📉 {metal.upper()}が {drop_ratio:.1f}% 暴落！\n総資産: {total_assets:,}円"
                            print(msg)
                            if use_notify:
                                try:
                                    notification.notify(title="Red Panda Sentinel", message=msg, app_name="Sentinel", timeout=10)
                                except: pass
                            if use_sound:
                                # 別スレッドで音を鳴らす（ループを止めないため）
                                threading.Thread(target=play_alert_sound, args=(sound_type,), daemon=True).start()
                                
            last_prices = current_prices
            update_ui(status_label, f"⏳ 監視中... (総資産: {total_assets:,}円)", "#00E676")
        else:
            update_ui(status_label, "⚠️ 価格取得エラー (再試行待機中...)", "#FF5252")
        time.sleep(60)

def start_monitoring():
    try:
        g_val = float(gold_entry.get())
        s_val = float(silver_entry.get())
        p_val = float(plat_entry.get())
        t_val = float(thresh_entry.get())
    except ValueError:
        update_ui(status_label, "⚠️ エラー: 数値を入力してください", "#FF5252")
        return

    use_notify = notify_switch.get() == 1
    use_sound = sound_switch.get() == 1
    sound_type = sound_type_combo.get()

    update_ui(status_label, "⏳ 監視エンジン起動中...", "#00E676")
    start_button.configure(state="disabled", text="🚨 監視開始済み🐾", fg_color="#D84315")
    
    for widget in [gold_entry, silver_entry, plat_entry, thresh_entry, notify_switch, sound_switch, sound_type_combo]:
        widget.configure(state="disabled")
    
    t = threading.Thread(target=monitoring_loop, args=(g_val, s_val, p_val, t_val, use_notify, use_sound, sound_type), daemon=True)
    t.start()

start_button = ctk.CTkButton(
    app, text="🚀 監視スタート！", font=("Helvetica", 15, "bold"), 
    fg_color="#FF5722", hover_color="#E64A19", text_color="white",
    height=40, corner_radius=8, command=start_monitoring
)
start_button.pack(pady=10, padx=30, fill="x")

def _fetch_initial_price():
    update_ui(status_label, "状態: 初期価格を取得中...🐾", "gray")
    prices = get_tanaka_prices()
    if prices:
        price_text = f"🟨 金: {prices['gold']:,}円 | 🪙 銀: {prices['silver']:,}円 | ⚙ Pt: {prices['platinum']:,}円"
        update_ui(price_label, price_text)
        update_ui(status_label, "状態: 停止中🐾 (初期価格 取得完了)", "gray")
    else:
        update_ui(price_label, "[現在価格] 初期取得に失敗しました")
        update_ui(status_label, "状態: 停止中🐾", "gray")

threading.Thread(target=_fetch_initial_price, daemon=True).start()

if __name__ == "__main__":
    app.mainloop()
