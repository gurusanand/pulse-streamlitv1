import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="PULSE Dashboard",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 PULSE Executive Dashboard")
st.markdown("Real-time banking insights and performance metrics")

# Generate sample data
@st.cache_data
def generate_dashboard_data():
    dates = pd.date_range(start='2024-01-01', end='2024-06-27', freq='D')
    
    # Revenue data
    revenue_data = pd.DataFrame({
        'date': dates,
        'revenue': np.random.uniform(800000, 1200000, len(dates)) + 
                  np.sin(np.arange(len(dates)) * 2 * np.pi / 30) * 100000,
        'target': 1000000
    })
    
    # Client metrics
    client_metrics = {
        'total_clients': 1247,
        'new_clients_month': 23,
        'active_clients': 1189,
        'client_satisfaction': 8.7
    }
    
    # Deal pipeline
    pipeline_data = pd.DataFrame({
        'stage': ['Prospect', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won'],
        'count': [45, 32, 18, 12, 8],
        'value': [12500000, 8900000, 5600000, 3200000, 2100000]
    })
    
    return revenue_data, client_metrics, pipeline_data

revenue_data, client_metrics, pipeline_data = generate_dashboard_data()

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Monthly Revenue",
        value="£24.5M",
        delta="12.3%"
    )

with col2:
    st.metric(
        label="👥 Active Clients", 
        value=f"{client_metrics['active_clients']:,}",
        delta=f"+{client_metrics['new_clients_month']}"
    )

with col3:
    st.metric(
        label="📊 Pipeline Value",
        value="£32.3M",
        delta="8.7%"
    )

with col4:
    st.metric(
        label="⭐ Satisfaction",
        value=f"{client_metrics['client_satisfaction']}/10",
        delta="0.3"
    )

# Charts row
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue Trend")
    fig_revenue = px.line(
        revenue_data.tail(30), 
        x='date', 
        y='revenue',
        title="Last 30 Days Revenue Performance"
    )
    fig_revenue.add_hline(y=revenue_data['target'].iloc[0], line_dash="dash", line_color="red")
    st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    st.subheader("🎯 Deal Pipeline")
    fig_pipeline = px.funnel(
        pipeline_data,
        x='count',
        y='stage',
        title="Sales Pipeline by Stage"
    )
    st.plotly_chart(fig_pipeline, use_container_width=True)

# Recent activities
st.subheader("📋 Recent Activities")

activities = [
    {"time": "2 min ago", "icon": "🔔", "message": "New high-value opportunity: TechCorp Ltd - £8.5M credit facility"},
    {"time": "15 min ago", "icon": "✅", "message": "Deal closed: Manufacturing Inc - £3.2M term loan approved"},
    {"time": "1 hour ago", "icon": "⚠️", "message": "Risk alert: RetailChain PLC - Credit utilization at 85%"},
    {"time": "2 hours ago", "icon": "📊", "message": "Monthly risk assessment completed for 156 clients"},
    {"time": "3 hours ago", "icon": "🤝", "message": "Client meeting scheduled: GlobalTech - Treasury services discussion"}
]

for activity in activities:
    st.markdown(f"{activity['icon']} **{activity['time']}** - {activity['message']}")

# Performance indicators
st.subheader("📊 Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    # Risk distribution
    risk_data = pd.DataFrame({
        'Risk Level': ['Low', 'Medium', 'High'],
        'Count': [45, 32, 8],
        'Percentage': [53, 38, 9]
    })
    
    fig_risk = px.pie(
        risk_data,
        values='Count',
        names='Risk Level',
        title="Client Risk Distribution",
        color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    )
    st.plotly_chart(fig_risk, use_container_width=True)

with col2:
    # Product performance
    product_data = pd.DataFrame({
        'Product': ['Term Loans', 'Trade Finance', 'Treasury', 'FX Services'],
        'Revenue': [12.5, 8.3, 6.7, 4.2]
    })
    
    fig_products = px.bar(
        product_data,
        x='Product',
        y='Revenue',
        title="Product Revenue (£M)"
    )
    st.plotly_chart(fig_products, use_container_width=True)

with col3:
    # Team performance
    team_data = pd.DataFrame({
        'RM': ['Sarah J.', 'Michael C.', 'Emma W.', 'David B.'],
        'Deals': [12, 8, 15, 6],
        'Revenue': [8.5, 6.2, 9.8, 4.1]
    })
    
    fig_team = px.scatter(
        team_data,
        x='Deals',
        y='Revenue',
        text='RM',
        title="RM Performance",
        size='Revenue'
    )
    fig_team.update_traces(textposition="top center")
    st.plotly_chart(fig_team, use_container_width=True)

