import customtkinter as ctk
import threading
import time
import math

# 🎨 कलर्स और थीम सेटअप (SEON डार्क नियॉन प्रीमियम लुक)
ctk.set_appearance_mode("Dark")
DARK_BG = "#0B0B0C"
CARD_BG = "#141416"
SEON_PINK = "#FF3366"  # ब्रैंड पिंक
NEON_GREEN = "#00FF66" # नियॉन ग्रीन

app = ctk.CTk()
app.title("SEON Ultra - गौरव भाई का वीआईपी ऐप")
app.geometry("520x740")
app.configure(fg_color=DARK_BG)

user_credentials = {"gaurav": "1234"}
cart = {}
products = [
    {"name": "🥛 अमूल ताज़ा दूध (1L)", "price": 66},
    {"name": "🍞 ब्रिटानिया सैंडविच ब्रेड", "price": 50},
    {"name": "🥔 ताज़े आलू (1KG)", "price": 30},
    {"name": "🍎 कश्मीरी सेब (1KG)", "price": 180},
    {"name": "🥤 कोका कोला (750ml)", "price": 45},
    {"name": "🍫 कैडबरी सिल्क", "price": 80}
]

# ==================== 📱 UI LAYOUT LAYERS ====================

# बाहरी रंग-बिरंगा बॉर्डर फ्रेम (Edge Light)
edge_border = ctk.CTkFrame(app, fg_color=SEON_PINK, corner_radius=18)
edge_border.pack(fill="both", expand=True, padx=10, pady=10)

# अंदर का मुख्य कंटेनर जो बॉर्डर के ऊपर रहेगा
inner_container = ctk.CTkFrame(edge_border, fg_color=DARK_BG, corner_radius=16)
inner_container.pack(fill="both", expand=True, padx=4, pady=4)


# ==================== 🏪 1. LOGIN SCREEN CONTAINER ====================
login_frame = ctk.CTkFrame(inner_container, fg_color=CARD_BG, corner_radius=15)

login_title = ctk.CTkLabel(login_frame, text="⚡ SEON", font=("Arial", 50, "bold"), text_color=SEON_PINK)
login_title.pack(pady=(80, 10))

login_subtitle = ctk.CTkLabel(login_frame, text="EDGE LIGHTING PREMIUM EDITION", font=("Arial", 12), text_color="#666666")
login_subtitle.pack(pady=(0, 40))

login_user_entry = ctk.CTkEntry(login_frame, placeholder_text="यूज़रनेम (gaurav)", width=320, height=45, fg_color="#1A1A1A", border_color="#333333")
login_user_entry.pack(pady=10)

login_pass_entry = ctk.CTkEntry(login_frame, placeholder_text="पासवर्ड (1234)", show="*", width=320, height=45, fg_color="#1A1A1A", border_color="#333333")
login_pass_entry.pack(pady=10)

login_status = ctk.CTkLabel(login_frame, text="", font=("Arial", 13))
login_status.pack(pady=5)


# ==================== 🛒 2. MAIN STORE SCREEN CONTAINER ====================
main_app_frame = ctk.CTkFrame(inner_container, fg_color=DARK_BG)

top_bar = ctk.CTkFrame(main_app_frame, fg_color="transparent")
top_bar.pack(fill="x", pady=10)

welcome_label = ctk.CTkLabel(top_bar, text="", font=("Arial", 16, "bold"), text_color=NEON_GREEN)
welcome_label.pack(side="left", padx=10)


# ==================== ⚙️ FUNCTIONS & LOGIC ====================

def show_frame(frame_to_show):
    login_frame.pack_forget()
    main_app_frame.pack_forget()
    frame_to_show.pack(fill="both", expand=True, padx=4, pady=4)

def login_user():
    username = login_user_entry.get().strip()
    password = login_pass_entry.get().strip()
    if username in user_credentials and user_credentials[username] == password:
        welcome_label.configure(text=f"👑 SEON VIP STORE: {username.upper()} BHAI")
        show_frame(main_app_frame)
    else:
        login_status.configure(text="❌ गलत पासवर्ड भाई!", text_color=SEON_PINK)

# लॉगिन बटन का कमांड फंक्शन के नीचे होना ज़रूरी है
login_btn = ctk.CTkButton(login_frame, text="🔓 स्टोर में घुसें", font=("Arial", 16, "bold"), fg_color=SEON_PINK, hover_color="#CC0033", width=320, height=45, command=login_user)
login_btn.pack(pady=15)

def run_edge_lighting():
    angle = 0
    while True:
        try:
            r = int((math.sin(angle) + 1) * 127.5)
            g = int((math.sin(angle + 2) + 1) * 127.5)
            b = int((math.sin(angle + 4) + 1) * 127.5)
            current_color = f"#{r:02x}{g:02x}{b:02x}"
            edge_border.configure(fg_color=current_color)
            angle += 0.05
            time.sleep(0.02)
        except:
            break

def run_samsung_progress(msg, duration=1.0):
    progress_frame.pack(fill="x", padx=20, pady=5, before=cart_frame)
    progress_text.configure(text=f"⚡ {msg}")
    steps = 20
    sleep_time = duration / steps
    for i in range(steps + 1):
        progress_bar.set(i / steps)
        time.sleep(sleep_time)
    progress_frame.pack_forget()

def add_to_cart(name, price):
    if name in cart:
        cart[name]['qty'] += 1
    else:
        cart[name] = {'price': price, 'qty': 1}
    update_cart_display()
    threading.Thread(target=run_samsung_progress, args=("आइटम सिंक हो रहा है...", 0.6)).start()

def update_cart_display():
    cart_text = ""
    total_bill = 0
    for name, info in cart.items():
        subtotal = info['price'] * info['qty']
        total_bill += subtotal
        cart_text += f" {name} x {info['qty']} = ₹{subtotal}\n"
    if not cart_text: 
        cart_text = " आपकी कार्ट खाली है भाई! कुछ ऐड करो..."
    cart_items_label.configure(text=cart_text)
    total_bill_label.configure(text=f"💰 कुल बिल: ₹{total_bill}")

def checkout():
    if not cart: return
    def target():
        run_samsung_progress("ऑर्डर प्रोसेस हो रहा है...", 1.5)
        cart.clear()
        update_cart_display()
        threading.Thread(target=run_samsung_progress, args=("🎉 ऑर्डर पक्का! 10 मिनट में घर पहुँचेगा!", 2.0)).start()
    threading.Thread(target=target).start()


# ==================== 🛒 MAIN STORE SCREEN CONTENTS ====================

logout_btn = ctk.CTkButton(top_bar, text="🚪 Log Out", font=("Arial", 11), fg_color="#1A1A1A", hover_color="#333333", width=70, height=25, command=lambda: show_frame(login_frame))
logout_btn.pack(side="right", padx=10)

prod_scroll_frame = ctk.CTkScrollableFrame(main_app_frame, width=440, height=240, label_text="🍉 SEON सुपरफास्ट स्टोर 🍉", label_text_color=SEON_PINK, fg_color=DARK_BG)
prod_scroll_frame.pack(pady=5, fill="both", expand=True)

for prod in products:
    item_frame = ctk.CTkFrame(prod_scroll_frame, fg_color=CARD_BG, height=55)
    item_frame.pack(fill="x", padx=5, pady=4)
    
    name_lbl = ctk.CTkLabel(item_frame, text=f"{prod['name']}\n₹{prod['price']}", font=("Arial", 13, "bold"), justify="left")
    name_lbl.pack(side="left", padx=15, pady=5)
    
    add_btn = ctk.CTkButton(item_frame, text="➕ Add", font=("Arial", 12, "bold"), fg_color="transparent", border_color=SEON_PINK, border_width=1, text_color=SEON_PINK, hover_color="#2b1419", width=65, height=30,
                             command=lambda p=prod['name'], pr=prod['price']: add_to_cart(p, pr))
    add_btn.pack(side="right", padx=15)

progress_frame = ctk.CTkFrame(main_app_frame, fg_color="transparent")
progress_text = ctk.CTkLabel(progress_frame, text="", font=("Arial", 12, "bold"), text_color=NEON_GREEN)
progress_text.pack(anchor="w", padx=20)
progress_bar = ctk.CTkProgressBar(progress_frame, progress_color=NEON_GREEN, fg_color="#222222", width=400, height=8)
progress_bar.pack(pady=5)
progress_bar.set(0)

cart_frame = ctk.CTkFrame(main_app_frame, fg_color=CARD_BG, corner_radius=12, border_color="#222222", border_width=1)
cart_frame.pack(fill="x", pady=10, ipady=5)

cart_title = ctk.CTkLabel(cart_frame, text="🛒 आपकी कार्ट:", font=("Arial", 13, "bold"), text_color=NEON_GREEN)
cart_title.pack(anchor="w", padx=15, pady=3)

cart_items_label = ctk.CTkLabel(cart_frame, text=" आपकी कार्ट खाली है भाई! कुछ ऐड करो...", font=("Arial", 12), text_color="#aaaaaa", justify="left")
cart_items_label.pack(anchor="w", padx=15)

total_bill_label = ctk.CTkLabel(main_app_frame, text="💰 कुल बिल: ₹0", font=("Arial", 18, "bold"), text_color="#FFFFFF")
total_bill_label.pack(pady=2)

checkout_btn = ctk.CTkButton(main_app_frame, text="🛍️ ऑर्डर करें (Checkout)", font=("Arial", 16, "bold"), fg_color=NEON_GREEN, text_color="black", hover_color="#00CC52", height=45, command=checkout)
checkout_btn.pack(fill="x", pady=(5, 10))


# ==================== 🏁 START APP ====================
threading.Thread(target=run_edge_lighting, daemon=True).start()

# अब यह लाइन सबसे नीचे है, इसलिए कोई NameError नहीं आएगा!
show_frame(login_frame)
app.mainloop()
