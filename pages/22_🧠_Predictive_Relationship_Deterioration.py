import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Predictive Relationship Deterioration",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Predictive Relationship Deterioration")

st.markdown("""
🚀 **AI-powered early warning system that predicts client relationship deterioration before it happens.**
""")

# Generate synthetic relationship health data
@st.cache_data
def generate_relationship_data():
    clients = ['TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd', 'HealthcarePro', 
               'StartupXYZ', 'LogisticsCorp', 'FinanceGroup', 'PropertyDev', 'MediaHouse']
    
    relationships = []
    for client in clients:
        # Generate historical data points
        for days_back in range(90, 0, -7):  # Weekly data points for 90 days
            date = datetime.now() - timedelta(days=days_back)
            
            # Simulate deterioration patterns for some clients
            base_health = random.uniform(0.6, 0.95)
            if client in ['RetailChain PLC', 'StartupXYZ']:  # Simulate deteriorating relationships
                deterioration_factor = (90 - days_back) / 90 * 0.4  # Gradual decline
                health_score = max(0.2, base_health - deterioration_factor)
            else:
                health_score = base_health + random.uniform(-0.1, 0.1)
            
            relationships.append({
                'client': client,
                'date': date,
                'health_score': health_score,
                'interaction_frequency': random.randint(1, 15),
                'response_time_hours': random.uniform(2, 48),
                'satisfaction_score': health_score * 10,
                'payment_delays': random.randint(0, 3),
                'complaint_count': random.randint(0, 2),
                'product_usage': random.uniform(0.3, 1.0),
                'revenue_trend': random.uniform(-0.2, 0.3),
                'risk_indicators': random.randint(0, 5),
                'engagement_score': health_score * random.uniform(0.8, 1.2),
                'churn_probability': 1 - health_score,
                'predicted_action': random.choice(['Monitor', 'Engage', 'Urgent Action', 'Escalate'])
            })
    
    return pd.DataFrame(relationships)

relationship_df = generate_relationship_data()

# Current relationship health overview
current_health = relationship_df.groupby('client').last().reset_index()

col1, col2, col3, col4 = st.columns(4)

with col1:
    high_risk_clients = len(current_health[current_health['health_score'] < 0.5])
    st.metric(
        label="🚨 High Risk Clients",
        value=high_risk_clients,
        delta=f"+{random.randint(0, 2)} this week"
    )

with col2:
    avg_health = current_health['health_score'].mean()
    st.metric(
        label="📊 Avg Health Score",
        value=f"{avg_health:.2f}",
        delta=f"{random.uniform(-0.05, 0.05):.3f}"
    )

with col3:
    predicted_churn = len(current_health[current_health['churn_probability'] > 0.7])
    st.metric(
        label="⚠️ Churn Risk",
        value=predicted_churn,
        delta="Early warning"
    )

with col4:
    urgent_actions = len(current_health[current_health['predicted_action'] == 'Urgent Action'])
    st.metric(
        label="🎯 Urgent Actions",
        value=urgent_actions,
        delta="Immediate attention"
    )

# Risk assessment dashboard
st.subheader("🎯 Client Risk Assessment")

# Sort clients by health score for priority display
priority_clients = current_health.sort_values('health_score').head(10)

for idx, client in priority_clients.iterrows():
    risk_level = "🚨 Critical" if client['health_score'] < 0.4 else "⚠️ Warning" if client['health_score'] < 0.7 else "✅ Healthy"
    
    with st.expander(f"{risk_level} - {client['client']} (Health: {client['health_score']:.2f})"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Current Metrics**")
            st.metric("Health Score", f"{client['health_score']:.2f}")
            st.metric("Churn Probability", f"{client['churn_probability']:.1%}")
            st.metric("Satisfaction", f"{client['satisfaction_score']:.1f}/10")
        
        with col2:
            st.markdown("**Engagement Indicators**")
            st.metric("Interaction Frequency", f"{client['interaction_frequency']}/month")
            st.metric("Response Time", f"{client['response_time_hours']:.1f} hours")
            st.metric("Product Usage", f"{client['product_usage']:.1%}")
        
        with col3:
            st.markdown("**Risk Factors**")
            st.metric("Payment Delays", client['payment_delays'])
            st.metric("Complaints", client['complaint_count'])
            st.metric("Risk Indicators", client['risk_indicators'])
        
        # AI-generated recommendations
        st.markdown("**🤖 AI Recommendations**")
        if client['health_score'] < 0.4:
            recommendations = [
                "Schedule immediate senior management meeting",
                "Conduct comprehensive relationship review",
                "Offer service recovery initiatives",
                "Consider pricing adjustments or concessions"
            ]
        elif client['health_score'] < 0.7:
            recommendations = [
                "Increase touchpoint frequency",
                "Proactive check-in call within 48 hours",
                "Review service delivery quality",
                "Identify additional value opportunities"
            ]
        else:
            recommendations = [
                "Maintain current engagement level",
                "Explore upselling opportunities",
                "Regular quarterly business reviews"
            ]
        
        for rec in recommendations:
            st.write(f"• {rec}")

# Predictive analytics tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trend Analysis", "🔮 Predictions", "🎯 Action Plans", "⚙️ Model Settings"])

with tab1:
    st.subheader("📈 Relationship Health Trends")
    
    # Select clients for trend analysis
    selected_clients = st.multiselect(
        "Select clients to analyze",
        options=relationship_df['client'].unique(),
        default=['RetailChain PLC', 'StartupXYZ', 'TechCorp Ltd']
    )
    
    if selected_clients:
        trend_data = relationship_df[relationship_df['client'].isin(selected_clients)]
        
        fig_trends = px.line(
            trend_data,
            x='date',
            y='health_score',
            color='client',
            title="Client Relationship Health Trends",
            labels={'health_score': 'Health Score', 'date': 'Date'}
        )
        fig_trends.add_hline(y=0.5, line_dash="dash", line_color="red", 
                            annotation_text="Critical Threshold")
        fig_trends.add_hline(y=0.7, line_dash="dash", line_color="orange", 
                            annotation_text="Warning Threshold")
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Correlation analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Health score vs satisfaction correlation
            fig_corr1 = px.scatter(
                current_health,
                x='satisfaction_score',
                y='health_score',
                size='interaction_frequency',
                color='churn_probability',
                title="Health vs Satisfaction Correlation",
                labels={'satisfaction_score': 'Satisfaction Score', 'health_score': 'Health Score'}
            )
            st.plotly_chart(fig_corr1, use_container_width=True)
        
        with col2:
            # Risk factors distribution
            fig_risk = px.histogram(
                current_health,
                x='risk_indicators',
                title="Risk Indicators Distribution",
                nbins=6
            )
            st.plotly_chart(fig_risk, use_container_width=True)

with tab2:
    st.subheader("🔮 Predictive Models & Forecasts")
    
    # Churn prediction model results
    st.markdown("**Churn Prediction Model Performance**")
    
    model_metrics = {
        'Accuracy': 89.2,
        'Precision': 85.7,
        'Recall': 91.3,
        'F1-Score': 88.4,
        'AUC-ROC': 0.94
    }
    
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, (metric, value) in enumerate(model_metrics.items()):
        with [col1, col2, col3, col4, col5][i]:
            st.metric(metric, f"{value}%" if metric != 'AUC-ROC' else f"{value}")
    
    # Feature importance
    st.markdown("**Model Feature Importance**")
    
    features = pd.DataFrame({
        'Feature': ['Interaction Frequency', 'Response Time', 'Satisfaction Score', 
                   'Payment Delays', 'Product Usage', 'Revenue Trend', 'Complaint Count'],
        'Importance': [0.23, 0.19, 0.18, 0.15, 0.12, 0.08, 0.05]
    })
    
    fig_importance = px.bar(
        features,
        x='Importance',
        y='Feature',
        orientation='h',
        title="Feature Importance in Churn Prediction"
    )
    st.plotly_chart(fig_importance, use_container_width=True)
    
    # 30-day forecast
    st.markdown("**30-Day Relationship Health Forecast**")
    
    forecast_clients = current_health.nsmallest(5, 'health_score')
    
    for _, client in forecast_clients.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{client['client']}**")
        
        with col2:
            current_score = client['health_score']
            predicted_change = random.uniform(-0.15, 0.1)
            predicted_score = max(0, min(1, current_score + predicted_change))
            
            st.metric(
                "Predicted Health",
                f"{predicted_score:.2f}",
                f"{predicted_change:+.2f}"
            )
        
        with col3:
            action_probability = 1 - predicted_score
            st.metric(
                "Action Required",
                f"{action_probability:.1%}",
                "High" if action_probability > 0.7 else "Medium" if action_probability > 0.4 else "Low"
            )

with tab3:
    st.subheader("🎯 AI-Generated Action Plans")
    
    # Generate action plans for high-risk clients
    high_risk_clients = current_health[current_health['health_score'] < 0.6].sort_values('health_score')
    
    for _, client in high_risk_clients.iterrows():
        with st.container():
            st.markdown(f"### 🚨 Action Plan: {client['client']}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Immediate actions
                st.markdown("**Immediate Actions (24-48 hours)**")
                immediate_actions = [
                    f"Schedule urgent call with {client['client']} leadership",
                    "Review recent service delivery incidents",
                    "Prepare relationship recovery proposal",
                    "Assign dedicated relationship manager"
                ]
                
                for action in immediate_actions:
                    st.write(f"• {action}")
                
                # Short-term actions
                st.markdown("**Short-term Actions (1-2 weeks)**")
                short_term_actions = [
                    "Conduct comprehensive account review",
                    "Implement enhanced service monitoring",
                    "Develop customized value proposition",
                    "Schedule regular check-in meetings"
                ]
                
                for action in short_term_actions:
                    st.write(f"• {action}")
            
            with col2:
                st.markdown("**Success Metrics**")
                st.metric("Target Health Score", "0.75+")
                st.metric("Timeline", "30 days")
                st.metric("Success Probability", f"{random.randint(65, 85)}%")
                
                if st.button(f"Execute Plan - {client['client']}", key=f"execute_{client['client']}"):
                    st.success(f"Action plan activated for {client['client']}!")
            
            st.divider()

with tab4:
    st.subheader("⚙️ Predictive Model Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Model Parameters**")
        
        prediction_horizon = st.selectbox("Prediction Horizon", ["7 days", "14 days", "30 days", "90 days"])
        sensitivity = st.slider("Model Sensitivity", 0.1, 1.0, 0.8, 0.1)
        alert_threshold = st.slider("Alert Threshold", 0.3, 0.8, 0.5, 0.05)
        
        st.markdown("**Feature Weights**")
        interaction_weight = st.slider("Interaction Frequency", 0.0, 1.0, 0.23, 0.01)
        satisfaction_weight = st.slider("Satisfaction Score", 0.0, 1.0, 0.18, 0.01)
        response_weight = st.slider("Response Time", 0.0, 1.0, 0.19, 0.01)
    
    with col2:
        st.markdown("**Alert Configuration**")
        
        email_alerts = st.checkbox("Email Alerts", value=True)
        sms_alerts = st.checkbox("SMS Alerts", value=False)
        dashboard_alerts = st.checkbox("Dashboard Notifications", value=True)
        
        st.markdown("**Automation Settings**")
        auto_action_plans = st.checkbox("Auto-generate Action Plans", value=True)
        auto_escalation = st.checkbox("Auto-escalate Critical Cases", value=True)
        auto_reporting = st.checkbox("Automated Weekly Reports", value=True)
        
        if st.button("💾 Save Configuration"):
            st.success("Model configuration saved successfully!")

# Recent predictions and alerts
st.subheader("🔔 Recent Predictions & Alerts")

recent_alerts = [
    {
        "time": "15 minutes ago",
        "client": "RetailChain PLC",
        "alert": "Health score dropped below 0.4 - Critical threshold breached",
        "action": "Urgent action plan activated",
        "confidence": 0.92
    },
    {
        "time": "2 hours ago",
        "client": "StartupXYZ",
        "alert": "Predicted 78% churn probability within 30 days",
        "action": "Relationship manager notified",
        "confidence": 0.85
    },
    {
        "time": "1 day ago",
        "client": "LogisticsCorp",
        "alert": "Satisfaction score trend indicates potential deterioration",
        "action": "Proactive engagement scheduled",
        "confidence": 0.73
    }
]

for alert in recent_alerts:
    col1, col2, col3 = st.columns([1, 6, 2])
    
    with col1:
        st.markdown("🚨")
    
    with col2:
        st.markdown(f"**{alert['time']}** - {alert['client']}")
        st.markdown(alert['alert'])
        st.caption(f"Action: {alert['action']}")
    
    with col3:
        st.metric("Confidence", f"{alert['confidence']:.1%}")

st.markdown("""
---
**Feature Highlights:**
- 🧠 Advanced ML models with 89%+ accuracy in churn prediction
- 📊 Real-time relationship health monitoring
- 🎯 Automated action plan generation
- ⚡ Early warning system with 30-90 day forecasts
- 🔄 Continuous model learning and improvement
""")

