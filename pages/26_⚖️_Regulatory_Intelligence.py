import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Regulatory Intelligence", page_icon="⚖️", layout="wide")

st.title("⚖️ Regulatory Intelligence")

# Generate regulatory data
@st.cache_data
def generate_regulatory_data():
    regulations = []
    reg_types = ['Basel III', 'GDPR', 'AML/KYC', 'IFRS', 'Stress Testing', 'Capital Requirements']
    impact_levels = ['High', 'Medium', 'Low']
    
    for i in range(15):
        regulations.append({
            'regulation_id': f"REG-{2024000+i}",
            'regulation_type': random.choice(reg_types),
            'title': f"Regulatory Update {i+1}",
            'impact_level': random.choice(impact_levels),
            'compliance_score': random.uniform(0.6, 0.98),
            'deadline': datetime.now() + timedelta(days=random.randint(30, 365)),
            'affected_clients': random.randint(5, 25),
            'implementation_cost': random.randint(50000, 2000000),
            'status': random.choice(['Monitoring', 'In Progress', 'Compliant', 'Action Required'])
        })
    
    return pd.DataFrame(regulations)

reg_df = generate_regulatory_data()
reg_df['deadline'] = pd.to_datetime(reg_df['deadline'], errors='coerce')
reg_df = reg_df.dropna(subset=['deadline'])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📋 Active Regulations", len(reg_df))
with col2:
    high_impact = len(reg_df[reg_df['impact_level'] == 'High'])
    st.metric("🚨 High Impact", high_impact)
with col3:
    avg_compliance = reg_df['compliance_score'].mean()
    st.metric("✅ Avg Compliance", f"{avg_compliance:.1%}")
with col4:
    action_required = len(reg_df[reg_df['status'] == 'Action Required'])
    st.metric("⚡ Action Required", action_required)

# Regulatory timeline
st.subheader("📅 Regulatory Timeline")
fig = px.scatter(
    reg_df,
    x='deadline',
    y='regulation_type',
    color='impact_level',
    title="Upcoming Regulatory Deadlines"
)
st.plotly_chart(fig, use_container_width=True)

# Compliance dashboard
st.subheader("📊 Compliance Dashboard")
for _, reg in reg_df.head(8).iterrows():
    with st.expander(f"{reg['regulation_type']} - {reg['title']}"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Impact Level", reg['impact_level'])
            st.metric("Affected Clients", reg['affected_clients'])
        with col2:
            st.metric("Compliance Score", f"{reg['compliance_score']:.1%}")
            st.metric("Implementation Cost", f"£{reg['implementation_cost']:,}")
        with col3:
            st.metric("Status", reg['status'])
            days_to_deadline = (reg['deadline'] - datetime.now()).days
            st.metric("Days to Deadline", days_to_deadline)
