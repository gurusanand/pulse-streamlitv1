
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
st.session_state.selected_deal_id = selected



if "selected_deal_id" not in st.session_state:
    st.session_state.selected_deal_id = "RM-001"

st.markdown(f"**🧭 Navigation:** Home / RM / {st.session_state.get('selected_deal_id', '')}**")



deal_info = {
    "RM-001": {"customer": "Alpha Corp", "stage": "GLM under preparation", "closure": "2024-07-01"},
    "RM-002": {"customer": "Beta Ltd", "stage": "Credit Committee Review", "closure": "2024-08-15"},
    "RM-003": {"customer": "Gamma Inc", "stage": "Initial Assessment", "closure": "2024-09-10"}
}

info = deal_info[st.session_state.selected_deal_id]
st.markdown(f"## Deal ID: {st.session_state.selected_deal_id}")
st.text(f"Customer: {info['customer']}")
st.text(f"Stage: {info['stage']} | Expected Closure: {info['closure']}")


# Approve deal simulation
status_key = f"status_{st.session_state.selected_deal_id}"
notif_key = "notifications"

if status_key in st.session_state and st.session_state[status_key] == "Under Review":
    if st.button("✅ Approve This Deal"):
        st.session_state[status_key] = "Approved"
        st.session_state[notif_key].append(f"✅ Deal {st.session_state.selected_deal_id} was approved by RM.")
        st.success("Deal marked as Approved.")
else:
    st.info("No pending approval for this deal.")



# Audit log per deal using session state
audit_key = f"audit_{st.session_state.selected_deal_id}"
if audit_key not in st.session_state:
    st.session_state[audit_key] = []

# Append audit entry on approval
if status_key in st.session_state and st.session_state[status_key] == "Approved":
    if not st.session_state[audit_key] or st.session_state[audit_key][-1] != "Approved":
        st.session_state[audit_key].append("Approved")

# Removed invalid st.markdown(" line that caused syntax errors

from datetime import datetime

# Initialize audit log per deal
audit_key = f"audit_{st.session_state.selected_deal_id}"
if audit_key not in st.session_state:
    st.session_state[audit_key] = []

# Reviewer comment input
st.markdown("### 💬 Reviewer Comment")
reviewer = st.text_input("Reviewer Name", "RM Manager")
comment = st.text_area("Comment", "Looks good. Approving.")
approve_click = st.button("✅ Approve with Comment")

if status_key in st.session_state and st.session_state[status_key] == "Under Review" and approve_click:
    st.session_state[status_key] = "Approved"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ✅ Approved by {reviewer}: {comment}"
    st.session_state[audit_key].append(entry)
    if notif_key not in st.session_state:
        st.session_state[notif_key] = []
    st.session_state[notif_key].append(entry)
    st.success("Deal marked as Approved with comment.")

# Display full timeline
st.markdown("### 🗂️ Approval Timeline")
if st.session_state[audit_key]:
    for i, event in enumerate(st.session_state[audit_key]):
        st.write(f"{i+1}. {event}")
else:
    st.info("No approval actions yet.")

