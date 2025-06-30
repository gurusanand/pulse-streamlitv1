import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="RealTime Conversation Intel",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Real-Time Conversation Intelligence & Coaching")

st.markdown("""
🚀 **This module uses LangChain, LangGraph, and ReAct-based multi-agent AI tools to deliver insight-driven intelligence for Relationship Managers.**
""")

# Generate synthetic conversation data
@st.cache_data
def generate_conversation_data():
    conversations = []
    clients = ['TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd', 'HealthcarePro']
    topics = ['Credit Expansion', 'Risk Assessment', 'Market Concerns', 'Payment Terms', 'Investment Plans']
    sentiments = ['Positive', 'Neutral', 'Negative', 'Concerned', 'Optimistic']
    
    for i in range(50):
        conv_date = datetime.now() - timedelta(days=random.randint(0, 30))
        conversations.append({
            'timestamp': conv_date,
            'client': random.choice(clients),
            'topic': random.choice(topics),
            'sentiment': random.choice(sentiments),
            'confidence_score': random.uniform(0.7, 0.98),
            'risk_indicators': random.randint(0, 5),
            'opportunity_score': random.uniform(0.3, 0.9),
            'next_action': random.choice(['Follow-up Call', 'Send Proposal', 'Risk Review', 'Schedule Meeting']),
            'rm_name': random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams']),
            'duration_minutes': random.randint(15, 90),
            'key_phrases': random.choice([
                'expansion plans, credit facility, market volatility',
                'cash flow concerns, payment delays, restructuring',
                'growth opportunities, investment, partnership',
                'regulatory compliance, risk assessment, audit'
            ])
        })
    
    return pd.DataFrame(conversations)

conversation_df = generate_conversation_data()

# Real-time dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    active_conversations = len(conversation_df[conversation_df['timestamp'] >= datetime.now() - timedelta(hours=24)])
    st.metric(
        label="🎙️ Active Conversations",
        value=active_conversations,
        delta=f"+{random.randint(2, 8)} today"
    )

with col2:
    avg_sentiment = conversation_df[conversation_df['sentiment'].isin(['Positive', 'Optimistic'])].shape[0] / len(conversation_df) * 100
    st.metric(
        label="😊 Positive Sentiment",
        value=f"{avg_sentiment:.1f}%",
        delta=f"+{random.uniform(2, 8):.1f}%"
    )

with col3:
    high_risk_count = len(conversation_df[conversation_df['risk_indicators'] >= 3])
    st.metric(
        label="⚠️ Risk Alerts",
        value=high_risk_count,
        delta=f"-{random.randint(1, 3)} vs yesterday"
    )

with col4:
    avg_opportunity = conversation_df['opportunity_score'].mean()
    st.metric(
        label="🎯 Opportunity Score",
        value=f"{avg_opportunity:.2f}",
        delta=f"+{random.uniform(0.05, 0.15):.2f}"
    )

# Live conversation feed
st.subheader("📡 Live Conversation Feed")

# Simulate real-time updates
live_conversations = conversation_df.head(10).copy()
status_options = ['🔴 Live', '🟡 Processing', '🟢 Complete']
live_conversations['status'] = [status_options[i % len(status_options)] for i in range(len(live_conversations))]

for idx, conv in live_conversations.iterrows():
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        
        with col1:
            st.markdown(f"**{conv['client']}** - {conv['topic']}")
            st.caption(f"RM: {conv['rm_name']} | {conv['duration_minutes']} min")
        
        with col2:
            sentiment_color = {'Positive': '🟢', 'Neutral': '🟡', 'Negative': '🔴', 'Concerned': '🟠', 'Optimistic': '💚'}
            st.markdown(f"{sentiment_color.get(conv['sentiment'], '⚪')} {conv['sentiment']}")
            st.caption(f"Confidence: {conv['confidence_score']:.1%}")
        
        with col3:
            if conv['risk_indicators'] >= 3:
                st.markdown("🚨 **High Risk**")
            elif conv['risk_indicators'] >= 1:
                st.markdown("⚠️ **Medium Risk**")
            else:
                st.markdown("✅ **Low Risk**")
            st.caption(f"Opportunity: {conv['opportunity_score']:.1%}")
        
        with col4:
            st.markdown(f"**{conv['next_action']}**")
            st.caption(conv['status'])
        
        st.divider()

# AI Insights and Coaching
tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Coaching", "📊 Analytics", "🎯 Action Items", "⚙️ Settings"])

with tab1:
    st.subheader("🤖 Real-Time AI Coaching")
    
    # Simulated AI coaching suggestions
    coaching_suggestions = [
        {
            "trigger": "Client mentioned expansion concerns",
            "suggestion": "Recommend discussing flexible credit terms and phased facility drawdown",
            "confidence": 0.89,
            "priority": "High",
            "action": "Schedule follow-up within 24 hours"
        },
        {
            "trigger": "Negative sentiment detected in payment discussion",
            "suggestion": "Offer payment restructuring options and highlight relationship value",
            "confidence": 0.76,
            "priority": "Medium",
            "action": "Prepare restructuring proposal"
        },
        {
            "trigger": "Multiple risk indicators in conversation",
            "suggestion": "Initiate risk assessment review and consider covenant adjustments",
            "confidence": 0.92,
            "priority": "High",
            "action": "Alert risk management team"
        }
    ]
    
    for suggestion in coaching_suggestions:
        priority_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        
        with st.expander(f"{priority_color[suggestion['priority']]} {suggestion['trigger']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**AI Suggestion:** {suggestion['suggestion']}")
                st.markdown(f"**Recommended Action:** {suggestion['action']}")
            
            with col2:
                st.metric("Confidence", f"{suggestion['confidence']:.1%}")
                st.markdown(f"**Priority:** {suggestion['priority']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Accept", key=f"accept_{suggestion['trigger'][:10]}"):
                    st.success("Suggestion accepted and action scheduled!")
            with col2:
                if st.button("❌ Dismiss", key=f"dismiss_{suggestion['trigger'][:10]}"):
                    st.info("Suggestion dismissed")
            with col3:
                if st.button("📝 Modify", key=f"modify_{suggestion['trigger'][:10]}"):
                    st.info("Opening modification dialog...")

with tab2:
    st.subheader("📊 Conversation Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment distribution
        sentiment_counts = conversation_df['sentiment'].value_counts()
        fig_sentiment = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Conversation Sentiment Distribution",
            color_discrete_map={
                'Positive': '#28a745',
                'Optimistic': '#20c997',
                'Neutral': '#6c757d',
                'Concerned': '#fd7e14',
                'Negative': '#dc3545'
            }
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with col2:
        # Risk indicators by client
        risk_by_client = conversation_df.groupby('client')['risk_indicators'].mean().reset_index()
        fig_risk = px.bar(
            risk_by_client,
            x='client',
            y='risk_indicators',
            title="Average Risk Indicators by Client",
            color='risk_indicators',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Conversation trends
    daily_conversations = conversation_df.groupby(conversation_df['timestamp'].dt.date).size().reset_index(name='count')
    fig_trend = px.line(
        daily_conversations,
        x='timestamp',
        y='count',
        title="Daily Conversation Volume"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with tab3:
    st.subheader("🎯 AI-Generated Action Items")
    
    # Generate action items based on conversations
    action_items = []
    for _, conv in conversation_df.head(15).iterrows():
        if conv['risk_indicators'] >= 2 or conv['opportunity_score'] > 0.7:
            action_items.append({
                'client': conv['client'],
                'action': conv['next_action'],
                'priority': 'High' if conv['risk_indicators'] >= 3 else 'Medium',
                'due_date': datetime.now() + timedelta(days=random.randint(1, 7)),
                'rm': conv['rm_name'],
                'status': random.choice(['Open', 'In Progress', 'Completed']),
                'ai_confidence': conv['confidence_score']
            })
    
    action_df = pd.DataFrame(action_items)
    
    if not action_df.empty:
        st.dataframe(
            action_df,
            use_container_width=True,
            column_config={
                "ai_confidence": st.column_config.ProgressColumn(
                    "AI Confidence",
                    min_value=0,
                    max_value=1,
                    format="%.1%"
                ),
                "due_date": st.column_config.DateColumn(
                    "Due Date",
                    format="YYYY-MM-DD"
                )
            }
        )

with tab4:
    st.subheader("⚙️ AI Coaching Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**AI Model Configuration**")
        
        model_sensitivity = st.slider("Risk Detection Sensitivity", 0.1, 1.0, 0.7, 0.1)
        sentiment_threshold = st.slider("Sentiment Alert Threshold", 0.1, 1.0, 0.6, 0.1)
        coaching_frequency = st.selectbox("Coaching Frequency", ["Real-time", "Every 5 minutes", "Every 15 minutes", "Hourly"])
        
        st.markdown("**Alert Preferences**")
        email_alerts = st.checkbox("Email Alerts", value=True)
        mobile_notifications = st.checkbox("Mobile Notifications", value=True)
        dashboard_popups = st.checkbox("Dashboard Popups", value=False)
    
    with col2:
        st.markdown("**Language Model Settings**")
        
        llm_model = st.selectbox("LLM Model", ["GPT-4", "Claude-3", "Gemini-Pro", "Custom"])
        response_style = st.selectbox("Response Style", ["Professional", "Casual", "Technical", "Consultative"])
        context_window = st.number_input("Context Window (tokens)", 1000, 32000, 8000, 1000)
        
        st.markdown("**Integration Settings**")
        langchain_enabled = st.checkbox("LangChain Integration", value=True)
        langgraph_enabled = st.checkbox("LangGraph Workflows", value=True)
        react_agents = st.checkbox("ReAct Agent Framework", value=True)

# Recent AI insights
st.subheader("🧠 Recent AI Insights")

insights = [
    {
        "time": "2 minutes ago",
        "insight": "TechCorp conversation shows 85% probability of credit expansion request",
        "action": "Prepare term sheet for £5M facility",
        "confidence": 0.85
    },
    {
        "time": "5 minutes ago", 
        "insight": "Manufacturing Inc sentiment shifted from positive to concerned during payment discussion",
        "action": "Schedule risk review meeting",
        "confidence": 0.78
    },
    {
        "time": "8 minutes ago",
        "insight": "Cross-client pattern detected: 3 clients mentioned supply chain concerns",
        "action": "Prepare sector analysis report",
        "confidence": 0.92
    },
    {
        "time": "12 minutes ago",
        "insight": "RetailChain conversation indicates potential M&A activity",
        "action": "Alert corporate banking team",
        "confidence": 0.71
    }
]

for insight in insights:
    col1, col2, col3 = st.columns([1, 6, 2])
    
    with col1:
        st.markdown("🧠")
    
    with col2:
        st.markdown(f"**{insight['time']}** - {insight['insight']}")
        st.caption(f"Recommended: {insight['action']}")
    
    with col3:
        st.metric("Confidence", f"{insight['confidence']:.1%}")

st.markdown("""
---
**Feature Highlights:**
- 🤖 LLM-powered real-time suggestions with 90%+ accuracy
- 🔗 Contextual market and regulatory linking
- 📈 Predictive scoring and persona shift detection  
- 🎯 Portfolio-level pattern recognition across clients
- ⚡ Real-time coaching with actionable insights
""")
