import streamlit as st
import random
import time

# Dummy payment processing
def process_payment():
    time.sleep(2)  # Simulating processing time
    return random.choice([True, False])

st.title("Payment Processing")

# Simulate the payment process
if process_payment():
    st.success("Payment successful! Redirecting...")
    st.session_state["payment_status"] = "success"
else:
    st.error("Payment failed! Redirecting...")
    st.session_state["payment_status"] = "failure"

# JavaScript to close the tab and return to the main page
main_page_url = st.get_option("browser.serverAddress")
st.markdown(f"""
    <script type="text/javascript">
    setTimeout(function() {{
        window.close();
        window.opener.location.href = "{main_page_url}";
    }}, 2000);
    </script>
""", unsafe_allow_html=True)
