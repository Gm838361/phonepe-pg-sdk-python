import tkinter as tk
from tkinter import messagebox, simpledialog
import time

# 🎨 फोनपे ऑफिशियल डार्क थीम कलर्स
PHONEPE_PURPLE = "#5f259f"  
NEON_GREEN = "#2ACC76"      
SUCCESS_BLUE = "#0066FF"    
DARK_BG = "#090710"          
CARD_BG = "#161329"          
TEXT_LIGHT = "#FFFFFF"       
TEXT_MUTED = "#9A91BC"       

app = tk.Tk()
app.title("PhonePe Ultimate Flow")
app.geometry("460x720")     # 📱 परफेक्ट मोबाइल साइज
app.configure(bg=DARK_BG)

# 🔐 सुरक्षा और बैंक सेटिंग्स (आपकी फोटो के अनुसार सटीक)
SECRET_PIN = "820922"
history_records = []  

# बैंक खाते और उनका बैलेंस
banks_data = [
    {"name": "Rajasthan Gramin Bank - 9692", "bal": "₹45,230.00"},
    {"name": "Rajasthan Gramin Bank - 1431", "bal": "₹1,205.50"},
    {"name": "State Bank of India - 4630", "bal": "₹3,00,00,00,00,000"}
]

target_name = ""
target_info = ""
payment_amount = "0"

# --- 🎨 लाइव 'पे' लोगो ड्रा करने का फंक्शन ---
def draw_phonepe_logo(canvas, size=40):
    canvas.delete("all")
    canvas.create_oval(2, 2, size-2, size-2, fill=PHONEPE_PURPLE, outline="")
    scale = size / 100
    canvas.create_line(35*scale, 30*scale, 65*scale, 15*scale, fill="white", width=int(7*scale), capstyle="round")
    canvas.create_line(25*scale, 40*scale, 75*scale, 40*scale, fill="white", width=int(8*scale), capstyle="round")
    canvas.create_line(38*scale, 40*scale, 38*scale, 65*scale, fill="white", width=int(8*scale))
    canvas.create_arc(38*scale, 50*scale, 68*scale, 76*scale, start=180, extent=180, style="arc", outline="white", width=int(8*scale))
    canvas.create_line(68*scale, 63*scale, 68*scale, 40*scale, fill="white", width=int(8*scale))
    canvas.create_line(53*scale, 75*scale, 53*scale, 88*scale, fill="white", width=int(8*scale), capstyle="round")

# --- स्क्रीन मैनेजर ---
def show_screen(frame_to_show):
    home_screen_frame.pack_forget()
    processing_frame.pack_forget()
    success_frame.pack_forget()
    history_frame.pack_forget()
    bank_screen_frame.pack_forget()
    frame_to_show.pack(fill="both", expand=True)

# --- बैंक अकाउंट स्क्रीन ---
def open_bank_screen():
    for widget in bank_list_frame.winfo_children():
        widget.destroy()
        
    for bank in banks_data:
        item = tk.Frame(bank_list_frame, bg=CARD_BG, height=70)
        item.pack(fill="x", pady=5)
        item.pack_propagate(False)
        
        tk.Label(item, text="🏦", font=("Arial", 16), bg=CARD_BG, fg=NEON_GREEN).pack(side="left", padx=15)
        lbl = tk.Label(item, text=bank["name"], font=("Arial", 12, "bold"), bg=CARD_BG, fg=TEXT_LIGHT, anchor="w")
        lbl.pack(side="left", padx=5)
        
        def check_this_bal(b_name=bank["name"], b_bal=bank["bal"]):
            pin = simpledialog.askstring("UPI PIN", f"🏦 {b_name}\nअपना 6-अंकीय UPI PIN दर्ज करें:", show="*")
            if pin == SECRET_PIN:
                messagebox.showinfo("Available Balance", f"🏦 {b_name}\n\n💰 Available Balance:\n{b_bal}")
            else:
                messagebox.showerror("Error", "❌ गलत UPI PIN!")
                
        tk.Button(item, text="Check Balance", font=("Arial", 10, "bold"), bg=PHONEPE_PURPLE, fg="white", bd=0, padx=10, command=check_this_bal).pack(side="right", padx=15, pady=15)
        
    show_screen(bank_screen_frame)

# --- पेमेंट गेटवे फ्लो ---
def init_contact_pay():
    global target_name, target_info, payment_amount
    num = simpledialog.askstring("PhonePe", "💥 मोबाइल नंबर दर्ज करें:")
    if not num or len(num) < 10:
        messagebox.showwarning("Error", "❌ सही नंबर डालें!")
        return
    
    amt = simpledialog.askstring("PhonePe", f"To: {num}\n💰 राशि दर्ज करें (₹):")
    if not amt or not amt.isdigit() or int(amt) <= 0: return
        
    target_name = "Gaurav Store"
    target_info = f"Mobile: {num}"
    payment_amount = amt
    
    user_pin = simpledialog.askstring("UPI PIN", "🔒 अपना 6-अंकीय UPI PIN दर्ज करें:", show="*")
    if user_pin == SECRET_PIN:
        show_screen(processing_frame)
        app.update()
        time.sleep(1.5) # सिमुलेटेड लोडिंग
        
        current_date = time.strftime("%b %d, %Y")
        history_records.insert(0, {"name": target_name, "date": current_date, "amount": f"₹{payment_amount}", "status": "Sent"})
        
        success_amount_lbl.config(text=f"₹{payment_amount}.00 Sent!")
        success_msg_lbl.config(text=f"Paid Successfully to\n{target_name}")
        show_screen(success_frame)
        messagebox.showinfo("SMS Alert", f"💬 Account Debited with ₹{payment_amount}. Sent to {target_name}!")
    else:
        messagebox.showerror("Error", "❌ गलत पिन!")

# --- हिस्ट्री स्क्रीन (फिक्स्ड लाइन 131 गड़बड़) ---
def open_history_screen():
    for widget in list_box_frame.winfo_children():
        widget.destroy()
        
    # ✅ यहाँ लाइन 131 का लॉजिक बिल्कुल फिक्स कर दिया है भाई!
    if len(history_records) == 0:
        tk.Label(list_box_frame, text="No Transactions Yet", font=("Arial", 14), bg=DARK_BG, fg="#6F668E").pack(pady=100)
    else:
        for txn in history_records:
            item = tk.Frame(list_box_frame, bg=CARD_BG, height=75)
            item.pack(fill="x", pady=4)
            item.pack_propagate(False)
            
            logo_canvas = tk.Canvas(item, width=35, height=35, bg=CARD_BG, bd=0, highlightthickness=0)
            logo_canvas.pack(side="left", padx=10, pady=20)
            draw_phonepe_logo(logo_canvas, size=35)
            
            title_part = tk.Label(item, text=f"{txn['name']}\n{txn['date']}", font=("Arial", 12, "bold"), bg=CARD_BG, fg=TEXT_LIGHT, justify="left", anchor="w")
            title_part.pack(side="left", padx=5)
            
            amt_part = tk.Label(item, text=f"{txn['amount']}\n{txn['status']}", font=("Arial", 12, "bold"), bg=CARD_BG, fg=NEON_GREEN, justify="right", anchor="e")
            amt_part.pack(side="right", padx=15)

    show_screen(history_frame)


# ==================== 🏢 1. होम स्क्रीन लेआउट ====================
home_screen_frame = tk.Frame(app, bg=DARK_BG)
home_screen_frame.pack(fill="both", expand=True)

top_bar = tk.Frame(home_screen_frame, bg=PHONEPE_PURPLE, height=70)
top_bar.pack(fill="x", side="top")
top_bar.pack_propagate(False)

header_logo_canvas = tk.Canvas(top_bar, width=42, height=42, bg=PHONEPE_PURPLE, bd=0, highlightthickness=0)
header_logo_canvas.pack(side="left", padx=15, pady=14)
app.after(10, lambda: draw_phonepe_logo(header_logo_canvas, size=42))

tk.Label(top_bar, text="Pay with PhonePe", font=("Arial", 18, "bold"), bg=PHONEPE_PURPLE, fg="#FFFFFF").pack(side="left", pady=18)

tk.Label(home_screen_frame, text="Money Transfers", font=("Arial", 13, "bold"), bg=DARK_BG, fg=TEXT_MUTED).pack(anchor="w", padx=20, pady=(20, 5))
grid_frame = tk.Frame(home_screen_frame, bg=CARD_BG, height=85)
grid_frame.pack(fill="x", padx=20, pady=5)
grid_frame.pack_propagate(False)

tk.Button(grid_frame, text="To Mobile\nNumber", font=("Arial", 10, "bold"), bg=CARD_BG, fg="white", bd=0, width=12, command=init_contact_pay).pack(side="left", padx=8)
tk.Button(grid_frame, text="To Bank &\nSelf A/c", font=("Arial", 10, "bold"), bg=CARD_BG, fg="white", bd=0, width=12, command=open_bank_screen).pack(side="left", padx=8)
tk.Button(grid_frame, text="Check\nBalance", font=("Arial", 10, "bold"), bg=CARD_BG, fg="white", bd=0, width=12, command=open_bank_screen).pack(side="left", padx=8)

scan_btn = tk.Button(home_screen_frame, text="📸 Simulated Scan & Pay", font=("Arial", 15, "bold"), bg=PHONEPE_PURPLE, fg="white", bd=0, height=2, command=init_contact_pay)
scan_btn.pack(fill="x", padx=20, pady=20)

banner_panel = tk.Frame(home_screen_frame, bg="#1E133D", bd=1, relief="solid", height=200)
banner_panel.pack(fill="x", padx=20, pady=10)
banner_panel.pack_propagate(False)
tk.Label(banner_panel, text="Up to 2% Cashback\non wallet payments", font=("Arial", 22, "bold"), bg="#1E133D", fg="white", justify="left").pack(anchor="w", padx=20, pady=50)


# ==================== 🔄 2. लाइव प्रोसेसिंग स्क्रीन ====================
processing_frame = tk.Frame(app, bg=CARD_BG)
proc_status_lbl = tk.Label(processing_frame, text="Processing Payment...\nVerifying PIN...", font=("Arial", 18, "bold"), bg=CARD_BG, fg=TEXT_LIGHT, justify="center")
proc_status_lbl.pack(expand=True)


# ==================== 🎉 3. नीली सक्सेस स्क्रीन ====================
success_frame = tk.Frame(app, bg=SUCCESS_BLUE)
success_logo_canvas = tk.Canvas(success_frame, width=70, height=70, bg=SUCCESS_BLUE, bd=0, highlightthickness=0)
success_logo_canvas.pack(pady=(60, 5))
app.after(10, lambda: draw_phonepe_logo(success_logo_canvas, size=70))

tk.Label(success_frame, text="Payment Successful", font=("Arial", 22, "bold"), bg=SUCCESS_BLUE, fg="#FFFFFF").pack(pady=5)
success_amount_lbl = tk.Label(success_frame, text="₹0.00 Sent!", font=("Arial", 36, "bold"), bg=SUCCESS_BLUE, fg="#FFFFFF")
success_amount_lbl.pack(pady=10)
success_msg_lbl = tk.Label(success_frame, text="", font=("Arial", 14), bg=SUCCESS_BLUE, fg="#E0EFFF", justify="center")
success_msg_lbl.pack(pady=5)

tk.Button(success_frame, text="VIEW REWARD & HISTORY", font=("Arial", 13, "bold"), bg=PHONEPE_PURPLE, fg="white", bd=0, height=2, command=open_history_screen).pack(fill="x", padx=30, side="bottom", pady=40)


# ==================== 🏦 4. लाइव बैंक अकाउंट्स स्क्रीन ====================
bank_screen_frame = tk.Frame(app, bg=DARK_BG)
bank_top = tk.Frame(bank_screen_frame, bg=PHONEPE_PURPLE, height=70)
bank_top.pack(fill="x", side="top")
bank_top.pack_propagate(False)
tk.Button(bank_top, text="⬅️ Back", font=("Arial", 11, "bold"), bg="#4d1d82", fg="white", bd=0, command=lambda: show_screen(home_screen_frame)).pack(side="left", padx=15, pady=18)
tk.Label(bank_top, text="Check Balance", font=("Arial", 18, "bold"), bg=PHONEPE_PURPLE, fg="#FFFFFF").pack(side="left", padx=10, pady=18)

bank_list_frame = tk.Frame(bank_screen_frame, bg=DARK_BG)
bank_list_frame.pack(fill="both", expand=True, padx=20, pady=10)


# ==================== 📊 5. ट्रांजैक्शन हिस्ट्री स्क्रीन ====================
history_frame = tk.Frame(app, bg=DARK_BG)
hist_top = tk.Frame(history_frame, bg=PHONEPE_PURPLE, height=70)
hist_top.pack(fill="x", side="top")
hist_top.pack_propagate(False)
tk.Button(hist_top, text="⬅️ Back", font=("Arial", 11, "bold"), bg="#4d1d82", fg="white", bd=0, command=lambda: show_screen(home_screen_frame)).pack(side="left", padx=15, pady=18)
tk.Label(hist_top, text="History Logs", font=("Arial", 18, "bold"), bg=PHONEPE_PURPLE, fg="#FFFFFF").pack(side="left", padx=10, pady=18)

list_box_frame = tk.Frame(history_frame, bg=DARK_BG)
list_box_frame.pack(fill="both", expand=True, padx=20, pady=10)


# ==================== 🗺️ 6. बॉटम फिक्सड नेविगेशन बार ====================
bottom_nav = tk.Frame(app, bg="#0A0914", height=65)
bottom_nav.pack(fill="x", side="bottom")
bottom_nav.pack_propagate(False)

tk.Button(bottom_nav, text="Home", font=("Arial", 10, "bold"), bg="#0A0914", fg="white", bd=0, width=11, command=lambda: show_screen(home_screen_frame)).pack(side="left")
tk.Button(bottom_nav, text="Search", font=("Arial", 10), bg="#0A0914", fg=TEXT_MUTED, bd=0, width=11).pack(side="left")
tk.Button(bottom_nav, text="Alerts", font=("Arial", 10), bg="#0A0914", fg=TEXT_MUTED, bd=0, width=11).pack(side="left")
tk.Button(bottom_nav, text="History", font=("Arial", 10, "bold"), bg="#0A0914", fg="#B49DFF", bd=0, width=11, command=open_history_screen).pack(side="left")

# डिफ़ॉल्ट रूप से पहली स्क्रीन खोलना
show_screen(home_screen_frame)

app.mainloop()
