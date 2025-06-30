import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Admin Configuration",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Admin Configuration")
st.markdown("System administration and configuration management")

# Check admin permissions
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'Administrator'

if st.session_state.user_role not in ['Administrator', 'Super Admin']:
    st.error("🚫 Access Denied: Administrator privileges required")
    st.stop()

# Admin tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 User Management", 
    "🔐 Roles & Permissions", 
    "🎨 UI Configuration", 
    "🌐 Localization", 
    "🔧 System Settings"
])

with tab1:
    st.header("👥 User Management")
    
    # User creation form
    with st.expander("➕ Add New User"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_first_name = st.text_input("First Name")
            new_last_name = st.text_input("Last Name")
        
        with col2:
            new_role = st.selectbox("Role", [
                "Relationship Manager",
                "Credit Analyst", 
                "Risk Manager",
                "Administrator",
                "Read-Only User"
            ])
            new_department = st.selectbox("Department", [
                "Commercial Banking",
                "Risk Management",
                "Credit",
                "Operations",
                "IT"
            ])
            new_status = st.selectbox("Status", ["Active", "Inactive", "Pending"])
        
        if st.button("Create User"):
            st.success(f"✅ User '{new_username}' created successfully!")
    
    # Existing users table
    st.subheader("📋 Existing Users")
    
    users_data = pd.DataFrame({
        'Username': ['john.smith', 'sarah.johnson', 'michael.chen', 'emma.williams'],
        'Name': ['John Smith', 'Sarah Johnson', 'Michael Chen', 'Emma Williams'],
        'Email': ['john.smith@bank.com', 'sarah.johnson@bank.com', 'michael.chen@bank.com', 'emma.williams@bank.com'],
        'Role': ['Senior RM', 'Credit Analyst', 'Risk Manager', 'Administrator'],
        'Department': ['Commercial', 'Credit', 'Risk', 'IT'],
        'Status': ['Active', 'Active', 'Active', 'Active'],
        'Last Login': ['2024-06-27 09:15', '2024-06-27 08:45', '2024-06-26 16:30', '2024-06-27 07:20']
    })
    
    # Add action buttons
    users_data['Actions'] = ['Edit | Disable | Reset Password'] * len(users_data)
    
    st.dataframe(users_data, use_container_width=True)

with tab2:
    st.header("🔐 Roles & Permissions")
    
    # Role selection
    roles = {
        "Super Administrator": {
            "description": "Full system access and control",
            "users": 2,
            "permissions": {
                "System Administration": ["Read", "Write", "Delete", "Configure"],
                "User Management": ["Read", "Write", "Delete", "Manage"],
                "Client Management": ["Read", "Write", "Delete", "Export"],
                "Deal Management": ["Read", "Write", "Delete", "Approve"],
                "Reports & Analytics": ["Read", "Write", "Delete", "Export"],
                "Configuration": ["Read", "Write", "Delete", "Deploy"]
            }
        },
        "Relationship Manager": {
            "description": "Client and deal management",
            "users": 15,
            "permissions": {
                "System Administration": [],
                "User Management": ["Read"],
                "Client Management": ["Read", "Write", "Export"],
                "Deal Management": ["Read", "Write"],
                "Reports & Analytics": ["Read", "Export"],
                "Configuration": ["Read"]
            }
        },
        "Credit Analyst": {
            "description": "Credit assessment and analysis",
            "users": 8,
            "permissions": {
                "System Administration": [],
                "User Management": [],
                "Client Management": ["Read"],
                "Deal Management": ["Read", "Write"],
                "Reports & Analytics": ["Read", "Write", "Export"],
                "Configuration": ["Read"]
            }
        },
        "Read-Only User": {
            "description": "View-only access to reports",
            "users": 5,
            "permissions": {
                "System Administration": [],
                "User Management": [],
                "Client Management": ["Read"],
                "Deal Management": ["Read"],
                "Reports & Analytics": ["Read"],
                "Configuration": []
            }
        }
    }
    
    selected_role = st.selectbox("Select Role to Configure", list(roles.keys()))
    role_info = roles[selected_role]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"**Description:** {role_info['description']}")
        st.markdown(f"**Users with this role:** {role_info['users']}")
        
        if st.button("Create New Role"):
            st.info("Role creation dialog would open here")
        
        if st.button("Clone Role"):
            st.info(f"Cloning role '{selected_role}'")
    
    with col2:
        st.subheader("Permissions Matrix")
        
        for category, perms in role_info['permissions'].items():
            st.markdown(f"**{category}**")
            
            all_perms = ["Read", "Write", "Delete", "Configure", "Manage", "Approve", "Export", "Deploy"]
            cols = st.columns(len(all_perms))
            
            for i, perm in enumerate(all_perms):
                with cols[i]:
                    checked = perm in perms
                    st.checkbox(
                        perm, 
                        value=checked, 
                        key=f"{selected_role}_{category}_{perm}",
                        disabled=selected_role == "Super Administrator"
                    )

with tab3:
    st.header("🎨 UI Configuration")
    
    # Theme configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Theme Settings")
        
        themes = {
            "Corporate Blue": {"primary": "#3B82F6", "secondary": "#1E40AF", "accent": "#60A5FA"},
            "Banking Green": {"primary": "#10B981", "secondary": "#047857", "accent": "#34D399"},
            "Professional Gray": {"primary": "#6B7280", "secondary": "#374151", "accent": "#9CA3AF"},
            "Premium Purple": {"primary": "#8B5CF6", "secondary": "#7C3AED", "accent": "#A78BFA"}
        }
        
        selected_theme = st.selectbox("Select Theme", list(themes.keys()))
        
        # Color preview
        theme_colors = themes[selected_theme]
        st.markdown(f"""
        <div style="display: flex; gap: 10px; margin: 10px 0;">
            <div style="width: 50px; height: 50px; background-color: {theme_colors['primary']}; border-radius: 5px;"></div>
            <div style="width: 50px; height: 50px; background-color: {theme_colors['secondary']}; border-radius: 5px;"></div>
            <div style="width: 50px; height: 50px; background-color: {theme_colors['accent']}; border-radius: 5px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Custom colors
        st.markdown("**Custom Colors**")
        primary_color = st.color_picker("Primary Color", theme_colors['primary'])
        secondary_color = st.color_picker("Secondary Color", theme_colors['secondary'])
        accent_color = st.color_picker("Accent Color", theme_colors['accent'])
    
    with col2:
        st.subheader("📐 Layout Settings")
        
        sidebar_position = st.selectbox("Sidebar Position", ["Left", "Right", "Collapsible"])
        header_style = st.selectbox("Header Style", ["Fixed", "Sticky", "Static"])
        content_width = st.selectbox("Content Width", ["Full Width", "Boxed", "Fluid"])
        card_style = st.selectbox("Card Style", ["Shadow", "Border", "Flat", "Elevated"])
        
        st.subheader("🔤 Typography")
        
        font_family = st.selectbox("Font Family", [
            "Inter", "Roboto", "Open Sans", "Lato", "Montserrat"
        ])
        font_size = st.selectbox("Base Font Size", ["14px", "15px", "16px", "17px", "18px"])
        
        st.subheader("📱 Responsive Settings")
        
        mobile_sidebar = st.checkbox("Collapsible sidebar on mobile", value=True)
        touch_friendly = st.checkbox("Touch-friendly interface", value=True)
        
    # Apply settings
    if st.button("💾 Apply UI Settings"):
        st.success("✅ UI settings applied successfully!")
        st.balloons()

with tab4:
    st.header("🌐 Localization Management")
    
    # Language settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗣️ Supported Languages")
        
        languages = {
            "🇬🇧 English": {"code": "en", "active": True, "completion": "100%"},
            "🇫🇷 French": {"code": "fr", "active": True, "completion": "95%"},
            "🇩🇪 German": {"code": "de", "active": False, "completion": "80%"},
            "🇪🇸 Spanish": {"code": "es", "active": False, "completion": "75%"},
            "🇮🇹 Italian": {"code": "it", "active": False, "completion": "60%"}
        }
        
        for lang, info in languages.items():
            col_lang, col_active, col_completion, col_action = st.columns([3, 1, 1, 1])
            
            with col_lang:
                st.write(lang)
            with col_active:
                st.checkbox("Active", value=info["active"], key=f"lang_{info['code']}")
            with col_completion:
                st.write(info["completion"])
            with col_action:
                if st.button("Edit", key=f"edit_{info['code']}"):
                    st.info(f"Editing {lang} translations...")
    
    with col2:
        st.subheader("🏷️ Quick Label Editor")
        
        # Sample labels for editing
        labels = {
            "dashboard.title": "Dashboard",
            "client.name": "Client Name", 
            "deal.value": "Deal Value",
            "risk.score": "Risk Score",
            "menu.analytics": "Analytics"
        }
        
        selected_label = st.selectbox("Select Label", list(labels.keys()))
        
        # Edit form
        english_text = st.text_input("English", value=labels[selected_label])
        french_text = st.text_input("French", placeholder="Tableau de bord")
        german_text = st.text_input("German", placeholder="Armaturenbrett")
        
        if st.button("💾 Save Label"):
            st.success(f"✅ Label '{selected_label}' updated!")
    
    # Bulk operations
    st.subheader("📦 Bulk Operations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        uploaded_file = st.file_uploader("Import Translations", type=['json', 'csv'])
        if uploaded_file:
            st.success("✅ Translations imported successfully!")
    
    with col2:
        if st.button("📤 Export All Translations"):
            st.download_button(
                label="Download translations.json",
                data=json.dumps(labels, indent=2),
                file_name="translations.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("🔄 Sync with Translation Service"):
            st.info("Syncing with external translation service...")

with tab5:
    st.header("🔧 System Settings")
    
    # Security settings
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 Security Configuration")
        
        session_timeout = st.number_input("Session Timeout (minutes)", value=30, min_value=5, max_value=480)
        password_expiry = st.number_input("Password Expiry (days)", value=90, min_value=30, max_value=365)
        max_login_attempts = st.number_input("Max Login Attempts", value=3, min_value=1, max_value=10)
        
        st.markdown("**Password Requirements**")
        min_length = st.number_input("Minimum Length", value=8, min_value=6, max_value=20)
        require_uppercase = st.checkbox("Require uppercase letters", value=True)
        require_numbers = st.checkbox("Require numbers", value=True)
        require_symbols = st.checkbox("Require special characters", value=True)
        
        st.markdown("**Audit & Logging**")
        enable_audit = st.checkbox("Enable audit logging", value=True)
        log_retention = st.number_input("Log retention (days)", value=365, min_value=30, max_value=2555)
    
    with col2:
        st.subheader("💾 Data Management")
        
        data_retention = st.number_input("Data Retention (years)", value=7, min_value=1, max_value=20)
        backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly"])
        backup_retention = st.number_input("Backup Retention (months)", value=12, min_value=1, max_value=60)
        
        st.markdown("**Performance Settings**")
        cache_duration = st.number_input("Cache Duration (hours)", value=24, min_value=1, max_value=168)
        max_concurrent_users = st.number_input("Max Concurrent Users", value=100, min_value=10, max_value=1000)
        
        st.markdown("**Maintenance**")
        maintenance_window = st.selectbox("Maintenance Window", [
            "Sunday 02:00-04:00",
            "Saturday 23:00-01:00", 
            "Daily 01:00-02:00"
        ])
        
        auto_updates = st.checkbox("Enable automatic updates", value=False)
    
    # System status
    st.subheader("📊 System Status")
    
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    
    with status_col1:
        st.metric("System Uptime", "99.9%", "0.1%")
    
    with status_col2:
        st.metric("Active Users", "47", "+3")
    
    with status_col3:
        st.metric("Database Size", "2.3 GB", "+45 MB")
    
    with status_col4:
        st.metric("Response Time", "120ms", "-15ms")
    
    # Apply settings
    if st.button("💾 Apply System Settings"):
        st.success("✅ System settings applied successfully!")
        st.info("Some changes may require a system restart to take effect.")

