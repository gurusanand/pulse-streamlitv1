import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="RM Pipeline Summary",
    page_icon="🔁",
    layout="wide"
)

st.title("🔁 RM Pipeline Summary")
st.markdown("📈 **Comprehensive pipeline overview across all relationship managers**")

# Generate enhanced RM pipeline data
@st.cache_data
def generate_rm_pipeline_data():
    rms = ['Sarah Johnson', 'Michael Chen', 'Emma Williams', 'David Brown', 'Lisa Davis', 'James Wilson', 'Maria Garcia', 'Robert Taylor']
    stages = ['🔍 Prospect', '✅ Qualified', '📋 Proposal', '🤝 Negotiation', '🎉 Closed Won', '❌ Closed Lost']
    
    pipeline_data = []
    
    for rm in rms:
        # Generate deals for each RM
        num_deals = random.randint(8, 20)
        
        for i in range(num_deals):
            stage = random.choice(stages)
            
            # Probability based on stage
            if stage == '❌ Closed Lost':
                probability = 0
            elif stage == '🎉 Closed Won':
                probability = 100
            elif stage == '🤝 Negotiation':
                probability = random.randint(70, 90)
            elif stage == '📋 Proposal':
                probability = random.randint(50, 75)
            elif stage == '✅ Qualified':
                probability = random.randint(30, 60)
            else:  # Prospect
                probability = random.randint(10, 40)
            
            deal = {
                'rm_name': rm,
                'deal_id': f'DEAL-{rm[:2].upper()}-{1000 + i}',
                'client_name': random.choice(['TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd', 'HealthcarePro', 'StartupXYZ', 'LogisticsCorp', 'FinanceGroup', 'AutoMotive Co', 'ConsultingFirm']),
                'deal_name': random.choice(['Credit Facility', 'Term Loan', 'Working Capital', 'Trade Finance', 'Investment Loan', 'Equipment Finance']),
                'value': random.randint(250000, 15000000),
                'stage': stage,
                'probability': probability,
                'created_date': datetime.now() - timedelta(days=random.randint(1, 120)),
                'expected_close': datetime.now() + timedelta(days=random.randint(7, 90)),
                'product_type': random.choice(['Term Loan', 'Credit Line', 'Trade Finance', 'Treasury Services', 'Investment Banking']),
                'industry': random.choice(['Technology', 'Manufacturing', 'Healthcare', 'Retail', 'Energy', 'Finance', 'Automotive']),
                'risk_rating': random.choice(['🟢 Low', '🟡 Medium', '🔴 High']),
                'last_activity': datetime.now() - timedelta(days=random.randint(1, 10))
            }
            
            # Calculate weighted value
            deal['weighted_value'] = deal['value'] * (deal['probability'] / 100)
            pipeline_data.append(deal)
    
    return pd.DataFrame(pipeline_data)

pipeline_df = generate_rm_pipeline_data()

# RM Performance Overview
st.subheader("🎯 RM Performance Overview")

# Calculate RM metrics
rm_summary = pipeline_df.groupby('rm_name').agg({
    'deal_id': 'count',
    'value': 'sum',
    'weighted_value': 'sum',
    'probability': 'mean'
}).reset_index()

rm_summary.columns = ['RM', 'Total Deals', 'Pipeline Value', 'Weighted Value', 'Avg Probability']

# Top metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rms = len(rm_summary)
    st.metric(
        label="👥 Active RMs",
        value=total_rms,
        delta="All performing"
    )

with col2:
    total_pipeline = rm_summary['Pipeline Value'].sum()
    st.metric(
        label="💰 Total Pipeline",
        value=f"£{total_pipeline/1000000:.1f}M",
        delta=f"+{random.uniform(8, 15):.1f}%"
    )

with col3:
    total_weighted = rm_summary['Weighted Value'].sum()
    st.metric(
        label="⚖️ Weighted Pipeline",
        value=f"£{total_weighted/1000000:.1f}M",
        delta=f"{random.uniform(65, 85):.0f}% confidence"
    )

with col4:
    avg_deals_per_rm = rm_summary['Total Deals'].mean()
    st.metric(
        label="📊 Avg Deals/RM",
        value=f"{avg_deals_per_rm:.0f}",
        delta=f"+{random.uniform(2, 5):.0f} vs target"
    )

# RM Performance Comparison
st.subheader("📊 RM Performance Comparison")

col1, col2 = st.columns(2)

with col1:
    # RM Pipeline Value Chart
    fig_rm_value = px.bar(
        rm_summary.sort_values('Pipeline Value', ascending=True),
        x='Pipeline Value',
        y='RM',
        orientation='h',
        title="Pipeline Value by RM",
        color='Pipeline Value',
        color_continuous_scale='viridis'
    )
    fig_rm_value.update_layout(height=400)
    st.plotly_chart(fig_rm_value, use_container_width=True)

with col2:
    # RM Deal Count vs Avg Probability
    fig_rm_scatter = px.scatter(
        rm_summary,
        x='Total Deals',
        y='Avg Probability',
        size='Weighted Value',
        color='RM',
        title="Deal Count vs Success Rate",
        hover_data=['Pipeline Value']
    )
    fig_rm_scatter.update_layout(height=400)
    st.plotly_chart(fig_rm_scatter, use_container_width=True)

# Pipeline Stage Distribution
st.subheader("🔄 Pipeline Stage Distribution")

# Calculate stage distribution across all RMs
stage_summary = pipeline_df.groupby(['stage', 'rm_name']).agg({
    'deal_id': 'count',
    'value': 'sum'
}).reset_index()

col1, col2 = st.columns(2)

with col1:
    # Stacked bar chart by RM and stage
    fig_stage_rm = px.bar(
        stage_summary,
        x='rm_name',
        y='deal_id',
        color='stage',
        title="Deal Distribution by RM and Stage",
        barmode='stack'
    )
    fig_stage_rm.update_xaxes(tickangle=45)
    st.plotly_chart(fig_stage_rm, use_container_width=True)

with col2:
    # Overall stage distribution
    overall_stages = pipeline_df.groupby('stage')['deal_id'].count().reset_index()
    fig_stage_pie = px.pie(
        overall_stages,
        values='deal_id',
        names='stage',
        title="Overall Stage Distribution"
    )
    st.plotly_chart(fig_stage_pie, use_container_width=True)

# RM Performance Cards
st.subheader("👤 Individual RM Performance")

# Create performance cards for each RM
for _, rm_data in rm_summary.iterrows():
    rm_deals = pipeline_df[pipeline_df['rm_name'] == rm_data['RM']]
    
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        
        with col1:
            # RM Info Card
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                text-align: center;
                margin: 10px 0;
            ">
                <h3 style="margin: 0; color: white;">👤 {rm_data['RM']}</h3>
                <p style="margin: 5px 0; font-size: 16px;">Relationship Manager</p>
                <p style="margin: 0; font-size: 14px;">📞 Active • 🎯 Target: £15M</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Deals", rm_data['Total Deals'])
            won_deals = len(rm_deals[rm_deals['stage'] == '🎉 Closed Won'])
            st.metric("Won", won_deals)
        
        with col3:
            st.metric("Pipeline", f"£{rm_data['Pipeline Value']/1000000:.1f}M")
            st.metric("Weighted", f"£{rm_data['Weighted Value']/1000000:.1f}M")
        
        with col4:
            st.metric("Avg Prob", f"{rm_data['Avg Probability']:.0f}%")
            avg_deal_size = rm_data['Pipeline Value'] / rm_data['Total Deals']
            st.metric("Avg Size", f"£{avg_deal_size/1000000:.1f}M")
        
        with col5:
            # Quick actions
            if st.button("📊 Details", key=f"details_{rm_data['RM']}"):
                st.success(f"Viewing {rm_data['RM']}'s detailed pipeline")
            if st.button("📞 Contact", key=f"contact_{rm_data['RM']}"):
                st.success(f"Contacting {rm_data['RM']}")
        
        # Mini pipeline for this RM
        rm_stages = rm_deals.groupby('stage')['deal_id'].count().reset_index()
        if not rm_stages.empty:
            fig_mini = px.bar(
                rm_stages,
                x='stage',
                y='deal_id',
                title=f"{rm_data['RM']}'s Pipeline Stages",
                height=200
            )
            fig_mini.update_layout(showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_mini, use_container_width=True)
        
        st.divider()

# Pipeline Workflow Visualization
st.subheader("🔄 Pipeline Workflow Analysis")

# Create workflow data
workflow_data = pipeline_df.groupby('stage').agg({
    'deal_id': 'count',
    'value': 'sum',
    'weighted_value': 'sum'
}).reset_index()

# Sort by logical stage order
stage_order = ['🔍 Prospect', '✅ Qualified', '📋 Proposal', '🤝 Negotiation', '🎉 Closed Won', '❌ Closed Lost']
workflow_data['stage_order'] = workflow_data['stage'].map({stage: i for i, stage in enumerate(stage_order)})
workflow_data = workflow_data.sort_values('stage_order')

col1, col2 = st.columns([2, 1])

with col1:
    # Funnel visualization
    fig_funnel = go.Figure()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    for i, row in workflow_data.iterrows():
        if row['stage'] not in ['🎉 Closed Won', '❌ Closed Lost']:  # Exclude closed deals from funnel
            fig_funnel.add_trace(go.Funnel(
                y=[row['stage']],
                x=[row['deal_id']],
                textinfo="value+percent initial",
                marker=dict(color=colors[i % len(colors)]),
                connector=dict(line=dict(color="royalblue", dash="dot", width=3))
            ))
    
    fig_funnel.update_layout(
        title="Active Pipeline Funnel",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    # Stage metrics
    for _, row in workflow_data.iterrows():
        conversion_rate = (row['deal_id'] / workflow_data['deal_id'].sum()) * 100
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 15px;
            border-radius: 10px;
            margin: 8px 0;
            color: white;
            text-align: center;
        ">
            <h4 style="margin: 0; color: white;">{row['stage']}</h4>
            <p style="margin: 5px 0; font-size: 18px; font-weight: bold;">{row['deal_id']} deals</p>
            <p style="margin: 0; font-size: 14px;">£{row['value']/1000000:.1f}M • {conversion_rate:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

# Analytics Tabs
tab1, tab2, tab3 = st.tabs(["📈 Trends", "🎯 Targets", "📊 Insights"])

with tab1:
    # Monthly trends
    pipeline_df['month'] = pipeline_df['created_date'].dt.to_period('M')
    monthly_trends = pipeline_df.groupby(['month', 'rm_name']).agg({
        'deal_id': 'count',
        'value': 'sum'
    }).reset_index()
    monthly_trends['month'] = monthly_trends['month'].astype(str)
    
    fig_trends = px.line(
        monthly_trends,
        x='month',
        y='value',
        color='rm_name',
        title="Monthly Pipeline Trends by RM"
    )
    st.plotly_chart(fig_trends, use_container_width=True)

with tab2:
    # Target vs Actual
    targets = {rm: random.randint(12000000, 20000000) for rm in rm_summary['RM']}
    rm_summary['Target'] = rm_summary['RM'].map(targets)
    rm_summary['Achievement'] = (rm_summary['Pipeline Value'] / rm_summary['Target']) * 100
    
    fig_targets = px.bar(
        rm_summary,
        x='RM',
        y=['Pipeline Value', 'Target'],
        title="Pipeline vs Targets",
        barmode='group'
    )
    st.plotly_chart(fig_targets, use_container_width=True)

with tab3:
    # Key insights
    st.markdown("### 🔍 Key Insights")
    
    top_performer = rm_summary.loc[rm_summary['Pipeline Value'].idxmax(), 'RM']
    highest_prob = rm_summary.loc[rm_summary['Avg Probability'].idxmax(), 'RM']
    most_deals = rm_summary.loc[rm_summary['Total Deals'].idxmax(), 'RM']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"🏆 **Top Performer**\n{top_performer}\n£{rm_summary.loc[rm_summary['RM'] == top_performer, 'Pipeline Value'].iloc[0]/1000000:.1f}M pipeline")
    
    with col2:
        st.success(f"🎯 **Highest Success Rate**\n{highest_prob}\n{rm_summary.loc[rm_summary['RM'] == highest_prob, 'Avg Probability'].iloc[0]:.0f}% avg probability")
    
    with col3:
        st.warning(f"📊 **Most Active**\n{most_deals}\n{rm_summary.loc[rm_summary['RM'] == most_deals, 'Total Deals'].iloc[0]} active deals")

st.markdown("""
---
**RM Pipeline Summary Features:**
- 🔄 Comprehensive RM performance comparison and analysis
- 📊 Interactive charts and visualizations for pipeline insights
- 👤 Individual RM performance cards with detailed metrics
- 🎯 Target tracking and achievement monitoring
- 📈 Trend analysis and forecasting capabilities
""")

