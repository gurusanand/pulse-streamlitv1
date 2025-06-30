import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Pipeline Management",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Deal Pipeline Management")
st.markdown("🎯 **Track opportunities, analyze performance, and optimize your sales pipeline**")

# Generate enhanced pipeline data
@st.cache_data
def generate_pipeline_data():
    stages = ['🔍 Prospect', '✅ Qualified', '📋 Proposal', '🤝 Negotiation', '🎉 Closed Won', '❌ Closed Lost']
    stage_values = [1, 2, 3, 4, 5, 0]
    
    deals = []
    for i in range(45):
        stage_idx = random.randint(0, len(stages)-1)
        stage = stages[stage_idx]
        stage_value = stage_values[stage_idx]
        
        # Probability based on stage
        if stage_value == 0:  # Closed Lost
            probability = 0
        elif stage_value == 5:  # Closed Won
            probability = 100
        else:
            probability = random.randint(stage_value * 15, min(95, stage_value * 25))
        
        deal = {
            'deal_id': f'DEAL-{2024000 + i}',
            'client_name': random.choice(['TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd', 'HealthcarePro', 'StartupXYZ', 'LogisticsCorp', 'FinanceGroup']),
            'deal_name': random.choice(['Credit Facility', 'Term Loan', 'Working Capital', 'Trade Finance', 'Investment Loan']),
            'value': random.randint(500000, 25000000),
            'stage': stage,
            'stage_value': stage_value,
            'probability': probability,
            'rm_name': random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams', 'David Brown', 'Lisa Davis']),
            'created_date': datetime.now() - timedelta(days=random.randint(1, 180)),
            'expected_close': datetime.now() + timedelta(days=random.randint(7, 120)),
            'product_type': random.choice(['Term Loan', 'Credit Line', 'Trade Finance', 'Treasury Services', 'Investment Banking']),
            'industry': random.choice(['Technology', 'Manufacturing', 'Healthcare', 'Retail', 'Energy', 'Finance']),
            'risk_rating': random.choice(['🟢 Low', '🟡 Medium', '🔴 High']),
            'last_activity': datetime.now() - timedelta(days=random.randint(1, 14)),
            'next_action': random.choice(['Client Meeting', 'Proposal Review', 'Documentation', 'Credit Approval', 'Contract Signing']),
            'weighted_value': 0
        }
        
        # Calculate weighted value
        deal['weighted_value'] = deal['value'] * (deal['probability'] / 100)
        deals.append(deal)
    
    return pd.DataFrame(deals)

pipeline_df = generate_pipeline_data()

# Enhanced Pipeline Metrics with better styling
st.subheader("📊 Pipeline Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_deals = len(pipeline_df[pipeline_df['stage_value'] > 0])
    st.metric(
        label="🎯 Active Deals",
        value=total_deals,
        delta=f"+{random.randint(2, 8)} this week"
    )

with col2:
    total_value = pipeline_df[pipeline_df['stage_value'] > 0]['value'].sum()
    st.metric(
        label="💰 Total Pipeline",
        value=f"£{total_value/1000000:.1f}M",
        delta=f"+£{random.uniform(2, 8):.1f}M"
    )

with col3:
    weighted_value = pipeline_df[pipeline_df['stage_value'] > 0]['weighted_value'].sum()
    st.metric(
        label="⚖️ Weighted Value",
        value=f"£{weighted_value/1000000:.1f}M",
        delta=f"{random.uniform(5, 15):.1f}% confidence"
    )

with col4:
    avg_deal_size = pipeline_df[pipeline_df['stage_value'] > 0]['value'].mean()
    st.metric(
        label="📈 Avg Deal Size",
        value=f"£{avg_deal_size/1000000:.1f}M",
        delta=f"+{random.uniform(10, 25):.1f}%"
    )

with col5:
    win_rate = len(pipeline_df[pipeline_df['stage'] == '🎉 Closed Won']) / len(pipeline_df) * 100
    st.metric(
        label="🏆 Win Rate",
        value=f"{win_rate:.1f}%",
        delta=f"+{random.uniform(2, 8):.1f}%"
    )

# Pipeline Funnel Visualization
st.subheader("🔄 Pipeline Funnel")

# Create funnel data
active_deals = pipeline_df[pipeline_df['stage_value'] > 0]
funnel_data = active_deals.groupby(['stage', 'stage_value']).agg({
    'deal_id': 'count',
    'value': 'sum',
    'weighted_value': 'sum'
}).reset_index()

funnel_data = funnel_data.sort_values('stage_value', ascending=False)

col1, col2 = st.columns([2, 1])

with col1:
    # Funnel chart
    fig_funnel = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    for i, row in funnel_data.iterrows():
        fig_funnel.add_trace(go.Funnel(
            y=[row['stage']],
            x=[row['deal_id']],
            textinfo="value+percent initial",
            marker=dict(color=colors[i % len(colors)]),
            connector=dict(line=dict(color="royalblue", dash="dot", width=3))
        ))
    
    fig_funnel.update_layout(
        title="Deal Count by Stage",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    # Stage summary cards
    for _, row in funnel_data.iterrows():
        with st.container():
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 15px;
                border-radius: 10px;
                margin: 5px 0;
                color: white;
                text-align: center;
            ">
                <h4 style="margin: 0; color: white;">{row['stage']}</h4>
                <p style="margin: 5px 0; font-size: 18px; font-weight: bold;">{row['deal_id']} deals</p>
                <p style="margin: 0; font-size: 14px;">£{row['value']/1000000:.1f}M total</p>
            </div>
            """, unsafe_allow_html=True)

# Pipeline Workflow Chart
st.subheader("🔄 Deal Workflow Process")

# Create workflow visualization
workflow_stages = ['🔍 Prospect', '✅ Qualified', '📋 Proposal', '🤝 Negotiation', '🎉 Closed Won']
workflow_counts = [funnel_data[funnel_data['stage'] == stage]['deal_id'].sum() if not funnel_data[funnel_data['stage'] == stage].empty else 0 for stage in workflow_stages]

fig_workflow = go.Figure()

# Add workflow arrows and stages
for i, (stage, count) in enumerate(zip(workflow_stages, workflow_counts)):
    fig_workflow.add_trace(go.Scatter(
        x=[i],
        y=[0],
        mode='markers+text',
        marker=dict(size=max(50, count*3), color=colors[i % len(colors)], opacity=0.8),
        text=f"{stage}<br>{count} deals",
        textposition="middle center",
        textfont=dict(size=12, color="white"),
        showlegend=False,
        hovertemplate=f"<b>{stage}</b><br>Deals: {count}<extra></extra>"
    ))
    
    # Add arrows between stages
    if i < len(workflow_stages) - 1:
        fig_workflow.add_annotation(
            x=i+0.4, y=0,
            ax=i+0.6, ay=0,
            xref='x', yref='y',
            axref='x', ayref='y',
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='#34495e'
        )

fig_workflow.update_layout(
    title="Deal Flow Through Pipeline Stages",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    height=200,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig_workflow, use_container_width=True)

# Enhanced Deal Cards View
st.subheader("💼 Active Deals")

# Filter options
col1, col2, col3 = st.columns(3)

with col1:
    stage_filter = st.selectbox("Filter by Stage", ["All Stages"] + list(active_deals['stage'].unique()))

with col2:
    rm_filter = st.selectbox("Filter by RM", ["All RMs"] + list(active_deals['rm_name'].unique()))

with col3:
    sort_by = st.selectbox("Sort by", ["Value (High to Low)", "Probability", "Expected Close", "Last Activity"])

# Apply filters
filtered_deals = active_deals.copy()

if stage_filter != "All Stages":
    filtered_deals = filtered_deals[filtered_deals['stage'] == stage_filter]

if rm_filter != "All RMs":
    filtered_deals = filtered_deals[filtered_deals['rm_name'] == rm_filter]

# Sort deals
if sort_by == "Value (High to Low)":
    filtered_deals = filtered_deals.sort_values('value', ascending=False)
elif sort_by == "Probability":
    filtered_deals = filtered_deals.sort_values('probability', ascending=False)
elif sort_by == "Expected Close":
    filtered_deals = filtered_deals.sort_values('expected_close')
else:
    filtered_deals = filtered_deals.sort_values('last_activity', ascending=False)

# Display deals as enhanced cards
for _, deal in filtered_deals.head(10).iterrows():
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 15px;
                border-radius: 10px;
                color: white;
                margin: 5px 0;
            ">
                <h4 style="margin: 0; color: white;">{deal['client_name']}</h4>
                <p style="margin: 5px 0; font-size: 16px;">{deal['deal_name']}</p>
                <p style="margin: 0; font-size: 14px;">💰 £{deal['value']:,}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**Stage:** {deal['stage']}")
            st.markdown(f"**RM:** {deal['rm_name']}")
            st.markdown(f"**Risk:** {deal['risk_rating']}")
        
        with col3:
            st.metric("Probability", f"{deal['probability']}%")
            days_to_close = (deal['expected_close'] - datetime.now()).days
            st.metric("Days to Close", days_to_close)
        
        with col4:
            if st.button("📝 Update", key=f"update_{deal['deal_id']}"):
                st.success("Deal updated!")
            if st.button("📞 Contact", key=f"contact_{deal['deal_id']}"):
                st.success("Contact initiated!")
        
        st.divider()

# Performance Analytics
tab1, tab2, tab3 = st.tabs(["📈 Performance", "🎯 RM Analytics", "📊 Trends"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Value by industry
        industry_value = active_deals.groupby('industry')['value'].sum().reset_index()
        fig_industry = px.pie(
            industry_value,
            values='value',
            names='industry',
            title="Pipeline Value by Industry"
        )
        st.plotly_chart(fig_industry, use_container_width=True)
    
    with col2:
        # Probability distribution
        fig_prob = px.histogram(
            active_deals,
            x='probability',
            nbins=10,
            title="Deal Probability Distribution"
        )
        st.plotly_chart(fig_prob, use_container_width=True)

with tab2:
    # RM performance
    rm_performance = active_deals.groupby('rm_name').agg({
        'deal_id': 'count',
        'value': 'sum',
        'weighted_value': 'sum',
        'probability': 'mean'
    }).reset_index()
    
    rm_performance.columns = ['RM', 'Deal Count', 'Total Value', 'Weighted Value', 'Avg Probability']
    
    for _, rm in rm_performance.iterrows():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(f"👤 {rm['RM']}", "")
        
        with col2:
            st.metric("Deals", rm['Deal Count'])
        
        with col3:
            st.metric("Value", f"£{rm['Total Value']/1000000:.1f}M")
        
        with col4:
            st.metric("Avg Prob", f"{rm['Avg Probability']:.0f}%")

with tab3:
    # Monthly trend
    active_deals['month'] = active_deals['created_date'].dt.to_period('M')
    monthly_trend = active_deals.groupby('month').agg({
        'deal_id': 'count',
        'value': 'sum'
    }).reset_index()
    
    monthly_trend['month'] = monthly_trend['month'].astype(str)
    
    fig_trend = px.line(
        monthly_trend,
        x='month',
        y='value',
        title="Monthly Pipeline Value Trend"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("""
---
**Pipeline Management Features:**
- 🔄 Visual pipeline funnel with stage progression
- 💼 Enhanced deal cards with quick actions
- 📊 Comprehensive analytics and performance tracking
- 🎯 RM performance monitoring and comparison
- 📈 Trend analysis and forecasting capabilities
""")

