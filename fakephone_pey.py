import streamlit as st
import time
import random

st.set_page_config(page_title="Gaurav Digital Store", page_icon="🧾", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0A0915; }
    h1, h2, h3 { color: #FFFFFF !important; }
    div.stButton > button:first-child {
        background-color: #27AE60; color: white; font-size: 18px;
        font-weight: bold; border-radius: 8px; width: 100%; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

SUGGESTIONS = {'Laptop Stand': 850, 'Ceramic Mug': 350, 'Wireless Mouse': 499, 'Gaming Keyboard': 1299, 'Earbuds': 1499}

if 'cart' not in st.session_state: st.session_state.cart = [{'name': 'Laptop Stand', 'price': 850, 'qty': 1}, {'name': 'Ceramic Mug', 'price': 350, 'qty': 1}]
if 'page' not in st.session_state: st.session_state.page = 'cart'
if 'payment_mode' not in st.session_state: st.session_state.payment_mode = 'Online'
if 'generated_otp' not in st.session_state: st.session_state.generated_otp = None
if 'user_mobile' not in st.session_state: st.session_state.user_mobile = ""

if st.session_state.page == 'cart':
    st.title("🧾 GAURAV DIGITAL STORE")
    st.subheader("Jaipur, Rajasthan")
    st.write("---")
    selected_item = st.selectbox("🛍️ Quick Add Item:", ["Select an item..."] + list(SUGGESTIONS.keys()))
    if selected_item != "Select an item...":
        if st.button("➕ Add to Bill"):
            st.session_state.cart.append({'name': selected_item, 'price': SUGGESTIONS[selected_item], 'qty': 1})
            st.success(f"{selected_item} जोड़ा गया!")
            time.sleep(0.5)
            st.rerun()
    st.write("---")
    st.session_state.payment_mode = st.radio("💳 Select Payment Mode:", ['Debit/Credit Card', 'Online (UPI/PhonePe)', 'Cash on Delivery (COD)'])
    st.write("---")
    st.session_state.user_mobile = st.text_input("📞 Customer Mobile:", max_chars=10, placeholder="98XXXXXXXX")
    st.write("---")
    total = 0
    bill_content = f"{'Item Name':<20} {'Qty':<5} {'Price':<10}\n" + "-"*40 + "\n"
    for item in st.session_state.cart:
        line_total = item['price'] * item['qty']
        bill_content += f"{item['name'][:18]:<20} {item['qty']:<5} ₹{line_total:<10}\n"
        total += line_total
    bill_content += "-"*40 + "\n" + f"GRAND TOTAL: ₹{total}\n"
    st.code(bill_content, language="text")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear All"): st.session_state.cart = []; st.rerun()
    with col2:
        if st.button("🔒 SEND OTP & CONFIRM"):
            if not st.session_state.cart: st.error("बिल खाली है!")
            elif len(st.session_state.user_mobile) != 10 or not st.session_state.user_mobile.isdigit(): st.error("कृपया सही 10-अंकीय मोबाइल नंबर डालें!")
            else:
                st.session_state.generated_otp = str(random.randint(1000, 9999))
                st.session_state.page = 'otp_verify'; st.rerun()

elif st.session_state.page == 'otp_verify':
    st.title("🔒 Security Verification")
    st.write(f"OTP sent to **+91 {st.session_state.user_mobile}**")
    st.info(f"💬 **SMS Alert System:** Gaurav Store Order OTP is **{st.session_state.generated_otp}**")
    st.write("---")
    user_otp_input = st.text_input("Enter 4-digit OTP shown above:", max_chars=4, placeholder="XXXX")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Cancel"): st.session_state.page = 'cart'; st.rerun()
    with col2:
        if st.button("✅ Verify & Pay"):
            if user_otp_input == st.session_state.generated_otp: st.session_state.page = 'success'; st.rerun()
            else: st.error("❌ गलत OTP! कृपया सही नंबर डालें।")

elif st.session_state.page == 'success':
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #27AE60;'>✔ Shopping Successful!</h1>", unsafe_allow_html=True)
    total_amount = sum(item['price'] * item['qty'] for item in st.session_state.cart)
    st.write("---")
    st.markdown(f"<div style='text-align: center; font-size: 18px; color: #E0FFE0;'><p><b>Amount Paid:</b> ₹{total_amount}</p><p><b>Mode:</b> {st.session_state.payment_mode}</p><p>🔐 Verified via Gaurav Secure OTP</p><p>🎉 Order Confirmed Successfully!</p></div>", unsafe_allow_html=True)
    st.write("---")
    if st.button("⬅ BACK TO STORE"): st.session_state.cart = []; st.session_state.page = 'cart'; st.rerun()
