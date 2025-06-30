import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Advanced Analytics")
st.markdown("Business intelligence and performance metrics")

# Generate comprehensive analytics data
@st.cache_data
def generate_analytics_data():
    # Performance data
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    performance_data = []
    
    for date in dates:
        performance_data.append({
            'date': date,
            'revenue': random.uniform(800000, 1200000),
            'new_clients': random.randint(2, 8),
            'deals_closed': random.randint(1, 5),
            'pipeline_value': random.uniform(50000000, 80000000),
            'client_satisfaction': random.uniform(7.5, 9.5),
            'operational_efficiency': random.uniform(0.75, 0.95),
            'risk_score': random.uniform(3.0, 7.0),
            'market_share': random.uniform(0.12, 0.18)
        })
    
    return pd.DataFrame(performance_data)

analytics_df = generate_analytics_data()

# Key performance indicators
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_revenue = analytics_df['revenue'].sum()
    revenue_growth = ((analytics_df['revenue'].tail(30).mean() / analytics_df['revenue'].head(30).mean()) - 1) * 100
    st.metric(
        label="💰 Total Revenue",
        value=f"£{total_revenue/1000000:.1f}M",
        delta=f"{revenue_growth:.1f}%"
    )

with col2:
    total_clients = analytics_df['new_clients'].sum()
    client_growth = ((analytics_df['new_clients'].tail(30).sum() / analytics_df['new_clients'].head(30).sum()) - 1) * 100
    st.metric(
        label="👥 New Clients",
        value=total_clients,
        delta=f"{client_growth:.1f}%"
    )

with col3:
    total_deals = analytics_df['deals_closed'].sum()
    deal_growth = ((analytics_df['deals_closed'].tail(30).sum() / analytics_df['deals_closed'].head(30).sum()) - 1) * 100
    st.metric(
        label="🤝 Deals Closed",
        value=total_deals,
        delta=f"{deal_growth:.1f}%"
    )

with col4:
    avg_satisfaction = analytics_df['client_satisfaction'].mean()
    satisfaction_trend = analytics_df['client_satisfaction'].tail(30).mean() - analytics_df['client_satisfaction'].head(30).mean()
    st.metric(
        label="😊 Client Satisfaction",
        value=f"{avg_satisfaction:.1f}/10",
        delta=f"{satisfaction_trend:.2f}"
    )

with col5:
    avg_efficiency = analytics_df['operational_efficiency'].mean()
    efficiency_trend = analytics_df['operational_efficiency'].tail(30).mean() - analytics_df['operational_efficiency'].head(30).mean()
    st.metric(
        label="⚡ Operational Efficiency",
        value=f"{avg_efficiency:.1%}",
        delta=f"{efficiency_trend:.2%}"
    )

# Analytics dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Performance", "👥 Client Analytics", "💼 Deal Analytics", "🎯 Predictive", "📊 Custom Reports"])

with tab1:
    st.subheader("📈 Performance Analytics")
    
    # Time period selector
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**Performance Overview**")
    
    with col2:
        time_period = st.selectbox(
            "Time Period",
            options=["Last 30 days", "Last 90 days", "Last 6 months", "Year to date"],
            index=2
        )
    
    # Filter data based on time period
    if time_period == "Last 30 days":
        filtered_data = analytics_df.tail(30)
    elif time_period == "Last 90 days":
        filtered_data = analytics_df.tail(90)
    elif time_period == "Last 6 months":
        filtered_data = analytics_df.tail(180)
    else:
        filtered_data = analytics_df
    
    # Revenue trend
    col1, col2 = st.columns(2)
    
    with col1:
        fig_revenue = px.line(
            filtered_data,
            x='date',
            y='revenue',
            title="Daily Revenue Trend"
        )
        fig_revenue.update_layout(yaxis_tickformat='£,.0f')
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Monthly revenue aggregation
        monthly_revenue = filtered_data.groupby(filtered_data['date'].dt.to_period('M'))['revenue'].sum().reset_index()
        monthly_revenue['date'] = monthly_revenue['date'].astype(str)
        monthly_revenue['revenue_millions'] = monthly_revenue['revenue'] / 1000000
        
        fig_monthly = px.bar(
            monthly_revenue,
            x='date',
            y='revenue_millions',
            title="Monthly Revenue (£M)"
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Performance correlation matrix
    st.markdown("**Performance Correlation Analysis**")
    
    correlation_cols = ['revenue', 'new_clients', 'deals_closed', 'client_satisfaction', 'operational_efficiency']
    correlation_matrix = filtered_data[correlation_cols].corr()
    
    fig_corr = px.imshow(
        correlation_matrix,
        title="Performance Metrics Correlation",
        color_continuous_scale="RdBu",
        aspect="auto"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Performance benchmarks
    st.markdown("**Performance Benchmarks**")
    
    benchmarks = pd.DataFrame({
        'Metric': ['Revenue Growth', 'Client Acquisition', 'Deal Closure Rate', 'Client Satisfaction', 'Operational Efficiency'],
        'Current': [f"{revenue_growth:.1f}%", f"{client_growth:.1f}%", f"{deal_growth:.1f}%", f"{avg_satisfaction:.1f}/10", f"{avg_efficiency:.1%}"],
        'Target': ["15.0%", "20.0%", "25.0%", "8.5/10", "90.0%"],
        'Industry Avg': ["12.5%", "18.0%", "22.0%", "8.2/10", "85.0%"],
        'Status': ["✅ Above Target", "⚠️ Below Target", "⚠️ Below Target", "✅ Above Target", "✅ Above Target"]
    })
    
    st.dataframe(benchmarks, use_container_width=True)

with tab2:
    st.subheader("👥 Client Analytics")
    
    # Generate client analytics data
    @st.cache_data
    def generate_client_analytics():
        industries = ['Technology', 'Healthcare', 'Manufacturing', 'Retail', 'Energy', 'Finance']
        regions = ['London', 'Manchester', 'Birmingham', 'Edinburgh', 'Cardiff']
        
        client_data = []
        for i in range(200):
            client_data.append({
                'client_id': f'CLI-{1000 + i}',
                'industry': random.choice(industries),
                'region': random.choice(regions),
                'revenue_contribution': random.uniform(100000, 5000000),
                'relationship_length': random.randint(1, 15),
                'satisfaction_score': random.uniform(6.0, 10.0),
                'products_used': random.randint(1, 8),
                'last_interaction': datetime.now() - timedelta(days=random.randint(1, 90)),
                'growth_potential': random.choice(['High', 'Medium', 'Low']),
                'risk_level': random.choice(['Low', 'Medium', 'High'])
            })
        
        return pd.DataFrame(client_data)
    
    client_analytics_df = generate_client_analytics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Client distribution by industry
        industry_revenue = client_analytics_df.groupby('industry')['revenue_contribution'].sum().reset_index()
        industry_revenue['revenue_millions'] = industry_revenue['revenue_contribution'] / 1000000
        
        fig_industry = px.pie(
            industry_revenue,
            values='revenue_millions',
            names='industry',
            title="Revenue Distribution by Industry"
        )
        st.plotly_chart(fig_industry, use_container_width=True)
    
    with col2:
        # Client satisfaction by industry
        satisfaction_by_industry = client_analytics_df.groupby('industry')['satisfaction_score'].mean().reset_index()
        
        fig_satisfaction = px.bar(
            satisfaction_by_industry,
            x='industry',
            y='satisfaction_score',
            title="Average Satisfaction by Industry"
        )
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    
    # Client segmentation analysis
    st.markdown("**Client Segmentation Analysis**")
    
    # Create client segments based on revenue and relationship length
    client_analytics_df['segment'] = 'Standard'
    client_analytics_df.loc[
        (client_analytics_df['revenue_contribution'] > 1000000) & 
        (client_analytics_df['relationship_length'] > 5), 'segment'
    ] = 'Premium'
    client_analytics_df.loc[
        (client_analytics_df['revenue_contribution'] > 2000000) & 
        (client_analytics_df['relationship_length'] > 10), 'segment'
    ] = 'Elite'
    
    segment_analysis = client_analytics_df.groupby('segment').agg({
        'client_id': 'count',
        'revenue_contribution': ['sum', 'mean'],
        'satisfaction_score': 'mean',
        'products_used': 'mean'
    }).round(2)
    
    segment_analysis.columns = ['Client Count', 'Total Revenue', 'Avg Revenue', 'Avg Satisfaction', 'Avg Products']
    segment_analysis['Total Revenue'] = segment_analysis['Total Revenue'] / 1000000
    segment_analysis['Avg Revenue'] = segment_analysis['Avg Revenue'] / 1000000
    
    st.dataframe(segment_analysis, use_container_width=True)
    
    # Client lifecycle analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Relationship length distribution
        fig_relationship = px.histogram(
            client_analytics_df,
            x='relationship_length',
            title="Client Relationship Length Distribution",
            nbins=15
        )
        st.plotly_chart(fig_relationship, use_container_width=True)
    
    with col2:
        # Growth potential analysis
        growth_counts = client_analytics_df['growth_potential'].value_counts()
        
        fig_growth = px.bar(
            x=growth_counts.index,
            y=growth_counts.values,
            title="Client Growth Potential Distribution",
            color=growth_counts.index,
            color_discrete_map={
                'High': '#28a745',
                'Medium': '#ffc107',
                'Low': '#dc3545'
            }
        )
        st.plotly_chart(fig_growth, use_container_width=True)

with tab3:
    st.subheader("💼 Deal Analytics")
    
    # Generate deal analytics data
    @st.cache_data
    def generate_deal_analytics():
        deal_types = ['Term Loan', 'Credit Line', 'Trade Finance', 'Treasury Services', 'Equipment Finance']
        stages = ['Prospect', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
        
        deal_data = []
        for i in range(300):
            deal_data.append({
                'deal_id': f'DEAL-{2000 + i}',
                'deal_type': random.choice(deal_types),
                'deal_value': random.uniform(500000, 20000000),
                'stage': random.choice(stages),
                'probability': random.uniform(10, 95),
                'days_in_pipeline': random.randint(1, 365),
                'rm_name': random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams', 'David Brown', 'Lisa Davis']),
                'industry': random.choice(['Technology', 'Healthcare', 'Manufacturing', 'Retail', 'Energy']),
                'created_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'expected_close': datetime.now() + timedelta(days=random.randint(1, 180)),
                'actual_close': datetime.now() - timedelta(days=random.randint(1, 30)) if random.random() > 0.7 else None
            })
        
        return pd.DataFrame(deal_data)
    
    deal_analytics_df = generate_deal_analytics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Deal value by type
        deal_value_by_type = deal_analytics_df.groupby('deal_type')['deal_value'].sum().reset_index()
        deal_value_by_type['deal_value_millions'] = deal_value_by_type['deal_value'] / 1000000
        
        fig_deal_value = px.bar(
            deal_value_by_type,
            x='deal_type',
            y='deal_value_millions',
            title="Total Deal Value by Type (£M)"
        )
        st.plotly_chart(fig_deal_value, use_container_width=True)
    
    with col2:
        # Deal conversion funnel
        stage_order = ['Prospect', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
        funnel_data = deal_analytics_df['stage'].value_counts().reindex(stage_order, fill_value=0)
        
        fig_funnel = px.funnel(
            x=funnel_data.values,
            y=funnel_data.index,
            title="Deal Conversion Funnel"
        )
        st.plotly_chart(fig_funnel, use_container_width=True)
    
    # RM performance analysis
    st.markdown("**Relationship Manager Performance**")
    
    rm_performance = deal_analytics_df.groupby('rm_name').agg({
        'deal_id': 'count',
        'deal_value': ['sum', 'mean'],
        'probability': 'mean',
        'days_in_pipeline': 'mean'
    }).round(2)
    
    rm_performance.columns = ['Deal Count', 'Total Value', 'Avg Deal Size', 'Avg Probability', 'Avg Days in Pipeline']
    rm_performance['Total Value'] = rm_performance['Total Value'] / 1000000
    rm_performance['Avg Deal Size'] = rm_performance['Avg Deal Size'] / 1000000
    
    st.dataframe(rm_performance, use_container_width=True)
    
    # Deal velocity analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Average days in pipeline by stage
        pipeline_days = deal_analytics_df.groupby('stage')['days_in_pipeline'].mean().reset_index()
        
        fig_velocity = px.bar(
            pipeline_days,
            x='stage',
            y='days_in_pipeline',
            title="Average Days in Pipeline by Stage"
        )
        st.plotly_chart(fig_velocity, use_container_width=True)
    
    with col2:
        # Win rate by industry
        closed_deals = deal_analytics_df[deal_analytics_df['stage'].isin(['Closed Won', 'Closed Lost'])]
        win_rate_by_industry = closed_deals.groupby('industry').apply(
            lambda x: (x['stage'] == 'Closed Won').sum() / len(x) * 100
        ).reset_index(name='win_rate')
        
        fig_win_rate = px.bar(
            win_rate_by_industry,
            x='industry',
            y='win_rate',
            title="Win Rate by Industry (%)"
        )
        st.plotly_chart(fig_win_rate, use_container_width=True)

with tab4:
    st.subheader("🎯 Predictive Analytics")
    
    # Revenue forecasting
    st.markdown("**Revenue Forecasting**")
    
    # Generate forecast data
    historical_revenue = analytics_df['revenue'].values
    
    # Simple trend-based forecast
    trend = np.polyfit(range(len(historical_revenue)), historical_revenue, 1)
    forecast_days = 90
    forecast_dates = pd.date_range(start=analytics_df['date'].max() + timedelta(days=1), periods=forecast_days, freq='D')
    
    forecast_values = []
    for i in range(forecast_days):
        base_forecast = trend[0] * (len(historical_revenue) + i) + trend[1]
        # Add some seasonality and noise
        seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * i / 30)  # Monthly seasonality
        noise = random.uniform(0.9, 1.1)
        forecast_values.append(base_forecast * seasonal_factor * noise)
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'revenue': forecast_values,
        'type': 'Forecast'
    })
    
    # Combine historical and forecast data
    historical_df = analytics_df[['date', 'revenue']].copy()
    historical_df['type'] = 'Historical'
    
    combined_df = pd.concat([historical_df.tail(60), forecast_df], ignore_index=True)
    
    fig_forecast = px.line(
        combined_df,
        x='date',
        y='revenue',
        color='type',
        title="Revenue Forecast (Next 90 Days)"
    )
    fig_forecast.update_layout(yaxis_tickformat='£,.0f')
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Predictive insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Predictive Insights**")
        
        insights = [
            {
                "metric": "Revenue Growth",
                "prediction": "+12.5%",
                "confidence": "85%",
                "timeframe": "Next Quarter"
            },
            {
                "metric": "Client Acquisition",
                "prediction": "45 new clients",
                "confidence": "78%",
                "timeframe": "Next Month"
            },
            {
                "metric": "Deal Closure",
                "prediction": "£25M pipeline",
                "confidence": "92%",
                "timeframe": "Next 60 days"
            },
            {
                "metric": "Risk Score",
                "prediction": "Stable at 4.2",
                "confidence": "88%",
                "timeframe": "Next Quarter"
            }
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 8px;">
                <strong>{insight['metric']}</strong><br>
                <span style="color: #007bff; font-size: 1.2em;">{insight['prediction']}</span><br>
                <small>Confidence: {insight['confidence']} | {insight['timeframe']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Model Performance**")
        
        model_metrics = pd.DataFrame({
            'Model': ['Revenue Forecast', 'Client Churn', 'Deal Success', 'Risk Prediction'],
            'Accuracy': [87.5, 82.3, 79.8, 91.2],
            'Precision': [85.2, 78.9, 83.1, 89.7],
            'Recall': [89.1, 85.6, 76.4, 92.8],
            'F1-Score': [87.1, 82.1, 79.6, 91.2]
        })
        
        st.dataframe(model_metrics, use_container_width=True)
        
        # Model accuracy trend
        accuracy_trend = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Accuracy': [82.1, 84.3, 85.7, 86.9, 87.2, 87.5]
        })
        
        fig_accuracy = px.line(
            accuracy_trend,
            x='Month',
            y='Accuracy',
            title="Model Accuracy Trend (%)"
        )
        st.plotly_chart(fig_accuracy, use_container_width=True)

with tab5:
    st.subheader("📊 Custom Reports")
    
    st.markdown("**Report Builder**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Report Configuration**")
        
        report_type = st.selectbox(
            "Report Type",
            options=["Executive Summary", "Client Analysis", "Deal Performance", "Risk Assessment", "Custom"]
        )
        
        date_range = st.date_input(
            "Date Range",
            value=[datetime.now() - timedelta(days=30), datetime.now()],
            max_value=datetime.now()
        )
        
        metrics = st.multiselect(
            "Metrics to Include",
            options=["Revenue", "Client Count", "Deal Value", "Risk Score", "Satisfaction", "Efficiency"],
            default=["Revenue", "Client Count", "Deal Value"]
        )
        
        grouping = st.selectbox(
            "Group By",
            options=["Daily", "Weekly", "Monthly", "Quarterly"]
        )
        
        format_type = st.selectbox(
            "Export Format",
            options=["PDF", "Excel", "PowerPoint", "CSV"]
        )
    
    with col2:
        st.markdown("**Report Preview**")
        
        # Generate sample report data based on selections
        if len(date_range) == 2:
            start_date, end_date = date_range
            preview_data = analytics_df[
                (analytics_df['date'] >= pd.Timestamp(start_date)) &
                (analytics_df['date'] <= pd.Timestamp(end_date))
            ]
            
            if grouping == "Weekly":
                preview_data = preview_data.groupby(preview_data['date'].dt.to_period('W')).agg({
                    'revenue': 'sum',
                    'new_clients': 'sum',
                    'deals_closed': 'sum'
                }).reset_index()
            elif grouping == "Monthly":
                preview_data = preview_data.groupby(preview_data['date'].dt.to_period('M')).agg({
                    'revenue': 'sum',
                    'new_clients': 'sum',
                    'deals_closed': 'sum'
                }).reset_index()
            
            # Show preview chart
            if "Revenue" in metrics:
                fig_preview = px.line(
                    preview_data.head(20),
                    x='date',
                    y='revenue',
                    title=f"Revenue Trend - {grouping} View"
                )
                st.plotly_chart(fig_preview, use_container_width=True)
    
    # Report generation buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generate Report"):
            st.success(f"{report_type} report generated successfully!")
    
    with col2:
        if st.button("📧 Email Report"):
            st.success("Report emailed to stakeholders!")
    
    with col3:
        if st.button("📅 Schedule Report"):
            st.success("Report scheduled for automatic generation!")
    
    # Saved reports
    st.markdown("**Saved Reports**")
    
    saved_reports = pd.DataFrame({
        'Report Name': ['Q2 Executive Summary', 'Client Performance Analysis', 'Monthly Risk Report', 'Deal Pipeline Review'],
        'Type': ['Executive Summary', 'Client Analysis', 'Risk Assessment', 'Deal Performance'],
        'Created': ['2024-06-30', '2024-06-28', '2024-06-25', '2024-06-22'],
        'Status': ['Ready', 'Ready', 'Ready', 'Ready']
    })
    
    st.dataframe(
        saved_reports,
        use_container_width=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                options=["Ready", "Generating", "Error"]
            )
        }
    )

# Analytics insights
st.subheader("🧠 Analytics Insights")

insights = [
    {
        "category": "Performance",
        "insight": "Revenue growth accelerated 15% in Q2, driven by technology sector expansion",
        "impact": "High",
        "action": "Increase technology sector focus and resource allocation"
    },
    {
        "category": "Client Behavior",
        "insight": "Premium clients show 40% higher product adoption rates",
        "impact": "Medium",
        "action": "Develop targeted premium client engagement programs"
    },
    {
        "category": "Deal Pipeline",
        "insight": "Healthcare deals have shortest sales cycles (avg 45 days vs 67 days overall)",
        "impact": "Medium",
        "action": "Apply healthcare sales methodology to other sectors"
    },
    {
        "category": "Risk Management",
        "insight": "Early warning indicators predict 85% of potential defaults 90 days in advance",
        "impact": "High",
        "action": "Implement automated early warning alert system"
    }
]

for insight in insights:
    impact_color = {"High": "#28a745", "Medium": "#ffc107", "Low": "#508630"}
    
    st.markdown(f"""
    <div style="border-left: 4px solid {impact_color[insight['impact']]}; padding: 15px; margin: 10px 0; background-color: #508630;">
        <strong>{insight['category']}</strong> - <span style="color: {impact_color[insight['impact']]};">{insight['impact']} Impact</span><br>
        <em>{insight['insight']}</em><br>
        <strong>Recommended Action:</strong> {insight['action']}
    </div>
    """, unsafe_allow_html=True)

