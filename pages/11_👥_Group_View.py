import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Group View", page_icon="👥", layout="wide")

st.title("👥 Group View - Customer Portfolio Management")

# Generate comprehensive customer data
@st.cache_data
def generate_customer_data():
    customers = []
    company_names = [
        'TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd', 'HealthcarePro',
        'StartupXYZ', 'LogisticsCorp', 'FinanceGroup', 'PropertyDev', 'MediaHouse',
        'AutoMotors Ltd', 'FoodChain Co', 'PharmaCorp', 'TelecomGiant', 'ConstructionPro',
        'AeroSpace Inc', 'MarineServices', 'AgriTech Ltd', 'CleanEnergy Co', 'DataSystems'
    ]
    
    sectors = ['Technology', 'Manufacturing', 'Retail', 'Energy', 'Healthcare', 
               'Logistics', 'Finance', 'Real Estate', 'Media', 'Automotive']
    
    for i, company in enumerate(company_names):
        customers.append({
            'customer_id': f"CUST-{1000+i}",
            'company_name': company,
            'sector': random.choice(sectors),
            'relationship_manager': random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams', 'David Brown']),
            'total_exposure': random.randint(1000000, 100000000),
            'credit_rating': random.choice(['AAA', 'AA+', 'AA', 'A+', 'A', 'BBB+', 'BBB']),
            'relationship_length': random.randint(1, 15),
            'annual_revenue': random.randint(5000000, 500000000),
            'employee_count': random.randint(50, 10000),
            'country': random.choice(['UK', 'Germany', 'France', 'Netherlands', 'Switzerland']),
            'risk_score': random.uniform(0.1, 0.8),
            'profitability_score': random.uniform(0.3, 0.95),
            'growth_potential': random.uniform(0.2, 0.9),
            'last_interaction': datetime.now() - timedelta(days=random.randint(1, 30)),
            'products_used': random.randint(2, 8),
            'satisfaction_score': random.uniform(7.0, 9.8)
        })
    
    return pd.DataFrame(customers)

customer_df = generate_customer_data()

# Search and filter section
st.subheader("🔍 Customer Search & Filter")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Searchable dropdown for customers
    search_term = st.text_input("🔍 Search Customers", placeholder="Type customer name...")
    
    if search_term:
        filtered_customers = customer_df[
            customer_df['company_name'].str.contains(search_term, case=False, na=False)
        ]['company_name'].tolist()
    else:
        filtered_customers = customer_df['company_name'].tolist()
    
    selected_customer = st.selectbox(
        "Select Customer",
        options=['All Customers'] + filtered_customers,
        index=0
    )

with col2:
    sector_filter = st.selectbox(
        "Filter by Sector",
        options=['All Sectors'] + list(customer_df['sector'].unique())
    )

with col3:
    rm_filter = st.selectbox(
        "Filter by RM",
        options=['All RMs'] + list(customer_df['relationship_manager'].unique())
    )

# Apply filters
filtered_df = customer_df.copy()

if selected_customer != 'All Customers':
    filtered_df = filtered_df[filtered_df['company_name'] == selected_customer]

if sector_filter != 'All Sectors':
    filtered_df = filtered_df[filtered_df['sector'] == sector_filter]

if rm_filter != 'All RMs':
    filtered_df = filtered_df[filtered_df['relationship_manager'] == rm_filter]

# Portfolio overview metrics
st.subheader("📊 Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_customers = len(filtered_df)
    st.metric("👥 Total Customers", total_customers)

with col2:
    total_exposure = filtered_df['total_exposure'].sum()
    st.metric("💰 Total Exposure", f"£{total_exposure/1000000:.1f}M")

with col3:
    avg_satisfaction = filtered_df['satisfaction_score'].mean()
    st.metric("😊 Avg Satisfaction", f"{avg_satisfaction:.1f}/10")

with col4:
    high_risk_count = len(filtered_df[filtered_df['risk_score'] > 0.6])
    st.metric("⚠️ High Risk", high_risk_count)

# Customer portfolio visualization
tab1, tab2, tab3, tab4 = st.tabs(["📈 Portfolio Analysis", "👥 Customer Details", "🎯 Risk Matrix", "📊 Performance"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Exposure by sector
        sector_exposure = filtered_df.groupby('sector')['total_exposure'].sum().reset_index()
        fig_sector = px.pie(
            sector_exposure, 
            values='total_exposure', 
            names='sector',
            title="Exposure Distribution by Sector"
        )
        st.plotly_chart(fig_sector, use_container_width=True)
    
    with col2:
        # Risk vs Profitability scatter
        fig_risk = px.scatter(
            filtered_df,
            x='risk_score',
            y='profitability_score',
            size='total_exposure',
            color='sector',
            hover_data=['company_name'],
            title="Risk vs Profitability Matrix"
        )
        st.plotly_chart(fig_risk, use_container_width=True)

with tab2:
    st.subheader("👥 Customer Details")
    
    # Display customer data with enhanced formatting
    display_df = filtered_df[[
        'company_name', 'sector', 'relationship_manager', 'total_exposure',
        'credit_rating', 'risk_score', 'satisfaction_score', 'last_interaction'
    ]].copy()
    
    display_df['total_exposure'] = display_df['total_exposure'].apply(lambda x: f"£{x/1000000:.1f}M")
    display_df['risk_score'] = display_df['risk_score'].apply(lambda x: f"{x:.1%}")
    display_df['satisfaction_score'] = display_df['satisfaction_score'].apply(lambda x: f"{x:.1f}/10")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "company_name": "Company Name",
            "sector": "Sector",
            "relationship_manager": "RM",
            "total_exposure": "Exposure",
            "credit_rating": "Rating",
            "risk_score": "Risk Score",
            "satisfaction_score": "Satisfaction",
            "last_interaction": st.column_config.DateColumn("Last Contact")
        }
    )

with tab3:
    st.subheader("🎯 Risk Assessment Matrix")
    
    # Risk categorization
    filtered_df['risk_category'] = pd.cut(
        filtered_df['risk_score'], 
        bins=[0, 0.3, 0.6, 1.0], 
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )
    
    risk_summary = filtered_df.groupby('risk_category').agg({
        'company_name': 'count',
        'total_exposure': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_risk_count = px.bar(
            risk_summary,
            x='risk_category',
            y='company_name',
            title="Customer Count by Risk Category",
            color='risk_category',
            color_discrete_map={
                'Low Risk': '#28a745',
                'Medium Risk': '#ffc107', 
                'High Risk': '#dc3545'
            }
        )
        st.plotly_chart(fig_risk_count, use_container_width=True)
    
    with col2:
        fig_risk_exposure = px.bar(
            risk_summary,
            x='risk_category',
            y='total_exposure',
            title="Exposure by Risk Category",
            color='risk_category',
            color_discrete_map={
                'Low Risk': '#28a745',
                'Medium Risk': '#ffc107',
                'High Risk': '#dc3545'
            }
        )
        st.plotly_chart(fig_risk_exposure, use_container_width=True)

with tab4:
    st.subheader("📊 RM Performance Dashboard")
    
    rm_performance = filtered_df.groupby('relationship_manager').agg({
        'company_name': 'count',
        'total_exposure': 'sum',
        'satisfaction_score': 'mean',
        'profitability_score': 'mean'
    }).reset_index()
    
    rm_performance.columns = ['RM', 'Customers', 'Total_Exposure', 'Avg_Satisfaction', 'Avg_Profitability']
    
    for _, rm in rm_performance.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(f"👤 {rm['RM']}", "")
            
            with col2:
                st.metric("Customers", rm['Customers'])
            
            with col3:
                st.metric("Exposure", f"£{rm['Total_Exposure']/1000000:.1f}M")
            
            with col4:
                st.metric("Satisfaction", f"{rm['Avg_Satisfaction']:.1f}/10")
            
            st.divider()

# Quick actions section
if selected_customer != 'All Customers':
    st.subheader(f"🎯 Quick Actions for {selected_customer}")
    
    customer_data = filtered_df[filtered_df['company_name'] == selected_customer].iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📞 Schedule Call"):
            st.success("Call scheduled!")
    
    with col2:
        if st.button("📧 Send Email"):
            st.success("Email sent!")
    
    with col3:
        if st.button("📊 Generate Report"):
            st.success("Report generated!")
    
    with col4:
        if st.button("⚠️ Risk Review"):
            st.success("Risk review initiated!")

st.markdown("""
---
**Group View Features:**
- 🔍 Advanced customer search and filtering
- 📊 Real-time portfolio analytics
- 🎯 Risk assessment and monitoring
- 👥 RM performance tracking
- ⚡ Quick action capabilities
""")

