
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

# Create a unique session state key per deal
form_key = f"deal_form_{st.session_state.selected_deal_id}"

# Default form state if not already saved
if form_key not in st.session_state:
    st.session_state[form_key] = {
        "txn_type": info["txn_type"],
        "deal_group": info["deal_group"],
        "booking_country": info["booking_country"],
        "transaction_category": info["transaction_category"]
    }

with st.form(key="deal_edit_form"):
    txn_type = st.selectbox("Transaction Type", ["Islamic", "Conventional"], index=0 if st.session_state[form_key]["txn_type"] == "Islamic" else 1)
    deal_group = st.selectbox("Deal Group", ["IBG", "CIBG"], index=0 if st.session_state[form_key]["deal_group"] == "IBG" else 1)
    booking_country = st.selectbox("Booking Country", ["UAE", "KSA", "Qatar"], index=["UAE", "KSA", "Qatar"].index(st.session_state[form_key]["booking_country"]))
    txn_category = st.text_input("Transaction Category", st.session_state[form_key]["transaction_category"])
    submitted = st.form_submit_button("💾 Save Changes")
    if submitted:
        st.session_state[form_key] = {
            "txn_type": txn_type,
            "deal_group": deal_group,
            "booking_country": booking_country,
            "transaction_category": txn_category
        }
        st.success("Changes saved for " + st.session_state.selected_deal_id)

st.session_state.selected_deal_id = selected



if "selected_deal_id" not in st.session_state:
    st.session_state.selected_deal_id = "RM-001"

st.markdown(f"**🧭 Navigation:** Home / RM / {st.session_state.get('selected_deal_id', '')}**")


st.title("📅 RM - Create Drawdown Schedule")
st.text("Deal ID: RM-001 | Client: Alpha Corp | Booking Country: UAE")
st.date_input("Disbursement Date")
st.number_input("Disbursement Value (AED '000)", step=100000)
st.selectbox("Status", ["Amber 50%", "Green 80%", "Red 20%"])
st.button("Save Schedule")