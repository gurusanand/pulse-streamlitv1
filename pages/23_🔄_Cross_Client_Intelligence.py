import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Cross Client Intelligence", page_icon="🔄", layout="wide")

st.title("🔄 Cross Client Intelligence")

# Generate synthetic cross-client data
@st.cache_data
def generate_cross_client_data():
    clients = ['TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd', 'HealthcarePro']
    sectors = ['Technology', 'Manufacturing', 'Retail', 'Energy', 'Healthcare']
    
    connections = []
    for i, client1 in enumerate(clients):
        for j, client2 in enumerate(clients):
            if i != j:
                connections.append({
                    'client_a': client1,
                    'client_b': client2,
                    'connection_strength': random.uniform(0.1, 0.9),
                    'shared_suppliers': random.randint(0, 5),
                    'shared_customers': random.randint(0, 8),
                    'geographic_overlap': random.uniform(0, 1),
                    'business_synergy': random.uniform(0.2, 0.95),
                    'risk_correlation': random.uniform(0.1, 0.8)
                })
    
    return pd.DataFrame(connections)

cross_data = generate_cross_client_data()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🔗 Active Connections", len(cross_data[cross_data['connection_strength'] > 0.5]))
with col2:
    st.metric("🎯 High Synergy Pairs", len(cross_data[cross_data['business_synergy'] > 0.8]))
with col3:
    st.metric("⚠️ Risk Correlations", len(cross_data[cross_data['risk_correlation'] > 0.6]))
with col4:
    st.metric("🌐 Network Density", f"{cross_data['connection_strength'].mean():.2f}")

# Network visualization
fig = px.scatter(cross_data, x='connection_strength', y='business_synergy', 
                size='shared_customers', color='risk_correlation',
                hover_data=['client_a', 'client_b'],
                title="Client Network Analysis")
st.plotly_chart(fig, use_container_width=True)

# Cross-selling opportunities
st.subheader("💰 Cross-Selling Opportunities")
opportunities = cross_data[cross_data['business_synergy'] > 0.7].head(5)
for _, opp in opportunities.iterrows():
    with st.expander(f"{opp['client_a']} ↔ {opp['client_b']} (Synergy: {opp['business_synergy']:.1%})"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Shared Suppliers", opp['shared_suppliers'])
            st.metric("Shared Customers", opp['shared_customers'])
        with col2:
            st.metric("Geographic Overlap", f"{opp['geographic_overlap']:.1%}")
            st.metric("Connection Strength", f"{opp['connection_strength']:.1%}")

