
import streamlit as st
import plotly.graph_objects as go
import random

st.title("🛠️ Agent Failure & Rerouting Simulation")

# Simulate failure scenario
failure = st.selectbox("Simulate Agent Failure", ["None", "Review Agent", "Audit Agent"])

# Define graph labels and dynamic paths
labels = ["RM Agent", "Review Agent", "Audit Agent", "Notification Agent", "RM Agent (Rerouted)"]
color_map = {
    "None": ["#A6CEE3", "#B2DF8A", "#FB9A99", "#FDBF6F"],
    "Review Agent": ["#A6CEE3", "#FF6666", "#FFCC99", "#9999FF", "#A6CEE3"],
    "Audit Agent": ["#A6CEE3", "#B2DF8A", "#FF6666", "#FFCC99", "#A6CEE3"]
}

source_map = {
    "None": [0, 1, 2],
    "Review Agent": [0, 1, 4],
    "Audit Agent": [0, 1, 2, 4]
}

target_map = {
    "None": [1, 2, 3],
    "Review Agent": [1, 4, 3],
    "Audit Agent": [1, 2, 4, 3]
}

labels_extended = labels if failure != "None" else labels[:4]
sources = source_map[failure]
targets = target_map[failure]
values = [10 for _ in sources]

# Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=30,
        line=dict(color="black", width=0.5),
        label=labels_extended,
        color=color_map[failure]
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=["#A6CEE3", "#FF6666", "#FFCC99", "#A6CEE3"][:len(sources)]
    ))])

fig.update_layout(title_text="Agent Flow with Failure Simulation", font_size=12)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🔄 Agent Rerouting Log")
log = []
if failure == "None":
    log = [
        "✅ RM Agent triggered Review Agent",
        "✅ Review Agent processed and passed to Audit Agent",
        "✅ Audit Agent logged and sent to Notification Agent"
    ]
elif failure == "Review Agent":
    log = [
        "✅ RM Agent attempted to call Review Agent",
        "❌ Review Agent failed to respond",
        "🔁 Rerouted to RM Agent for reassessment",
        "📢 Notification Agent updated RM dashboard"
    ]
elif failure == "Audit Agent":
    log = [
        "✅ RM Agent triggered Review Agent",
        "✅ Review Agent completed review",
        "❌ Audit Agent failed to log",
        "🔁 Rerouted back to RM Agent for manual logging",
        "📢 Notification Agent updated RM dashboard"
    ]

for entry in log:
    st.write(f"- {entry}")
