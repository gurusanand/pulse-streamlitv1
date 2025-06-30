
import streamlit as st
import plotly.graph_objects as go

st.title("🛰️ Agent Flow Dashboard – Real-time Interaction View")

st.markdown("This is a simulated visualization of the agentic AI workflow for RM deal management.")

# Define nodes and links for a Sankey-like flow chart
labels = ["RM Agent", "Review Agent", "Audit Agent", "Notification Agent"]
sources = [0, 1, 2]
targets = [1, 2, 3]
values = [10, 10, 10]

# Build the graph
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=30,
        line=dict(color="black", width=0.5),
        label=labels,
        color=["#A6CEE3", "#B2DF8A", "#FB9A99", "#FDBF6F"]
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=["#A6CEE3", "#B2DF8A", "#FB9A99"]
    ))])

fig.update_layout(title_text="Agent-to-Agent Workflow", font_size=13)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🔄 Sample Agent Actions")
st.json({
    "RM Agent": "Initiated Deal RM-002",
    "Review Agent": "Flagged for Approval – Added Comment",
    "Audit Agent": "Logged approval event",
    "Notification Agent": "Sent update to RM dashboard"
})
