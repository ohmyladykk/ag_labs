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

# --- PyInstaller逕ｨ縺ｮ繝代せ隗｣豎ｺ髢｢謨ｰ ---
def resource_path(relative_path):
    """EXE蛹悶＠縺ｦ繧ら判蜒上ｒ豁｣縺励￥隱ｭ縺ｿ霎ｼ繧縺溘ａ縺ｮ鬲疲ｳ輔・髢｢謨ｰ"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = ctk.CTk()
app.geometry("450x700") # 繝ｭ繧ｴ縺悟・繧句・縲∝ｰ代＠邵ｦ髟ｷ縺ｫ縺励∪縺励◆
app.title("西 Panda Asset Sentinel Pro - 雋ｴ驥大ｱ昿dition")

try:
    app.iconbitmap(resource_path("redpanda_logo.ico"))
except Exception:
    pass

my_font = ("Helvetica", 14)
title_font = ("Helvetica", 18, "bold")
sub_font = ("Helvetica", 12)

# ==========================================
# 西 縺薙％縺九ｉ・√Ο繧ｴ逕ｻ蜒上ｒ荳逡ｪ荳翫↓驟咲ｽｮ縺吶ｋ蜃ｦ逅・# ==========================================
try:
    # 逕ｻ蜒上ヵ繧｡繧､繝ｫ蜷阪ｒ遉ｾ髟ｷ縺ｮ險縺・壹ｊ縲罫edpanda_logo.png縲阪↓螳悟・謖・ｮ夲ｼ・    logo_path = resource_path("redpanda_logo.png")
    logo_img_data = Image.open(logo_path)
    
    # 逕ｻ蜒上・陦ｨ遉ｺ繧ｵ繧､繧ｺ・・00x200縺上ｉ縺・′邯ｺ鮗励〒縺呻ｼ・    logo_image = ctk.CTkImage(light_image=logo_img_data, dark_image=logo_img_data, size=(200, 200))
    
    # 逕ｻ髱｢縺ｮ荳逡ｪ荳翫↓繝峨・繝ｳ縺ｨ驟咲ｽｮ
    logo_label = ctk.CTkLabel(app, image=logo_image, text="")
    logo_label.pack(pady=15)
    
except Exception as e:
    print(f"笞・・逕ｻ蜒剰ｪｭ縺ｿ霎ｼ縺ｿ繧ｨ繝ｩ繝ｼ: {e}")
    # 荳・′荳逕ｻ蜒上′隱ｭ縺ｿ霎ｼ繧√↑縺九▲縺滓凾縺ｮ菫晞匱
    ctk.CTkLabel(app, text="西 Panda Asset Sentinel Pro", font=("Helvetica", 18, "bold")).pack(pady=20)
# ==========================================

input_frame = ctk.CTkFrame(app, fg_color="#2C2C2E", corner_radius=12)
input_frame.pack(pady=5, padx=30, fill="x")

gold_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
gold_frame.pack(fill="x", padx=10, pady=(10, 2))
ctk.CTkLabel(gold_frame, text="荘 驥・(Gold) [g]:", font=my_font).pack(side="left")
gold_entry = ctk.CTkEntry(gold_frame, width=70, justify="right", font=my_font, corner_radius=6)
gold_entry.insert(0, "60")
gold_entry.pack(side="right")

silver_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
silver_frame.pack(fill="x", padx=10, pady=2)
ctk.CTkLabel(silver_frame, text="珍 驫 (Silver) [g]:", font=my_font).pack(side="left")
silver_entry = ctk.CTkEntry(silver_frame, width=70, justify="right", font=my_font, corner_radius=6)
silver_entry.insert(0, "20")
silver_entry.pack(side="right")

plat_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
plat_frame.pack(fill="x", padx=10, pady=2)
ctk.CTkLabel(plat_frame, text="虫 繝励Λ繝√リ (Pt) [g]:", font=my_font).pack(side="left")
plat_entry = ctk.CTkEntry(plat_frame, width=70, justify="right", font=my_font, corner_radius=6)
plat_entry.insert(0, "60")
plat_entry.pack(side="right")

thresh_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
thresh_frame.pack(fill="x", padx=10, pady=(2, 10))
ctk.CTkLabel(thresh_frame, text="悼 證ｴ關ｽ繧｢繝ｩ繝ｼ繝・(%):", font=my_font).pack(side="left")
thresh_entry = ctk.CTkEntry(thresh_frame, width=70, justify="right", font=my_font, text_color="#FF5252", corner_radius=6)
thresh_entry.insert(0, "3.0")
thresh_entry.pack(side="right")

toggle_frame = ctk.CTkFrame(app, fg_color="transparent")
toggle_frame.pack(pady=5, padx=30, fill="x")

notify_switch = ctk.CTkSwitch(toggle_frame, text="繝・せ繧ｯ繝医ャ繝鈴夂衍粕", font=my_font, progress_color="#FF7043", button_hover_color="#D84315", switch_width=35, switch_height=18)
notify_switch.select()
notify_switch.pack(anchor="w", pady=2)

sound_switch = ctk.CTkSwitch(toggle_frame, text="髻ｳ螢ｰ繧｢繝ｩ繝ｼ繝芋沐・, font=my_font, progress_color="#FF7043", button_hover_color="#D84315", switch_width=35, switch_height=18)
sound_switch.select()
sound_switch.pack(anchor="w", pady=2)

# 譁ｰ讖溯・: 繧｢繝ｩ繝ｼ繝磯浹縺ｮ遞ｮ鬘槭ｒ驕ｸ縺ｶ繧ｳ繝ｳ繝懊・繝・け繧ｹ
sound_type_combo = ctk.CTkComboBox(toggle_frame, values=["繧ｵ繧､繝ｬ繝ｳ (螟ｧ髻ｳ驥・", "繧ｷ繧ｹ繝・Β繧ｨ繝ｩ繝ｼ髻ｳ", "髮ｻ蟄宣浹 (繧ｷ繝ｳ繝励Ν)"], font=my_font, width=160, dropdown_font=my_font)
sound_type_combo.set("繧ｵ繧､繝ｬ繝ｳ (螟ｧ髻ｳ驥・")
sound_type_combo.pack(anchor="w", pady=(2, 2), padx=(30, 0))

status_label = ctk.CTkLabel(app, text="迥ｶ諷・ 蛛懈ｭ｢荳ｭ彫", font=my_font, text_color="gray")
status_label.pack(pady=(10, 2))
price_label = ctk.CTkLabel(app, text="[迴ｾ蝨ｨ萓｡譬ｼ] 譛ｪ蜿門ｾ・, font=sub_font)
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
                    val = tds[1].text.replace(',', '').replace('蜀・, '').strip()
                    if val.isdigit():
                        prices[key] = int(val)
        if all(v == 0 for v in prices.values()):
            raise ValueError()
        return prices
    except Exception:
        return None

def play_alert_sound(sound_type):
    try:
        if sound_type == "繧ｵ繧､繝ｬ繝ｳ (螟ｧ髻ｳ驥・":
            for _ in range(4):
                winsound.Beep(1200, 300)
                winsound.Beep(800, 300)
        elif sound_type == "繧ｷ繧ｹ繝・Β繧ｨ繝ｩ繝ｼ髻ｳ":
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
        update_ui(status_label, "誓 逶｣隕紋ｸｭ... (繝ｬ繝・ラ繝代Φ繝蜃ｺ蜍穂ｸｭ・・", "#FF7043")
        
        current_prices = get_tanaka_prices()
        if current_prices:
            price_text = f"荘 驥・ {current_prices['gold']:,}蜀・| 珍 驫: {current_prices['silver']:,}蜀・| 虫 Pt: {current_prices['platinum']:,}蜀・
            update_ui(price_label, price_text)
            
            total_assets = (current_prices['gold'] * gold_g) + (current_prices['silver'] * silver_g) + (current_prices['platinum'] * plat_g)
            print(f"腸 謗ｨ螳夂ｷ剰ｳ・肇: {total_assets:,}蜀・)

            if last_prices:
                for metal in ["gold", "silver", "platinum"]:
                    if last_prices[metal] > 0 and current_prices[metal] > 0:
                        drop_ratio = (last_prices[metal] - current_prices[metal]) / last_prices[metal] * 100
                        if drop_ratio >= threshold:
                            msg = f"圷 {metal.upper()}縺・{drop_ratio:.1f}% 證ｴ關ｽ・―n邱剰ｳ・肇: {total_assets:,}蜀・
                            print(msg)
                            if use_notify:
                                try:
                                    notification.notify(title="Red Panda Sentinel", message=msg, app_name="Sentinel", timeout=10)
                                except: pass
                            if use_sound:
                                # 蛻･繧ｹ繝ｬ繝・ラ縺ｧ髻ｳ繧帝ｳｴ繧峨☆・医Ν繝ｼ繝励ｒ豁｢繧√↑縺・◆繧・ｼ・                                threading.Thread(target=play_alert_sound, args=(sound_type,), daemon=True).start()
                                
            last_prices = current_prices
            update_ui(status_label, f"誓 逶｣隕紋ｸｭ... (邱剰ｳ・肇: {total_assets:,}蜀・", "#00E676")
        else:
            update_ui(status_label, "笞・・萓｡譬ｼ蜿門ｾ励お繝ｩ繝ｼ (蜀崎ｩｦ陦悟ｾ・ｩ滉ｸｭ...)", "#FF5252")
        time.sleep(60)

def start_monitoring():
    try:
        g_val = float(gold_entry.get())
        s_val = float(silver_entry.get())
        p_val = float(plat_entry.get())
        t_val = float(thresh_entry.get())
    except ValueError:
        update_ui(status_label, "笞・・繧ｨ繝ｩ繝ｼ: 謨ｰ蛟､繧貞・繧後※縺上□縺輔＞", "#FF5252")
        return

    use_notify = notify_switch.get() == 1
    use_sound = sound_switch.get() == 1
    sound_type = sound_type_combo.get()

    update_ui(status_label, "誓 逶｣隕悶お繝ｳ繧ｸ繝ｳ襍ｷ蜍穂ｸｭ...", "#00E676")
    start_button.configure(state="disabled", text="噫 繝ｬ繝・ラ繝代Φ繝蜃ｺ蜍穂ｸｭ・・, fg_color="#D84315")
    
    for widget in [gold_entry, silver_entry, plat_entry, thresh_entry, notify_switch, sound_switch, sound_type_combo]:
        widget.configure(state="disabled")
    
    t = threading.Thread(target=monitoring_loop, args=(g_val, s_val, p_val, t_val, use_notify, use_sound, sound_type), daemon=True)
    t.start()

start_button = ctk.CTkButton(
    app, text="誓 逶｣隕悶せ繧ｿ繝ｼ繝茨ｼ・, font=("Helvetica", 15, "bold"), 
    fg_color="#FF5722", hover_color="#E64A19", text_color="white",
    height=40, corner_radius=8, command=start_monitoring
)
start_button.pack(pady=10, padx=30, fill="x")

if __name__ == "__main__":
    app.mainloop()
