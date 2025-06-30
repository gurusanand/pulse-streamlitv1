import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Banking Assistant")

st.markdown("""
🚀 **Your intelligent banking companion powered by advanced AI models and real-time data integration.**
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI Banking Assistant. I can help you with client insights, deal analysis, risk assessment, and much more. How can I assist you today?"}
    ]

# Sample banking responses for simulation
banking_responses = {
    "client": [
        "Based on the latest data, TechCorp Ltd shows strong financial performance with a 15% revenue growth this quarter. Their credit utilization is at 65% with excellent payment history.",
        "Manufacturing Inc has been flagged for potential risk due to delayed payments in the last 30 days. I recommend scheduling a relationship review meeting.",
        "RetailChain PLC presents a great cross-selling opportunity. They've expressed interest in trade finance solutions during recent conversations."
    ],
    "risk": [
        "Current portfolio risk assessment shows 85% of clients in low-risk category. However, 3 clients require immediate attention due to covenant breaches.",
        "Market volatility in the energy sector may impact EnergyPlus Ltd. I suggest reviewing their exposure limits and stress testing scenarios.",
        "Regulatory changes in Basel III requirements will affect 12 clients in our portfolio. Compliance review recommended within 30 days."
    ],
    "deal": [
        "The £5M credit facility for TechCorp shows 89% probability of success based on historical patterns and current market conditions.",
        "I've identified 3 potential deals worth £15M total based on client conversation analysis and growth patterns.",
        "Deal pipeline analysis suggests focusing on healthcare sector opportunities - 67% higher success rate than average."
    ],
    "market": [
        "Current market sentiment analysis indicates positive outlook for technology sector with 78% confidence score.",
        "Interest rate trends suggest optimal timing for long-term facility discussions with growth-oriented clients.",
        "Sector analysis shows manufacturing clients are seeking working capital solutions due to supply chain pressures."
    ],
    "general": [
        "I can help you with client analysis, deal insights, risk assessment, market intelligence, and much more. What specific area would you like to explore?",
        "Based on your recent activities, I notice increased focus on technology sector clients. Would you like me to provide sector-specific insights?",
        "I've analyzed your portfolio and identified 5 key opportunities for this week. Would you like me to prioritize them for you?"
    ]
}

def get_ai_response(user_input):
    """Simulate AI response based on user input keywords"""
    user_input_lower = user_input.lower()
    
    # Simulate thinking time
    time.sleep(1)
    
    if any(word in user_input_lower for word in ['client', 'customer', 'company']):
        return random.choice(banking_responses["client"])
    elif any(word in user_input_lower for word in ['risk', 'danger', 'threat', 'exposure']):
        return random.choice(banking_responses["risk"])
    elif any(word in user_input_lower for word in ['deal', 'opportunity', 'sale', 'pipeline']):
        return random.choice(banking_responses["deal"])
    elif any(word in user_input_lower for word in ['market', 'sector', 'industry', 'trend']):
        return random.choice(banking_responses["market"])
    else:
        return random.choice(banking_responses["general"])

# Chat interface
st.subheader("💬 Chat with AI Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your banking portfolio..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your request..."):
            response = get_ai_response(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Quick action buttons
st.subheader("🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Portfolio Analysis"):
        response = "Your portfolio shows strong performance with £125M total exposure across 45 clients. Risk distribution: 78% low risk, 18% medium risk, 4% high risk. Top performing sector: Technology (32% of portfolio)."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col2:
    if st.button("🎯 Deal Opportunities"):
        response = "I've identified 7 high-probability opportunities worth £23M: 3 in technology sector, 2 in healthcare, 2 in manufacturing. TechCorp Ltd shows highest conversion probability at 91%."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col3:
    if st.button("⚠️ Risk Alerts"):
        response = "Current risk alerts: 2 clients with payment delays (Manufacturing Inc, RetailChain PLC), 1 covenant breach (StartupXYZ), 3 clients approaching credit limits. Immediate action recommended for Manufacturing Inc."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col4:
    if st.button("📈 Market Insights"):
        response = "Market analysis: Technology sector showing 15% growth, Manufacturing facing headwinds (-3%), Healthcare stable (+2%). Interest rates expected to remain stable. Recommend focusing on tech and healthcare opportunities."
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# AI Capabilities showcase
tab1, tab2, tab3, tab4 = st.tabs(["🧠 AI Capabilities", "📊 Analytics", "🔧 Tools", "⚙️ Settings"])

with tab1:
    st.subheader("🧠 AI Assistant Capabilities")
    
    capabilities = [
        {
            "category": "Client Intelligence",
            "features": [
                "Real-time client health scoring",
                "Relationship deterioration prediction",
                "Cross-selling opportunity identification",
                "Behavioral pattern analysis"
            ]
        },
        {
            "category": "Deal Management", 
            "features": [
                "Deal probability scoring",
                "Competitive intelligence analysis",
                "Optimal pricing recommendations",
                "Timeline prediction"
            ]
        },
        {
            "category": "Risk Assessment",
            "features": [
                "Portfolio risk analysis",
                "Early warning systems",
                "Stress testing scenarios",
                "Regulatory compliance monitoring"
            ]
        },
        {
            "category": "Market Intelligence",
            "features": [
                "Sector trend analysis",
                "Economic indicator tracking",
                "News sentiment analysis",
                "Competitive landscape monitoring"
            ]
        }
    ]
    
    for capability in capabilities:
        with st.expander(f"🎯 {capability['category']}"):
            for feature in capability['features']:
                st.write(f"• {feature}")

with tab2:
    st.subheader("📊 AI Performance Analytics")
    
    # Generate sample AI performance data
    performance_data = {
        'Metric': ['Accuracy', 'Response Time', 'User Satisfaction', 'Query Resolution'],
        'Score': [94.2, 1.8, 4.7, 89.5],
        'Target': [90.0, 2.0, 4.5, 85.0],
        'Unit': ['%', 'seconds', '/5', '%']
    }
    
    perf_df = pd.DataFrame(performance_data)
    
    for _, metric in perf_df.iterrows():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{metric['Metric']}**")
        
        with col2:
            delta = metric['Score'] - metric['Target']
            st.metric(
                label="Current",
                value=f"{metric['Score']}{metric['Unit']}",
                delta=f"{delta:+.1f}{metric['Unit']}"
            )
        
        with col3:
            st.metric(
                label="Target", 
                value=f"{metric['Target']}{metric['Unit']}"
            )

with tab3:
    st.subheader("🔧 AI Tools & Integrations")
    
    tools = [
        {"name": "Document Analysis", "status": "Active", "description": "Extract insights from contracts and reports"},
        {"name": "Voice Recognition", "status": "Active", "description": "Process meeting recordings and calls"},
        {"name": "Predictive Modeling", "status": "Active", "description": "Forecast client behavior and market trends"},
        {"name": "Natural Language Processing", "status": "Active", "description": "Understand and respond to complex queries"},
        {"name": "Data Visualization", "status": "Active", "description": "Generate charts and insights automatically"},
        {"name": "API Integrations", "status": "Active", "description": "Connect with external data sources"}
    ]
    
    for tool in tools:
        col1, col2, col3 = st.columns([3, 1, 2])
        
        with col1:
            st.markdown(f"**{tool['name']}**")
        
        with col2:
            status_color = "🟢" if tool['status'] == "Active" else "🔴"
            st.markdown(f"{status_color} {tool['status']}")
        
        with col3:
            st.caption(tool['description'])

with tab4:
    st.subheader("⚙️ AI Assistant Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Response Preferences**")
        
        response_style = st.selectbox("Response Style", ["Professional", "Casual", "Technical", "Concise"])
        detail_level = st.selectbox("Detail Level", ["High", "Medium", "Low"])
        language = st.selectbox("Language", ["English", "French", "German", "Spanish"])
        
        st.markdown("**Notification Settings**")
        proactive_alerts = st.checkbox("Proactive Insights", value=True)
        daily_summary = st.checkbox("Daily Summary", value=True)
        urgent_alerts = st.checkbox("Urgent Alerts", value=True)
    
    with col2:
        st.markdown("**AI Model Configuration**")
        
        model_version = st.selectbox("AI Model", ["GPT-4 Turbo", "Claude-3", "Gemini Pro"])
        confidence_threshold = st.slider("Confidence Threshold", 0.5, 1.0, 0.8)
        context_memory = st.slider("Context Memory (messages)", 10, 100, 50)
        
        st.markdown("**Data Sources**")
        crm_integration = st.checkbox("CRM Data", value=True)
        market_data = st.checkbox("Market Data", value=True)
        news_feeds = st.checkbox("News Feeds", value=True)
        
        if st.button("💾 Save Settings"):
            st.success("AI Assistant settings saved!")

# Clear chat button
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI Banking Assistant. I can help you with client insights, deal analysis, risk assessment, and much more. How can I assist you today?"}
    ]
    st.rerun()

st.markdown("""
---
**AI Assistant Features:**
- 🤖 Advanced natural language processing with banking domain expertise
- 📊 Real-time data analysis and insights generation
- 🎯 Personalized recommendations based on your portfolio
- ⚡ Instant responses to complex banking queries
- 🔄 Continuous learning from interactions and feedback
- 🛡️ Secure and compliant AI processing
""")

