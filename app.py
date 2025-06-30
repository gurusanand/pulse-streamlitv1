import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
import json
import os

# Configure page
st.set_page_config(
    page_title="PULSE - AI-Powered Banking Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for banking theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
    }
    
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .feature-card {
        background: #696969;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
    }
    
    .admin-panel {
        background: #fef7ff;
        border: 2px solid #a855f7;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .ui-builder {
        background: #f0fdf4;
        border: 2px solid #22c55e;
        border-radius: 10px;
        padding: 1rem;
    }
    
    .tech-demo {
        background: #fefce8;
        border: 2px solid #eab308;
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'Senior Relationship Manager'
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = 'Corporate Blue'
if 'custom_layouts' not in st.session_state:
    st.session_state.custom_layouts = {}
if 'user_permissions' not in st.session_state:
    st.session_state.user_permissions = {
        'admin': True,
        'ui_builder': True,
        'analytics': True,
        'client_management': True
    }

# Load mock data
@st.cache_data
def load_mock_data():
    """Load mock banking data for demonstration"""
    
    # Client data
    clients = pd.DataFrame({
        'client_id': range(1, 51),
        'name': [f'Client {i}' for i in range(1, 51)],
        'industry': np.random.choice(['Manufacturing', 'Technology', 'Healthcare', 'Finance', 'Retail'], 50),
        'revenue': np.random.uniform(1000000, 100000000, 50),
        'risk_score': np.random.uniform(1, 10, 50),
        'relationship_manager': np.random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams', 'David Brown'], 50),
        'last_contact': pd.date_range(start='2024-01-01', periods=50, freq='D')
    })
    
    # Deal pipeline data
    deals = pd.DataFrame({
        'deal_id': range(1, 101),
        'client_id': np.random.choice(range(1, 51), 100),
        'deal_name': [f'Deal {i}' for i in range(1, 101)],
        'value': np.random.uniform(100000, 10000000, 100),
        'stage': np.random.choice(['Prospect', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost'], 100),
        'probability': np.random.uniform(0.1, 0.9, 100),
        'close_date': pd.date_range(start='2024-01-01', periods=100, freq='W'),
        'product': np.random.choice(['Term Loan', 'Trade Finance', 'Treasury Services', 'FX Services'], 100)
    })
    
    # Performance data
    performance = pd.DataFrame({
        'month': pd.date_range(start='2024-01-01', periods=12, freq='M'),
        'revenue': np.random.uniform(10000000, 20000000, 12),
        'deals_closed': np.random.randint(20, 60, 12),
        'new_clients': np.random.randint(5, 15, 12),
        'client_satisfaction': np.random.uniform(8.0, 9.5, 12)
    })
    
    return clients, deals, performance

# Sidebar navigation
def render_sidebar():
    """Render the main navigation sidebar"""
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>🏦 PULSE</h2>
            <p>AI-Powered Banking Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User info
        st.markdown(f"**Welcome, John Smith**")
        st.markdown(f"*{st.session_state.user_role}*")
        st.markdown("---")
        
        # Main navigation
        selected = option_menu(
            menu_title="Navigation",
            options=[
                "Dashboard", "Client 360",  "Technical Architecture"
            ],
            icons=[
                "speedometer2", "people",  "cpu"
            ],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#f505c1bafafa"},
                "icon": {"color": "#3b82f6", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#505c1b"},
            }
        )
        
        return selected

# Dashboard page
def render_dashboard():
    """Render the main dashboard"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🏦 Executive Dashboard</h1>
        <p>Real-time insights and key performance indicators</p>
    </div>
    """, unsafe_allow_html=True)
    
    clients, deals, performance = load_mock_data()
    
    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = performance['revenue'].sum()
        st.metric(
            label="Total Revenue",
            value=f"£{total_revenue/1000000:.1f}M",
            delta="12.5%"
        )
    
    with col2:
        total_deals = len(deals[deals['stage'] == 'Closed Won'])
        st.metric(
            label="Deals Closed",
            value=total_deals,
            delta="8.3%"
        )
    
    with col3:
        active_clients = len(clients)
        st.metric(
            label="Active Clients",
            value=active_clients,
            delta="5.2%"
        )
    
    with col4:
        pipeline_value = deals[deals['stage'].isin(['Prospect', 'Qualified', 'Proposal', 'Negotiation'])]['value'].sum()
        st.metric(
            label="Pipeline Value",
            value=f"£{pipeline_value/1000000:.1f}M",
            delta="15.7%"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Revenue Trend")
        fig = px.line(
            performance, 
            x='month', 
            y='revenue',
            title="Monthly Revenue Performance"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Deal Pipeline by Stage")
        pipeline_summary = deals.groupby('stage')['value'].sum().reset_index()
        fig = px.pie(
            pipeline_summary,
            values='value',
            names='stage',
            title="Pipeline Distribution"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activities
    st.subheader("📋 Recent Activities")
    
    activities = [
        {"time": "5 min ago", "type": "alert", "message": "High-value opportunity requires attention - ABC Corp £5.2M deal"},
        {"time": "15 min ago", "type": "info", "message": "AI analysis completed for XYZ Manufacturing - Risk score updated"},
        {"time": "1 hour ago", "type": "warning", "message": "Credit limit approaching for DEF Industries - Review required"},
        {"time": "2 hours ago", "type": "success", "message": "Deal closed: GHI Services £2.1M term loan approved"}
    ]
    
    for activity in activities:
        icon = {"alert": "🚨", "info": "ℹ️", "warning": "⚠️", "success": "✅"}[activity["type"]]
        st.markdown(f"{icon} **{activity['time']}** - {activity['message']}")

# Client 360 page
def render_client360():
    """Render the Client 360 view"""
    
    st.markdown("""
    <div class="main-header">
        <h1>👥 Client 360</h1>
        <p>Complete client relationship management and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    clients, deals, performance = load_mock_data()
    
    # Client selection
    selected_client = st.selectbox(
        "Select Client",
        options=clients['name'].tolist(),
        index=0
    )
    
    client_data = clients[clients['name'] == selected_client].iloc[0]
    client_deals = deals[deals['client_id'] == client_data['client_id']]
    
    # Client overview
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader(f"🏢 {client_data['name']}")
        st.write(f"**Industry:** {client_data['industry']}")
        st.write(f"**Annual Revenue:** £{client_data['revenue']/1000000:.1f}M")
        st.write(f"**Relationship Manager:** {client_data['relationship_manager']}")
        st.write(f"**Last Contact:** {client_data['last_contact'].strftime('%Y-%m-%d')}")
    
    with col2:
        st.metric(
            label="Risk Score",
            value=f"{client_data['risk_score']:.1f}/10",
            delta="-0.5" if client_data['risk_score'] < 5 else "+0.3"
        )
    
    with col3:
        total_deal_value = client_deals['value'].sum()
        st.metric(
            label="Total Deal Value",
            value=f"£{total_deal_value/1000000:.1f}M",
            delta="22.1%"
        )
    
    # Client deals
    st.subheader("💼 Active Deals")
    
    if not client_deals.empty:
        st.dataframe(
            client_deals[['deal_name', 'value', 'stage', 'probability', 'product']],
            use_container_width=True
        )
    else:
        st.info("No active deals for this client")
    
    # AI Insights
    st.subheader("🤖 AI-Powered Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Relationship Health</h4>
            <p><strong>Score:</strong> 8.5/10 (Excellent)</p>
            <p><strong>Trend:</strong> Improving (+0.7 this quarter)</p>
            <p><strong>Key Factors:</strong> Regular engagement, growing deal pipeline, positive payment history</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Recommendations</h4>
            <ul>
                <li>Schedule quarterly business review</li>
                <li>Introduce treasury services for cash management</li>
                <li>Consider trade finance for international expansion</li>
                <li>Monitor credit utilization trends</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Admin Configuration page
def render_admin_config():
    """Render the admin configuration panel"""
    
    if not st.session_state.user_permissions.get('admin', False):
        st.error("🚫 Access Denied: Admin privileges required")
        return
    
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Admin Configuration</h1>
        <p>System administration and configuration management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Roles & Permissions", "🎨 UI Configuration", "🌐 Localization", "🔧 System Settings"])
    
    with tab1:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        
        st.subheader("Role Management")
        
        # Role selection
        roles = [
            "Super Administrator",
            "Relationship Manager", 
            "Credit Analyst",
            "Read-Only Viewer"
        ]
        
        selected_role = st.selectbox("Select Role", roles)
        
        # Permission matrix
        st.subheader("Permissions Matrix")
        
        permissions = {
            "System Administration": ["Read", "Write", "Delete", "Configure"],
            "User Management": ["Read", "Write", "Delete", "Manage"],
            "Client Management": ["Read", "Write", "Delete", "Export"],
            "Deal Management": ["Read", "Write", "Delete", "Approve"],
            "Reports & Analytics": ["Read", "Write", "Delete", "Export"],
            "Configuration": ["Read", "Write", "Delete", "Deploy"]
        }
        
        for category, perms in permissions.items():
            st.write(f"**{category}**")
            cols = st.columns(len(perms))
            for i, perm in enumerate(perms):
                with cols[i]:
                    st.checkbox(perm, key=f"{category}_{perm}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        
        st.subheader("Theme Configuration")
        
        # Theme selection
        themes = {
            "Corporate Blue": {"primary": "#3B82F6", "secondary": "#1E40AF"},
            "Banking Green": {"primary": "#10B981", "secondary": "#047857"},
            "Professional Gray": {"primary": "#6B7280", "secondary": "#374151"},
            "Premium Purple": {"primary": "#8B5CF6", "secondary": "#7C3AED"}
        }
        
        selected_theme = st.selectbox("Select Theme", list(themes.keys()))
        st.session_state.current_theme = selected_theme
        
        # Layout configuration
        st.subheader("Layout Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            sidebar_position = st.selectbox("Sidebar Position", ["Left", "Right", "Collapsible"])
            header_style = st.selectbox("Header Style", ["Fixed", "Sticky", "Static"])
        
        with col2:
            content_width = st.selectbox("Content Width", ["Full Width", "Boxed", "Fluid"])
            card_style = st.selectbox("Card Style", ["Shadow", "Border", "Flat"])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        
        st.subheader("Language Management")
        
        # Language settings
        languages = {
            "🇬🇧 English": "en",
            "🇫🇷 French": "fr", 
            "🇩🇪 German": "de",
            "🇪🇸 Spanish": "es",
            "🇮🇹 Italian": "it"
        }
        
        for lang, code in languages.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(lang)
            with col2:
                st.checkbox("Active", key=f"lang_{code}")
            with col3:
                if st.button("Edit", key=f"edit_{code}"):
                    st.info(f"Editing {lang} labels...")
        
        # Label configuration
        st.subheader("Quick Label Editor")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            label_key = st.text_input("Label Key", placeholder="dashboard.title")
        with col2:
            english_text = st.text_input("English", placeholder="Dashboard")
        with col3:
            french_text = st.text_input("French", placeholder="Tableau de bord")
        
        if st.button("Add Label"):
            st.success("Label added successfully!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        
        st.subheader("Security Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            session_timeout = st.number_input("Session Timeout (minutes)", value=30, min_value=5, max_value=480)
            password_expiry = st.number_input("Password Expiry (days)", value=90, min_value=30, max_value=365)
        
        with col2:
            st.checkbox("Require uppercase letters", value=True)
            st.checkbox("Require numbers", value=True)
            st.checkbox("Enable audit logging", value=True)
        
        st.subheader("Data Management")
        
        col1, col2 = st.columns(2)
        with col1:
            data_retention = st.number_input("Data Retention (years)", value=7, min_value=1, max_value=20)
        with col2:
            backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
        
        st.markdown('</div>', unsafe_allow_html=True)

# UI Builder page
def render_ui_builder():
    """Render the drag-and-drop UI builder"""
    
    if not st.session_state.user_permissions.get('ui_builder', False):
        st.error("🚫 Access Denied: UI Builder privileges required")
        return
    
    st.markdown("""
    <div class="main-header">
        <h1>🎨 UI Builder</h1>
        <p>Drag-and-drop page builder for custom layouts</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="ui-builder">', unsafe_allow_html=True)
    
    # UI Builder tabs
    tab1, tab2, tab3 = st.tabs(["🧩 Widget Library", "📐 Layout Templates", "⚙️ Page Settings"])
    
    with tab1:
        st.subheader("Available Widgets")
        
        widget_categories = {
            "📊 Analytics": [
                {"name": "KPI Card", "description": "Display key performance indicators"},
                {"name": "Line Chart", "description": "Time series data visualization"},
                {"name": "Bar Chart", "description": "Categorical data comparison"},
                {"name": "Pie Chart", "description": "Proportional data display"}
            ],
            "💼 Business": [
                {"name": "Client Card", "description": "Client information display"},
                {"name": "Deal Card", "description": "Deal summary and status"},
                {"name": "News Feed", "description": "Latest news and updates"},
                {"name": "Risk Gauge", "description": "Risk level indicator"}
            ],
            "📋 Data": [
                {"name": "Data Table", "description": "Tabular data display"},
                {"name": "Search Box", "description": "Data search and filtering"},
                {"name": "Export Button", "description": "Data export functionality"},
                {"name": "Pagination", "description": "Data navigation controls"}
            ],
            "🎛️ Controls": [
                {"name": "Action Button", "description": "Interactive button"},
                {"name": "Form Input", "description": "Data input field"},
                {"name": "Dropdown", "description": "Selection dropdown"},
                {"name": "Toggle Switch", "description": "Boolean control"}
            ]
        }
        
        for category, widgets in widget_categories.items():
            with st.expander(category):
                for widget in widgets:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{widget['name']}**")
                        st.write(widget['description'])
                    with col2:
                        if st.button("Add", key=f"add_{widget['name']}"):
                            st.success(f"Added {widget['name']} to canvas")
    
    with tab2:
        st.subheader("Layout Templates")
        
        templates = [
            {
                "name": "Executive Dashboard",
                "description": "KPIs, charts, and key metrics",
                "preview": "📊📈📋"
            },
            {
                "name": "Client Overview", 
                "description": "Client-focused layout",
                "preview": "👤📊📋"
            },
            {
                "name": "Analytics Hub",
                "description": "Data-heavy analytical view", 
                "preview": "📈📊📉"
            },
            {
                "name": "Risk Dashboard",
                "description": "Risk monitoring and alerts",
                "preview": "⚠️📊🛡️"
            }
        ]
        
        for template in templates:
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.markdown(f"<div style='font-size: 2em; text-align: center;'>{template['preview']}</div>", unsafe_allow_html=True)
                with col2:
                    st.write(f"**{template['name']}**")
                    st.write(template['description'])
                with col3:
                    if st.button("Use Template", key=f"template_{template['name']}"):
                        st.success(f"Applied {template['name']} template")
    
    with tab3:
        st.subheader("Page Configuration")
        
        # Page settings
        page_name = st.text_input("Page Name", value="Custom Dashboard")
        page_description = st.text_area("Page Description", value="Custom dashboard created with UI Builder")
        
        col1, col2 = st.columns(2)
        with col1:
            page_width = st.selectbox("Page Width", ["Full Width", "Boxed", "Fluid"])
            grid_size = st.selectbox("Grid Size", ["12 Columns", "16 Columns", "24 Columns"])
        
        with col2:
            responsive_mode = st.checkbox("Responsive Design", value=True)
            auto_save = st.checkbox("Auto Save", value=True)
        
        # Save/Load layouts
        st.subheader("Layout Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Layout"):
                layout_name = st.text_input("Layout Name", value="My Custom Layout")
                if layout_name:
                    st.session_state.custom_layouts[layout_name] = {
                        "name": page_name,
                        "description": page_description,
                        "settings": {
                            "width": page_width,
                            "grid": grid_size,
                            "responsive": responsive_mode
                        }
                    }
                    st.success(f"Layout '{layout_name}' saved!")
        
        with col2:
            if st.button("📂 Load Layout"):
                if st.session_state.custom_layouts:
                    selected_layout = st.selectbox("Select Layout", list(st.session_state.custom_layouts.keys()))
                    if st.button("Load"):
                        st.success(f"Loaded layout '{selected_layout}'")
                else:
                    st.info("No saved layouts found")
        
        with col3:
            if st.button("🗑️ Clear Canvas"):
                st.warning("Canvas cleared!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Technical Architecture page
def render_technical_architecture():
    """Render technical architecture demonstrations"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ Technical Architecture</h1>
        <p>Advanced technology demonstrations and system design</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Architecture tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗄️ Database Layer", "🤖 MCP Server", "👥 CrewAI", "⚡ Circuit Breaker", "🔄 CQRS Pattern"])
    
    with tab1:
        st.markdown('<div class="tech-demo">', unsafe_allow_html=True)
        
        st.subheader("🗄️ Multi-Database Architecture")
        
        # Database overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🔵 MS SQL Server**
            - Transactional data
            - ACID compliance
            - Complex queries
            - Reporting
            """)
            
            if st.button("Test MS SQL Connection"):
                st.success("✅ MS SQL Server connected")
                st.code("""
                SELECT TOP 10 
                    client_name, 
                    total_revenue,
                    last_transaction_date
                FROM clients 
                ORDER BY total_revenue DESC
                """)
        
        with col2:
            st.markdown("""
            **🟢 MongoDB**
            - Document storage
            - Flexible schema
            - Real-time data
            - User preferences
            """)
            
            if st.button("Test MongoDB Connection"):
                st.success("✅ MongoDB connected")
                st.code("""
                db.user_sessions.find({
                    "user_id": "john_smith",
                    "session_date": {
                        "$gte": ISODate("2024-01-01")
                    }
                }).sort({"timestamp": -1})
                """)
        
        with col3:
            st.markdown("""
            **🟡 FAISS Vector DB**
            - Similarity search
            - AI embeddings
            - Semantic queries
            - Recommendations
            """)
            
            if st.button("Test FAISS Connection"):
                st.success("✅ FAISS Vector DB connected")
                st.code("""
                import faiss
                import numpy as np
                
                # Search similar clients
                query_vector = np.random.random(128)
                distances, indices = index.search(
                    query_vector.reshape(1, -1), k=5
                )
                """)
        
        # Database performance metrics
        st.subheader("📊 Database Performance")
        
        db_metrics = pd.DataFrame({
            'Database': ['MS SQL', 'MongoDB', 'FAISS'],
            'Response Time (ms)': [45, 23, 12],
            'Throughput (ops/sec)': [1200, 2500, 5000],
            'Storage (GB)': [250, 180, 45]
        })
        
        fig = px.bar(db_metrics, x='Database', y='Response Time (ms)', title="Database Response Times")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="tech-demo">', unsafe_allow_html=True)
        
        st.subheader("🤖 Model Context Protocol (MCP) Server")
        
        st.markdown("""
        The MCP Server provides a standardized interface for AI models to interact with banking tools and data sources.
        """)
        
        # MCP Server status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔧 Registered Tools**
            - Client data retrieval
            - Risk assessment calculator
            - Market data fetcher
            - Compliance checker
            - Report generator
            """)
        
        with col2:
            st.markdown("""
            **📊 Server Status**
            - Status: 🟢 Online
            - Uptime: 99.9%
            - Active connections: 15
            - Tools registered: 25
            - Avg response time: 120ms
            """)
        
        # MCP Tool demonstration
        st.subheader("🛠️ Tool Execution Demo")
        
        selected_tool = st.selectbox(
            "Select MCP Tool",
            ["client_risk_assessment", "market_data_fetch", "compliance_check", "report_generate"]
        )
        
        if st.button("Execute Tool"):
            with st.spinner("Executing MCP tool..."):
                import time
                time.sleep(2)
                
                if selected_tool == "client_risk_assessment":
                    st.json({
                        "tool": "client_risk_assessment",
                        "client_id": "12345",
                        "risk_score": 7.2,
                        "factors": ["Credit history", "Industry volatility", "Geographic exposure"],
                        "recommendation": "Monitor closely"
                    })
                elif selected_tool == "market_data_fetch":
                    st.json({
                        "tool": "market_data_fetch",
                        "symbol": "GBPUSD",
                        "price": 1.2745,
                        "change": "+0.0023",
                        "timestamp": "2024-06-27T10:30:00Z"
                    })
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="tech-demo">', unsafe_allow_html=True)
        
        st.subheader("👥 CrewAI Multi-Agent Framework")
        
        st.markdown("""
        CrewAI orchestrates multiple AI agents working together to complete complex banking tasks.
        """)
        
        # Agent hierarchy
        st.subheader("🏢 Agent Hierarchy")
        
        agents = {
            "Supervisor Agent": {
                "role": "Task coordination and delegation",
                "status": "🟢 Active",
                "tasks": 15
            },
            "Risk Analysis Agent": {
                "role": "Credit and market risk assessment", 
                "status": "🟢 Active",
                "tasks": 8
            },
            "Client Intelligence Agent": {
                "role": "Client data analysis and insights",
                "status": "🟢 Active", 
                "tasks": 12
            },
            "Compliance Agent": {
                "role": "Regulatory compliance checking",
                "status": "🟡 Busy",
                "tasks": 5
            },
            "Market Data Agent": {
                "role": "Real-time market information",
                "status": "🟢 Active",
                "tasks": 20
            }
        }
        
        for agent_name, agent_info in agents.items():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            with col1:
                st.write(f"**{agent_name}**")
            with col2:
                st.write(agent_info["role"])
            with col3:
                st.write(agent_info["status"])
            with col4:
                st.write(f"{agent_info['tasks']} tasks")
        
        # Agent workflow demo
        st.subheader("🔄 Workflow Execution")
        
        if st.button("Start Multi-Agent Task"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            workflow_steps = [
                "Supervisor Agent: Analyzing task requirements...",
                "Risk Analysis Agent: Calculating risk metrics...", 
                "Client Intelligence Agent: Gathering client insights...",
                "Market Data Agent: Fetching current market data...",
                "Compliance Agent: Checking regulatory requirements...",
                "Supervisor Agent: Consolidating results..."
            ]
            
            for i, step in enumerate(workflow_steps):
                status_text.text(step)
                progress_bar.progress((i + 1) / len(workflow_steps))
                time.sleep(1)
            
            st.success("✅ Multi-agent task completed successfully!")
            
            # Show results
            st.json({
                "task_id": "CREW_001",
                "status": "completed",
                "agents_involved": 5,
                "execution_time": "6.2 seconds",
                "result": {
                    "risk_score": 6.8,
                    "client_insights": "High-value client with growth potential",
                    "market_conditions": "Favorable for lending",
                    "compliance_status": "All checks passed"
                }
            })
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="tech-demo">', unsafe_allow_html=True)
        
        st.subheader("⚡ Circuit Breaker Pattern")
        
        st.markdown("""
        Circuit breakers prevent cascading failures by monitoring service health and failing fast when issues are detected.
        """)
        
        # Circuit breaker status
        services = {
            "Payment Processing": {"status": "🟢 Closed", "failure_rate": "0.1%", "response_time": "45ms"},
            "Risk Assessment": {"status": "🟢 Closed", "failure_rate": "0.3%", "response_time": "120ms"},
            "Market Data Feed": {"status": "🟡 Half-Open", "failure_rate": "2.1%", "response_time": "250ms"},
            "Compliance Check": {"status": "🟢 Closed", "failure_rate": "0.0%", "response_time": "80ms"},
            "Client Database": {"status": "🔴 Open", "failure_rate": "15.2%", "response_time": "timeout"}
        }
        
        st.subheader("🔧 Service Circuit Breakers")
        
        for service, metrics in services.items():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            with col1:
                st.write(f"**{service}**")
            with col2:
                st.write(metrics["status"])
            with col3:
                st.write(f"Failure: {metrics['failure_rate']}")
            with col4:
                st.write(f"Response: {metrics['response_time']}")
        
        # Circuit breaker simulation
        st.subheader("🧪 Circuit Breaker Simulation")
        
        selected_service = st.selectbox("Select Service", list(services.keys()))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Simulate Success"):
                st.success(f"✅ {selected_service}: Request successful")
        
        with col2:
            if st.button("Simulate Failure"):
                st.error(f"❌ {selected_service}: Request failed")
        
        with col3:
            if st.button("Reset Circuit"):
                st.info(f"🔄 {selected_service}: Circuit breaker reset")
        
        # Circuit breaker metrics
        st.subheader("📊 Circuit Breaker Metrics")
        
        metrics_data = pd.DataFrame({
            'Time': pd.date_range(start='2024-06-27 09:00', periods=24, freq='H'),
            'Success Rate': np.random.uniform(95, 100, 24),
            'Response Time': np.random.uniform(50, 200, 24)
        })
        
        fig = px.line(metrics_data, x='Time', y='Success Rate', title="Service Success Rate Over Time")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="tech-demo">', unsafe_allow_html=True)
        
        st.subheader("🔄 CQRS (Command Query Responsibility Segregation)")
        
        st.markdown("""
        CQRS separates read and write operations to optimize performance and scalability.
        """)
        
        # CQRS overview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📝 Command Side (Write)**
            - Handle business operations
            - Validate and process commands
            - Update write database
            - Publish events
            """)
            
            st.subheader("Command Examples")
            commands = [
                "CreateClient",
                "UpdateDeal", 
                "ProcessPayment",
                "AssignRiskScore",
                "GenerateReport"
            ]
            
            selected_command = st.selectbox("Select Command", commands)
            
            if st.button("Execute Command"):
                st.success(f"✅ Command '{selected_command}' executed successfully")
                st.json({
                    "command_id": f"CMD_{np.random.randint(1000, 9999)}",
                    "command_type": selected_command,
                    "timestamp": datetime.now().isoformat(),
                    "status": "completed",
                    "events_published": 2
                })
        
        with col2:
            st.markdown("""
            **📖 Query Side (Read)**
            - Optimized for reading
            - Denormalized views
            - Fast query performance
            - Read-only operations
            """)
            
            st.subheader("Query Examples")
            queries = [
                "GetClientPortfolio",
                "GetDealPipeline",
                "GetRiskReport",
                "GetPerformanceMetrics",
                "GetComplianceStatus"
            ]
            
            selected_query = st.selectbox("Select Query", queries)
            
            if st.button("Execute Query"):
                st.success(f"✅ Query '{selected_query}' executed successfully")
                st.json({
                    "query_id": f"QRY_{np.random.randint(1000, 9999)}",
                    "query_type": selected_query,
                    "timestamp": datetime.now().isoformat(),
                    "execution_time": f"{np.random.randint(10, 100)}ms",
                    "records_returned": np.random.randint(1, 1000)
                })
        
        # Event sourcing
        st.subheader("📋 Event Store")
        
        events = pd.DataFrame({
            'Event ID': [f"EVT_{i:04d}" for i in range(1, 11)],
            'Event Type': np.random.choice(['ClientCreated', 'DealUpdated', 'PaymentProcessed', 'RiskAssessed'], 10),
            'Timestamp': pd.date_range(start='2024-06-27 09:00', periods=10, freq='15min'),
            'Aggregate ID': [f"AGG_{np.random.randint(100, 999)}" for _ in range(10)],
            'Version': np.random.randint(1, 5, 10)
        })
        
        st.dataframe(events, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main application
def main():
    """Main application entry point"""
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to appropriate page
    if selected_page == "Dashboard":
        render_dashboard()
    elif selected_page == "Client 360":
        render_client360()
    elif selected_page == "Pipeline":
        st.info("🚧 Pipeline Management - Coming Soon")
    elif selected_page == "AI Assistant":
        st.info("🚧 AI Assistant - Coming Soon")
    elif selected_page == "News Intelligence":
        st.info("🚧 News Intelligence - Coming Soon")
    elif selected_page == "Risk Management":
        st.info("🚧 Risk Management - Coming Soon")
    elif selected_page == "Analytics":
        st.info("🚧 Advanced Analytics - Coming Soon")
    elif selected_page == "Admin Config":
        render_admin_config()
    elif selected_page == "UI Builder":
        render_ui_builder()
    elif selected_page == "Technical Architecture":
        render_technical_architecture()

if __name__ == "__main__":
    main()

