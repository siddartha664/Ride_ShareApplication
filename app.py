import streamlit as st
import random
import time

# Dummy product list
products = [
    {"name": "Product 1", "price": 100},
    {"name": "Product 2", "price": 150},
    {"name": "Service 1", "price": 200},
]

# Function to simulate payment processing
def process_payment(card_number, expiry_date, cvv):
    # Dummy check to simulate card validation
    if len(card_number) == 16 and len(expiry_date) == 5 and len(cvv) == 3:
        # Simulating a random payment success or failure
        return random.choice([True, False])
    return False

# Streamlit App
st.title("Dummy Payment System")

# Step 1: Select a product or service
st.subheader("Select a Product or Service")
selected_product = st.selectbox(
    "Choose a product/service:", [p["name"] for p in products]
)

# Get the price of the selected product
for product in products:
    if product["name"] == selected_product:
        price = product["price"]

st.write(f"Price: ${price}")

# Step 2: Input payment details
st.subheader("Enter Payment Details")
card_number = st.text_input("Card Number (16 digits)")
expiry_date = st.text_input("Expiry Date (MM/YY)")
cvv = st.text_input("CVV (3 digits)", type="password")

# Step 3: Process payment on button click
if st.button("Pay Now"):
    if card_number and expiry_date and cvv:
        with st.spinner("Processing your payment..."):
            time.sleep(2)  # Simulating processing time
            payment_success = process_payment(card_number, expiry_date, cvv)
            
            if payment_success:
                st.success(f"Payment of ${price} for {selected_product} was successful!")
            else:
                st.error("Payment failed. Please check your card details and try again.")
    else:
        st.warning("Please fill in all the payment details.")
