
import streamlit as st

# Define available deal IDs
available_deals = {
    "RM-001": "Alpha Corp",
    "RM-002": "Beta Ltd",
    "RM-003": "Gamma Inc"
}

# Default session state for selected deal
if "selected_deal_id" not in st.session_state:
    st.session_state.selected_deal_id = "RM-001"

# Show breadcrumbs and deal selector
st.markdown(f"**🧭 Navigation:** Home / RM / {st.session_state.selected_deal_id} - {available_deals[st.session_state.selected_deal_id]}**")
selected = st.selectbox("Select Deal", list(available_deals.keys()), format_func=lambda x: f"{x} - {available_deals[x]}")

deal_data = {
    "RM-001": {
        "customer": "Alpha Corp",
        "txn_type": "Islamic",
        "booking_country": "UAE",
        "stage": "GLM under preparation",
        "closure_date": "2024-07-01",
        "deal_group": "IBG",
        "transaction_category": "Enhancement of limits",
        "revenue": "AED 3.2M"
    },
    "RM-002": {
        "customer": "Beta Ltd",
        "txn_type": "Conventional",
        "booking_country": "KSA",
        "stage": "Credit Committee Review",
        "closure_date": "2024-08-15",
        "deal_group": "CIBG",
        "transaction_category": "Working Capital Loan",
        "revenue": "AED 2.5M"
    },
    "RM-003": {
        "customer": "Gamma Inc",
        "txn_type": "Islamic",
        "booking_country": "Qatar",
        "stage": "Initial Assessment",
        "closure_date": "2024-09-10",
        "deal_group": "IBG",
        "transaction_category": "New Facility",
        "revenue": "AED 4.1M"
    }
}
info = deal_data[st.session_state.selected_deal_id]

st.session_state.selected_deal_id = selected



if "selected_deal_id" not in st.session_state:
    st.session_state.selected_deal_id = "RM-001"

st.markdown(f"**🧭 Navigation:** Home / RM / {st.session_state.get('selected_deal_id', '')}**")


st.title("🤝 RM - Deal Team")
st.markdown("### Assigned Team")
st.write("**Name:** Ayesha Khan  \n**Division:** Corporate Finance")
st.markdown("### Deal Room Discussion")
st.write("- 12 Jun 2025 - Added by @Ayesha: Please review document set.")