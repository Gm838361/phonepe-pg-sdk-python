import tkinter as tk
from tkinter import messagebox, ttk

# 🎨 प्रीमियम डार्क और सक्सेस थीम कलर्स
DARK_BG = '#0A0915'
CARD_BG = '#161329'
ACCENT_PURPLE = '#5f259f'
SUCCESS_GREEN = '#27AE60'
TEXT_LIGHT = '#FFFFFF'
TEXT_MUTED = '#9A91BC'

# 🛒 क्विक आइटम सजेशन्स
SUGGESTIONS = {
    'Laptop Stand': 850,
    'Ceramic Mug': 350,
    'Wireless Mouse': 499,
    'Gaming Keyboard': 1299,
    'Earbuds': 1499
}

class AdvancedBillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaurav Store - Pro Billing")
        self.root.geometry("480x750")
        self.root.configure(bg=DARK_BG)
        
        self.cart = [
            {'name': 'Laptop Stand', 'price': 850, 'qty': 1},
            {'name': 'Ceramic Mug', 'price': 350, 'qty': 1}
        ]
        self.grand_total = 0

        # --- 📱 MAIN CART SCREEN (Frame 1) ---
        self.cart_frame = tk.Frame(self.root, bg=DARK_BG)
        self.cart_frame.pack(fill="both", expand=True)

        # --- 🎉 SUCCESS SLIDE (Frame 2) ---
        self.success_frame = tk.Frame(self.root, bg=SUCCESS_GREEN)

        self.setup_cart_ui()
        self.setup_success_ui()
        self.refresh_bill()

    def setup_cart_ui(self):
        # Header Panel
        header = tk.Frame(self.cart_frame, bg=ACCENT_PURPLE, height=60)
        header.pack(fill="x")
        tk.Label(header, text="🧾 GAURAV DIGITAL STORE", font=("Arial", 15, "bold"), bg=ACCENT_PURPLE, fg="white").pack(pady=15)

        # Quick Dropdown Setup
        input_area = tk.Frame(self.cart_frame, bg=DARK_BG, padx=20, pady=10)
        input_area.pack(fill="x")

        tk.Label(input_area, text="Quick Add Item:", font=("Arial", 10, "bold"), bg=DARK_BG, fg=TEXT_MUTED).pack(side="left", padx=5)
        
        # Style the dropdown configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground=CARD_BG, background=ACCENT_PURPLE, foreground='white')
        
        self.item_combo = ttk.Combobox(input_area, values=list(SUGGESTIONS.keys()), font=("Arial", 10), state="readonly")
        self.item_combo.pack(side="left", fill="x", expand=True, padx=5)
        self.item_combo.bind("<<ComboboxSelected>>", self.quick_add)

        # --- 💳 PAYMENT MODE SELECTION PANEL (FIXED) ---
        pay_label = tk.Label(self.cart_frame, text="Select Payment Mode:", font=("Arial", 11, "bold"), bg=DARK_BG, fg=TEXT_MUTED)
        pay_label.pack(pady=(15, 5), anchor="w", padx=20)
        
        self.pay_var = tk.StringVar(value="Online (UPI)")
        mode_frame = tk.Frame(self.cart_frame, bg=CARD_BG, padx=15, pady=10, bd=1, relief="solid")
        mode_frame.pack(fill="x", padx=20, pady=5)
        
        # Radio buttons mapped cleanly to avoid syntax layout errors
        tk.Radiobutton(mode_frame, text="Debit/Credit Card", variable=self.pay_var, value="Card", bg=CARD_BG, fg=TEXT_LIGHT, selectcolor=DARK_BG, font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Radiobutton(mode_frame, text="Online (UPI/PhonePe)", variable=self.pay_var, value="Online", bg=CARD_BG, fg=TEXT_LIGHT, selectcolor=DARK_BG, font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Radiobutton(mode_frame, text="Cash on Delivery (COD)", variable=self.pay_var, value="Cash", bg=CARD_BG, fg=TEXT_LIGHT, selectcolor=DARK_BG, font=("Arial", 10)).pack(anchor="w", pady=2)

        # Receipt Area Screen
        tk.Label(self.cart_frame, text="Live Invoice Receipt:", font=("Arial", 11, "bold"), bg=DARK_BG, fg=TEXT_MUTED).pack(anchor="w", padx=20, pady=(10, 2))
        self.bill_text = tk.Text(self.cart_frame, height=14, bg=CARD_BG, fg="white", font=("Courier", 10), bd=0, padx=15, pady=15)
        self.bill_text.pack(fill="x", padx=20, pady=5)

        # Action Buttons Layout
        btn_clear = tk.Button(self.cart_frame, text="🔄 Clear All Items", font=("Arial", 10, "bold"), bg="#443355", fg=TEXT_LIGHT, bd=0, command=self.clear_all, height=1)
        btn_clear.pack(fill="x", padx=20, pady=2)

        self.pay_btn = tk.Button(self.cart_frame, text="🔒 CONFIRM ORDER & PAY", font=("Arial", 13, "bold"), bg=SUCCESS_GREEN, fg="white", bd=0, height=2, command=self.go_to_success)
        self.pay_btn.pack(fill="x", padx=20, pady=15, side="bottom")

    def setup_success_ui(self):
        # Big Verified Checkmark
        tk.Label(self.success_frame, text="✔", font=("Arial", 90), bg=SUCCESS_GREEN, fg="white").pack(pady=(140, 10))
        tk.Label(self.success_frame, text="Shopping Successful!", font=("Arial", 24, "bold"), bg=SUCCESS_GREEN, fg="white").pack()
        
        self.final_details = tk.Label(self.success_frame, text="", font=("Arial", 13), bg=SUCCESS_GREEN, fg="#E0FFE0", justify="center")
        self.final_details.pack(pady=25)

        tk.Button(self.success_frame, text="⬅ BACK TO GAURAV STORE", font=("Arial", 12, "bold"), bg="white", fg=SUCCESS_GREEN, bd=0, width=24, height=2, command=self.reset_app).pack(pady=40)

    def quick_add(self, event):
        name = self.item_combo.get()
        if name in SUGGESTIONS:
            price = SUGGESTIONS[name]
            self.cart.append({'name': name, 'price': price, 'qty': 1})
            self.refresh_bill()

    def refresh_bill(self):
        self.bill_text.config(state="normal")
        self.bill_text.delete("1.0", tk.END)
        
        header = f"{'Item Name':<20} {'Qty':<5} {'Total Price':<10}\n"
        divider = "-"*40 + "\n"
        content = ""
        total = 0
        
        for item in self.cart:
            line_total = item['price'] * item['qty']
            content += f"{item['name'][:18]:<20} {item['qty']:<5} ₹{line_total:<10}\n"
            total += line_total
        
        self.grand_total = total
        self.bill_text.insert(tk.END, header + divider + content + divider + f"GRAND TOTAL: ₹{total}")
        self.bill_text.config(state="disabled")

    def go_to_success(self):
        if not self.cart:
            messagebox.showwarning("Cart Empty", "कृपया पहले बिल में कोई आइटम जोड़ें!")
            return
        
        mode = self.pay_var.get()
        details = f"Final Amount: ₹{self.grand_total}\nPayment Mode selected: {mode.upper()}\n\nOrder Has Been Confirmed Successfully!"
        self.final_details.config(text=details)
        
        # --- 🔄 SCREEN SWAPPING ANIMATION (SLIDE CHANGE) ---
        self.cart_frame.pack_forget()
        self.success_frame.pack(fill="both", expand=True)

    def clear_all(self):
        self.cart.clear()
        self.refresh_bill()

    def reset_app(self):
        self.cart.clear()
        self.refresh_bill()
        self.success_frame.pack_forget()
        self.cart_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedBillApp(root)
    root.mainloop()
