import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Contextual Deal Assistant", page_icon="🧾", layout="wide")

st.title("🧾 Contextual Deal Assistant")

# Generate deal context data
@st.cache_data
def generate_deal_data():
    deals = []
    clients = ['TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd']
    deal_types = ['Credit Facility', 'Trade Finance', 'Investment Loan', 'Working Capital']
    
    for i in range(20):
        deals.append({
            'deal_id': f"DEAL-{1000+i}",
            'client': random.choice(clients),
            'deal_type': random.choice(deal_types),
            'amount': random.randint(500000, 50000000),
            'stage': random.choice(['Prospect', 'Proposal', 'Negotiation', 'Documentation', 'Closed']),
            'probability': random.uniform(0.3, 0.95),
            'ai_score': random.uniform(0.6, 0.98),
            'risk_rating': random.choice(['Low', 'Medium', 'High']),
            'timeline_days': random.randint(30, 180),
            'competitive_intel': random.choice(['High', 'Medium', 'Low']),
            'relationship_score': random.uniform(0.5, 1.0)
        })
    
    return pd.DataFrame(deals)

deal_df = generate_deal_data()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💼 Active Deals", len(deal_df))
with col2:
    total_value = deal_df['amount'].sum()
    st.metric("💰 Total Pipeline", f"£{total_value/1000000:.1f}M")
with col3:
    avg_prob = deal_df['probability'].mean()
    st.metric("📊 Avg Probability", f"{avg_prob:.1%}")
with col4:
    high_ai_score = len(deal_df[deal_df['ai_score'] > 0.8])
    st.metric("🤖 AI Recommended", high_ai_score)

# Deal recommendations
st.subheader("🎯 AI Deal Recommendations")
top_deals = deal_df.nlargest(5, 'ai_score')

for _, deal in top_deals.iterrows():
    with st.expander(f"{deal['deal_id']} - {deal['client']} (AI Score: {deal['ai_score']:.1%})"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Deal Value", f"£{deal['amount']:,}")
            st.metric("Probability", f"{deal['probability']:.1%}")
        with col2:
            st.metric("Timeline", f"{deal['timeline_days']} days")
            st.metric("Risk Rating", deal['risk_rating'])
        with col3:
            st.metric("Relationship Score", f"{deal['relationship_score']:.1%}")
            if st.button(f"Prioritize {deal['deal_id']}", key=f"prio_{deal['deal_id']}"):
                st.success("Deal prioritized!")

# Deal pipeline visualization
fig = px.sunburst(deal_df, path=['stage', 'deal_type'], values='amount',
                  title="Deal Pipeline by Stage and Type")
st.plotly_chart(fig, use_container_width=True)

