import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Risk Management",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Risk Management")
st.markdown("Real-time risk assessment and monitoring")

# Generate sample risk data
@st.cache_data
def generate_risk_data():
    clients = []
    for i in range(100):
        client = {
            'client_id': f'CLI-{1000 + i}',
            'client_name': f'Client {chr(65 + i % 26)}{i}',
            'industry': random.choice(['Technology', 'Manufacturing', 'Healthcare', 'Retail', 'Energy', 'Finance']),
            'credit_rating': random.choice(['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC']),
            'risk_score': random.uniform(1, 10),
            'probability_default': random.uniform(0.01, 0.15),
            'exposure_amount': random.uniform(1000000, 50000000),
            'collateral_value': random.uniform(500000, 30000000),
            'debt_to_equity': random.uniform(0.2, 3.0),
            'current_ratio': random.uniform(0.8, 2.5),
            'cash_flow_ratio': random.uniform(-0.2, 0.4),
            'revenue_growth': random.uniform(-0.3, 0.5),
            'last_review_date': datetime.now() - timedelta(days=random.randint(1, 365)),
            'next_review_date': datetime.now() + timedelta(days=random.randint(30, 180)),
            'risk_trend': random.choice(['Improving', 'Stable', 'Deteriorating']),
            'covenant_status': random.choice(['Compliant', 'Warning', 'Breach']),
            'relationship_manager': random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams', 'David Brown'])
        }
        clients.append(client)
    
    return pd.DataFrame(clients)

risk_df = generate_risk_data()

# Risk overview metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_exposure = risk_df['exposure_amount'].sum()
    st.metric(
        label="💰 Total Exposure",
        value=f"£{total_exposure/1000000:.1f}M",
        delta="2.3%"
    )

with col2:
    avg_risk_score = risk_df['risk_score'].mean()
    st.metric(
        label="📊 Avg Risk Score",
        value=f"{avg_risk_score:.1f}/10",
        delta="-0.2"
    )

with col3:
    high_risk_count = len(risk_df[risk_df['risk_score'] > 7])
    st.metric(
        label="⚠️ High Risk Clients",
        value=high_risk_count,
        delta="-3"
    )

with col4:
    covenant_breaches = len(risk_df[risk_df['covenant_status'] == 'Breach'])
    st.metric(
        label="🚨 Covenant Breaches",
        value=covenant_breaches,
        delta="+1"
    )

# Risk dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Risk Distribution")
    
    # Risk score distribution
    risk_bins = pd.cut(risk_df['risk_score'], bins=[0, 3, 5, 7, 10], labels=['Low', 'Medium', 'High', 'Critical'])
    risk_counts = risk_bins.value_counts()
    
    fig_risk_dist = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Risk Score Distribution",
        color_discrete_map={
            'Low': '#28a745',
            'Medium': '#ffc107',
            'High': '#fd7e14',
            'Critical': '#dc3545'
        }
    )
    st.plotly_chart(fig_risk_dist, use_container_width=True)

with col2:
    st.subheader("📈 Risk vs Exposure")
    
    # Risk score vs exposure scatter plot
    fig_scatter = px.scatter(
        risk_df,
        x='risk_score',
        y='exposure_amount',
        color='industry',
        size='probability_default',
        title="Risk Score vs Exposure Amount",
        labels={
            'risk_score': 'Risk Score',
            'exposure_amount': 'Exposure Amount (£)',
            'probability_default': 'Default Probability'
        }
    )
    fig_scatter.update_layout(yaxis_tickformat='£,.0f')
    st.plotly_chart(fig_scatter, use_container_width=True)

# Risk filters
st.subheader("🔍 Risk Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    industry_filter = st.multiselect(
        "Industry",
        options=risk_df['industry'].unique(),
        default=risk_df['industry'].unique()
    )

with col2:
    risk_level_filter = st.multiselect(
        "Risk Level",
        options=['Low', 'Medium', 'High', 'Critical'],
        default=['High', 'Critical']
    )

with col3:
    covenant_filter = st.multiselect(
        "Covenant Status",
        options=risk_df['covenant_status'].unique(),
        default=risk_df['covenant_status'].unique()
    )

with col4:
    min_exposure = st.number_input(
        "Min Exposure (£M)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=1.0
    )

# Apply filters
risk_bins = pd.cut(risk_df['risk_score'], bins=[0, 3, 5, 7, 10], labels=['Low', 'Medium', 'High', 'Critical'])
risk_df['risk_level'] = risk_bins

filtered_risk_df = risk_df[
    (risk_df['industry'].isin(industry_filter)) &
    (risk_df['risk_level'].isin(risk_level_filter)) &
    (risk_df['covenant_status'].isin(covenant_filter)) &
    (risk_df['exposure_amount'] >= min_exposure * 1000000)
]

# Risk monitoring table
st.subheader("📋 Risk Monitoring Dashboard")

# Prepare display dataframe
display_risk_df = filtered_risk_df.copy()
display_risk_df['Exposure (£M)'] = (display_risk_df['exposure_amount'] / 1000000).round(2)
display_risk_df['PD (%)'] = (display_risk_df['probability_default'] * 100).round(2)
display_risk_df['Risk Score'] = display_risk_df['risk_score'].round(1)
display_risk_df['D/E Ratio'] = display_risk_df['debt_to_equity'].round(2)
display_risk_df['Current Ratio'] = display_risk_df['current_ratio'].round(2)

# Risk trend indicators
def get_trend_indicator(trend):
    if trend == 'Improving':
        return '📈 Improving'
    elif trend == 'Deteriorating':
        return '📉 Deteriorating'
    else:
        return '➡️ Stable'

display_risk_df['Trend'] = display_risk_df['risk_trend'].apply(get_trend_indicator)

# Covenant status indicators
def get_covenant_indicator(status):
    if status == 'Compliant':
        return '✅ Compliant'
    elif status == 'Warning':
        return '⚠️ Warning'
    else:
        return '🚨 Breach'

display_risk_df['Covenant'] = display_risk_df['covenant_status'].apply(get_covenant_indicator)

# Select columns for display
risk_columns = [
    'client_name', 'industry', 'credit_rating', 'Risk Score', 
    'Exposure (£M)', 'PD (%)', 'D/E Ratio', 'Current Ratio',
    'Trend', 'Covenant', 'relationship_manager'
]

st.dataframe(
    display_risk_df[risk_columns],
    use_container_width=True,
    column_config={
        "client_name": "Client Name",
        "industry": "Industry",
        "credit_rating": "Credit Rating",
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score",
            min_value=0,
            max_value=10,
            format="%.1f"
        ),
        "Exposure (£M)": st.column_config.NumberColumn(
            "Exposure (£M)",
            format="£%.2f"
        ),
        "PD (%)": st.column_config.NumberColumn(
            "PD (%)",
            format="%.2f%%"
        ),
        "relationship_manager": "RM"
    }
)

# Risk analytics
st.subheader("📊 Risk Analytics")

tab1, tab2, tab3, tab4 = st.tabs(["🏭 Industry Analysis", "📈 Trend Analysis", "🎯 Portfolio Metrics", "🚨 Alert System"])

with tab1:
    st.markdown("**🏭 Industry Risk Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Industry risk distribution
        industry_risk = filtered_risk_df.groupby('industry').agg({
            'risk_score': 'mean',
            'exposure_amount': 'sum',
            'probability_default': 'mean'
        }).reset_index()
        
        industry_risk['exposure_millions'] = industry_risk['exposure_amount'] / 1000000
        
        fig_industry_risk = px.bar(
            industry_risk,
            x='industry',
            y='risk_score',
            title="Average Risk Score by Industry"
        )
        st.plotly_chart(fig_industry_risk, use_container_width=True)
    
    with col2:
        # Industry exposure
        fig_industry_exposure = px.bar(
            industry_risk,
            x='industry',
            y='exposure_millions',
            title="Total Exposure by Industry (£M)"
        )
        st.plotly_chart(fig_industry_exposure, use_container_width=True)
    
    # Industry risk matrix
    st.markdown("**Industry Risk Matrix**")
    
    industry_matrix = filtered_risk_df.groupby(['industry', 'risk_level']).size().unstack(fill_value=0)
    
    fig_matrix = px.imshow(
        industry_matrix.values,
        x=industry_matrix.columns,
        y=industry_matrix.index,
        title="Industry vs Risk Level Matrix",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

with tab2:
    st.markdown("**📈 Risk Trend Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk trend distribution
        trend_counts = filtered_risk_df['risk_trend'].value_counts()
        
        fig_trends = px.pie(
            values=trend_counts.values,
            names=trend_counts.index,
            title="Risk Trend Distribution",
            color_discrete_map={
                'Improving': '#28a745',
                'Stable': '#6c757d',
                'Deteriorating': '#dc3545'
            }
        )
        st.plotly_chart(fig_trends, use_container_width=True)
    
    with col2:
        # Covenant status distribution
        covenant_counts = filtered_risk_df['covenant_status'].value_counts()
        
        fig_covenant = px.bar(
            x=covenant_counts.index,
            y=covenant_counts.values,
            title="Covenant Status Distribution",
            color=covenant_counts.index,
            color_discrete_map={
                'Compliant': '#28a745',
                'Warning': '#ffc107',
                'Breach': '#dc3545'
            }
        )
        st.plotly_chart(fig_covenant, use_container_width=True)
    
    # Risk migration analysis
    st.markdown("**Risk Migration Analysis**")
    
    # Simulate risk migration data
    migration_data = pd.DataFrame({
        'From_Rating': ['AAA', 'AA', 'A', 'BBB', 'BB', 'B'],
        'To_AAA': [95, 2, 0, 0, 0, 0],
        'To_AA': [3, 90, 5, 1, 0, 0],
        'To_A': [2, 7, 85, 8, 2, 0],
        'To_BBB': [0, 1, 8, 80, 10, 3],
        'To_BB': [0, 0, 2, 10, 75, 15],
        'To_B': [0, 0, 0, 1, 13, 82]
    })
    
    st.dataframe(migration_data, use_container_width=True)

with tab3:
    st.markdown("**🎯 Portfolio Risk Metrics**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Value at Risk
        var_95 = np.percentile(filtered_risk_df['exposure_amount'] * filtered_risk_df['probability_default'], 95)
        st.metric(
            label="📊 VaR (95%)",
            value=f"£{var_95/1000000:.1f}M",
            delta="↓ 5.2%"
        )
        
        # Expected Loss
        expected_loss = (filtered_risk_df['exposure_amount'] * filtered_risk_df['probability_default']).sum()
        st.metric(
            label="💸 Expected Loss",
            value=f"£{expected_loss/1000000:.1f}M",
            delta="↓ 2.1%"
        )
    
    with col2:
        # Concentration risk
        top_5_exposure = filtered_risk_df.nlargest(5, 'exposure_amount')['exposure_amount'].sum()
        concentration_ratio = (top_5_exposure / filtered_risk_df['exposure_amount'].sum()) * 100
        
        st.metric(
            label="🎯 Concentration (Top 5)",
            value=f"{concentration_ratio:.1f}%",
            delta="↑ 1.3%"
        )
        
        # Portfolio diversity
        industry_count = filtered_risk_df['industry'].nunique()
        st.metric(
            label="🌐 Industry Diversity",
            value=f"{industry_count} sectors",
            delta="Stable"
        )
    
    with col3:
        # Risk-adjusted return
        portfolio_return = 0.085  # 8.5% assumed return
        portfolio_risk = filtered_risk_df['risk_score'].mean()
        risk_adjusted_return = portfolio_return / (portfolio_risk / 10)
        
        st.metric(
            label="📈 Risk-Adj Return",
            value=f"{risk_adjusted_return:.2f}",
            delta="↑ 0.15"
        )
        
        # Capital adequacy
        capital_ratio = 0.125  # 12.5% assumed
        st.metric(
            label="🏛️ Capital Ratio",
            value=f"{capital_ratio:.1%}",
            delta="↑ 0.5%"
        )
    
    # Risk correlation matrix
    st.markdown("**Risk Factor Correlation Matrix**")
    
    correlation_factors = ['risk_score', 'debt_to_equity', 'current_ratio', 'cash_flow_ratio', 'revenue_growth']
    correlation_matrix = filtered_risk_df[correlation_factors].corr()
    
    fig_corr = px.imshow(
        correlation_matrix,
        title="Risk Factor Correlation Matrix",
        color_continuous_scale="RdBu",
        aspect="auto"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

with tab4:
    st.markdown("**🚨 Risk Alert System**")
    
    # Generate risk alerts
    alerts = []
    
    # High risk score alerts
    high_risk_clients = filtered_risk_df[filtered_risk_df['risk_score'] > 8]
    for _, client in high_risk_clients.iterrows():
        alerts.append({
            'severity': 'Critical',
            'type': 'High Risk Score',
            'client': client['client_name'],
            'message': f"Risk score {client['risk_score']:.1f}/10 - Immediate review required",
            'timestamp': datetime.now() - timedelta(hours=random.randint(1, 24))
        })
    
    # Covenant breach alerts
    breach_clients = filtered_risk_df[filtered_risk_df['covenant_status'] == 'Breach']
    for _, client in breach_clients.iterrows():
        alerts.append({
            'severity': 'High',
            'type': 'Covenant Breach',
            'client': client['client_name'],
            'message': f"Covenant breach detected - Legal action may be required",
            'timestamp': datetime.now() - timedelta(hours=random.randint(1, 48))
        })
    
    # Deteriorating trend alerts
    deteriorating_clients = filtered_risk_df[filtered_risk_df['risk_trend'] == 'Deteriorating']
    for _, client in deteriorating_clients.head(5).iterrows():
        alerts.append({
            'severity': 'Medium',
            'type': 'Deteriorating Trend',
            'client': client['client_name'],
            'message': f"Risk trend deteriorating - Enhanced monitoring recommended",
            'timestamp': datetime.now() - timedelta(hours=random.randint(1, 72))
        })
    
    # Sort alerts by severity and timestamp
    severity_order = {'Critical': 3, 'High': 2, 'Medium': 1}
    alerts.sort(key=lambda x: (severity_order[x['severity']], x['timestamp']), reverse=True)
    
    # Display alerts
    for alert in alerts[:10]:  # Show top 10 alerts
        severity_color = {
            'Critical': '#dc3545',
            'High': '#fd7e14',
            'Medium': '#ffc107'
        }
        
        severity_icon = {
            'Critical': '🚨',
            'High': '⚠️',
            'Medium': '⚡'
        }
        
        st.markdown(f"""
        <div style="border-left: 4px solid {severity_color[alert['severity']]}; padding: 15px; margin: 10px 0; background-color: #f8f9fa;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{severity_icon[alert['severity']]} {alert['severity']} - {alert['type']}</strong><br>
                    <strong>Client:</strong> {alert['client']}<br>
                    <em>{alert['message']}</em>
                </div>
                <div style="text-align: right; font-size: 0.9em; color: #666;">
                    {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Alert configuration
    st.markdown("**Alert Configuration**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Risk Score Thresholds**")
        critical_threshold = st.slider("Critical Alert", 7.0, 10.0, 8.0, 0.1)
        high_threshold = st.slider("High Alert", 5.0, 8.0, 6.5, 0.1)
        medium_threshold = st.slider("Medium Alert", 3.0, 6.0, 5.0, 0.1)
    
    with col2:
        st.markdown("**Notification Settings**")
        email_alerts = st.checkbox("Email Alerts", value=True)
        sms_alerts = st.checkbox("SMS Alerts", value=False)
        dashboard_alerts = st.checkbox("Dashboard Alerts", value=True)
        
        alert_frequency = st.selectbox(
            "Alert Frequency",
            options=["Immediate", "Hourly", "Daily", "Weekly"]
        )
    
    if st.button("💾 Save Alert Settings"):
        st.success("Alert settings saved successfully!")

# Risk reporting
st.subheader("📊 Risk Reporting")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Generate Risk Report"):
        st.success("Comprehensive risk report generated!")

with col2:
    if st.button("📧 Email Risk Summary"):
        st.success("Risk summary emailed to stakeholders!")

with col3:
    if st.button("📊 Export Risk Data"):
        st.success("Risk data exported to Excel!")

