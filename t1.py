import streamlit as st

# Store payment status in session state
if "payment_status" not in st.session_state:
    st.session_state["payment_status"] = None

st.title("Dummy Payment System")

# Step 1: Product Selection
products = [
    {"name": "Product 1", "price": 100},
    {"name": "Product 2", "price": 150},
    {"name": "Service 1", "price": 200},
]
selected_product = st.selectbox("Choose a product/service:", [p["name"] for p in products])

# Get the price of the selected product
for product in products:
    if product["name"] == selected_product:
        price = product["price"]

st.write(f"Price: ${price}")

# Step 2: Payment button
pay_button = st.button("Pay Now")

# JavaScript to open new tab for payment processing
if pay_button:
    payment_url = st.get_option("browser.serverAddress") + ":8501/t2"
    st.markdown(f"""
        <script type="text/javascript">
        window.open("{payment_url}", "_blank");
        </script>
    """, unsafe_allow_html=True)

# Check for payment status
if st.session_state["payment_status"] == "success":
    st.success(f"Payment of ${price} for {selected_product} was successful!")
    # Reset payment status
    st.session_state["payment_status"] = None

elif st.session_state["payment_status"] == "failure":
    st.error("Payment failed. Please try again.")
    # Reset payment status
    st.session_state["payment_status"] = None
