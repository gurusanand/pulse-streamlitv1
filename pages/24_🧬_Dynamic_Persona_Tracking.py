import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Dynamic Persona Tracking", page_icon="🧬", layout="wide")

st.title("🧬 Dynamic Persona Tracking")

# Generate persona evolution data
@st.cache_data
def generate_persona_data():
    personas = []
    clients = ['TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd']
    persona_types = ['Conservative', 'Growth-Oriented', 'Risk-Averse', 'Aggressive', 'Balanced']
    
    for client in clients:
        for days_back in range(30, 0, -1):
            date = datetime.now() - timedelta(days=days_back)
            personas.append({
                'client': client,
                'date': date,
                'persona_type': random.choice(persona_types),
                'confidence_score': random.uniform(0.6, 0.95),
                'risk_appetite': random.uniform(0.1, 0.9),
                'growth_focus': random.uniform(0.2, 0.8),
                'decision_speed': random.uniform(0.3, 0.9),
                'relationship_depth': random.uniform(0.4, 1.0)
            })
    
    return pd.DataFrame(personas)

persona_df = generate_persona_data()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🎭 Active Personas", len(persona_df['persona_type'].unique()))
with col2:
    st.metric("📈 Persona Shifts", random.randint(5, 12))
with col3:
    st.metric("🎯 Avg Confidence", f"{persona_df['confidence_score'].mean():.1%}")
with col4:
    st.metric("⚡ Real-time Updates", "Live")

# Persona evolution chart
fig = px.line(persona_df, x='date', y='risk_appetite', color='client',
              title="Risk Appetite Evolution by Client")
st.plotly_chart(fig, use_container_width=True)

# Current persona analysis
st.subheader("🎭 Current Persona Analysis")
current_personas = persona_df.groupby('client').last().reset_index()

for _, persona in current_personas.iterrows():
    with st.expander(f"{persona['client']} - {persona['persona_type']}"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Risk Appetite", f"{persona['risk_appetite']:.1%}")
            st.metric("Growth Focus", f"{persona['growth_focus']:.1%}")
        with col2:
            st.metric("Decision Speed", f"{persona['decision_speed']:.1%}")
            st.metric("Relationship Depth", f"{persona['relationship_depth']:.1%}")
        with col3:
            st.metric("Confidence", f"{persona['confidence_score']:.1%}")
            if st.button(f"Update {persona['client']}", key=f"update_{persona['client']}"):
                st.success("Persona updated!")

