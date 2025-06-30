
import streamlit as st
import pandas as pd

# Dummy data for personas
personas = [
    {
        "name": "M. SUBRAMANIAN",
        "designation": "Chairman",
        "client": "GARNASH ENTERPRISES LLC SYN1",
        "cif": "0131045486",
        "email": "ZJG@mil.k@kensmarshop.com",
        "phone": "9718810062",
        "last_call_status": "Completed - Positive",
        "communication_status": "Awaiting follow-up email",
        "positions": ["ALIJABR REAL ESTATE INV.", "EGYPTIAN GENERAL PETRO LTD..."],
        "activity": "LUKOIL FINANCE B.V. - Treasury Services - FX Approved",
        "call_history": [
            {"date": "11-Jun-2025", "company": "VITOL BAHRAIN E C", "status": "Completed"},
            {"date": "03-May-2025", "company": "ABU DHABI COMMERCE", "status": "Missed"},
            {"date": "21-Apr-2025", "company": "NATIONAL BANK", "status": "Completed"}
        ],
        "news": [
            {"title": "Swiss criminal court convicts bank", "sentiment": "Negative"},
            {"title": "Total unit fined $4.1 million for attempted market manipulation", "sentiment": "Negative"},
            {"title": "LNG sanctions under US scrutiny", "sentiment": "Negative"}
        ]
    },
    {
        "name": "Rahul Iyer",
        "designation": "Group CFO",
        "client": "AL TAYER MOTORS LLC",
        "cif": "0210043200",
        "email": "rahul@altayer.com",
        "phone": "971509988888",
        "last_call_status": "Completed",
        "communication_status": "Proposal sent",
        "positions": ["AL TAYER INVESTMENTS"],
        "activity": "Treasury FX Deal Executed - HSBC",
        "call_history": [
            {"date": "05-May-2025", "company": "HSBC MIDDLE EAST", "status": "Completed"}
        ],
        "news": [
            {"title": "HSBC expands FX trade services", "sentiment": "Positive"}
        ]
    }
]

st.title("🧑‍💼 Personas - Client View")

client_names = sorted(set(p["client"] for p in personas))
selected_client = st.selectbox("Select a Client", client_names)

search_query = st.text_input("Search Personas (Name or Designation)").strip().lower()

# Filter personas by client and search
filtered_personas = [
    p for p in personas
    if p["client"] == selected_client and
    (search_query in p["name"].lower() or search_query in p["designation"].lower())
]

if filtered_personas:
    names = [p["name"] for p in filtered_personas]
    selected_name = st.selectbox("Select a Persona", names)

    persona = next((p for p in personas if p["name"] == selected_name), None)

    if persona:
        st.subheader(f"{persona['name']} - {persona['designation']}")
        st.markdown(
"**Client Name:** {}  \n**CIF:** {}  \n**Email:** {}  \n**Phone:** {}".format(
    persona["client"], persona["cif"], persona["email"], persona["phone"]
)
        )
        st.markdown(
            "**Last Call Status:** {}  \n**Communication Status:** {}".format(
                persona["last_call_status"], persona["communication_status"]
            )
        )

        st.markdown("### Current Positions")
        for pos in persona.get("positions", []):
            st.write(f"- {pos}")

        st.markdown("### Persona Activity")
        st.success(persona.get("activity", "No recent activity"))

        st.markdown("### Call History (Last 12 months)")
        if persona.get("call_history"):
            df_calls = pd.DataFrame(persona["call_history"])
            st.table(df_calls)
        else:
            st.info("No call history available.")

        st.markdown("### Related News")
        if persona.get("news"):
            for item in persona["news"]:
                st.write(f"- **{item['title']}** ({item['sentiment']})")
        else:
            st.info("No news available.")

        # Link to Group View
        st.markdown("---")
        st.markdown(
            f"[🔗 View Group Details for {persona['client']}](/Group_View?client={persona['client'].replace(' ', '%20')})"
        )
else:
    st.warning("No matching personas found for this client.")
