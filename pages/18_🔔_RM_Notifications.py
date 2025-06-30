import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="RM Notifications", page_icon="🔔", layout="wide")

st.title("🔔 RM Notifications & Alerts")

# Generate synthetic notification data
@st.cache_data
def generate_notification_data():
    notifications = []
    clients = ['TechCorp Ltd', 'Manufacturing Inc', 'RetailChain PLC', 'EnergyPlus Ltd', 'HealthcarePro']
    notification_types = ['Deal Alert', 'Risk Warning', 'Payment Due', 'Meeting Reminder', 'Compliance Alert', 'Opportunity']
    priorities = ['High', 'Medium', 'Low', 'Critical']
    statuses = ['Unread', 'Read', 'Acknowledged', 'Resolved']
    
    for i in range(50):
        notification_time = datetime.now() - timedelta(hours=random.randint(1, 168))  # Last week
        notifications.append({
            'id': f"NOTIF-{1000+i}",
            'timestamp': notification_time,
            'client': random.choice(clients),
            'type': random.choice(notification_types),
            'priority': random.choice(priorities),
            'status': random.choice(statuses),
            'title': f"Alert for {random.choice(clients)}",
            'message': f"Important notification regarding {random.choice(notification_types).lower()}",
            'rm_assigned': random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams']),
            'action_required': random.choice([True, False]),
            'due_date': notification_time + timedelta(days=random.randint(1, 14)),
            'source': random.choice(['System', 'AI Engine', 'Manual', 'External API']),
            'category': random.choice(['Client Management', 'Risk Management', 'Compliance', 'Sales'])
        })
    
    return pd.DataFrame(notifications)

notification_df = generate_notification_data()

# Notification summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    unread_count = len(notification_df[notification_df['status'] == 'Unread'])
    st.metric("📬 Unread", unread_count, delta=f"+{random.randint(2, 8)} today")

with col2:
    critical_count = len(notification_df[notification_df['priority'] == 'Critical'])
    st.metric("🚨 Critical", critical_count, delta="Immediate attention")

with col3:
    action_required = len(notification_df[notification_df['action_required'] == True])
    st.metric("⚡ Action Required", action_required, delta=f"{random.randint(5, 12)} pending")

with col4:
    overdue_count = len(notification_df[notification_df['due_date'] < datetime.now()])
    st.metric("⏰ Overdue", overdue_count, delta="Review needed")

# Filter and search section
st.subheader("🔍 Filter Notifications")

col1, col2, col3, col4 = st.columns(4)

with col1:
    priority_filter = st.selectbox("Priority", ['All'] + list(notification_df['priority'].unique()))

with col2:
    status_filter = st.selectbox("Status", ['All'] + list(notification_df['status'].unique()))

with col3:
    type_filter = st.selectbox("Type", ['All'] + list(notification_df['type'].unique()))

with col4:
    rm_filter = st.selectbox("RM", ['All'] + list(notification_df['rm_assigned'].unique()))

# Apply filters
filtered_notifications = notification_df.copy()

if priority_filter != 'All':
    filtered_notifications = filtered_notifications[filtered_notifications['priority'] == priority_filter]
if status_filter != 'All':
    filtered_notifications = filtered_notifications[filtered_notifications['status'] == status_filter]
if type_filter != 'All':
    filtered_notifications = filtered_notifications[filtered_notifications['type'] == type_filter]
if rm_filter != 'All':
    filtered_notifications = filtered_notifications[filtered_notifications['rm_assigned'] == rm_filter]

# Sort by timestamp (newest first)
filtered_notifications = filtered_notifications.sort_values('timestamp', ascending=False)

# Notification feed
st.subheader("📋 Notification Feed")

# Priority color mapping
priority_colors = {
    'Critical': '🔴',
    'High': '🟠', 
    'Medium': '🟡',
    'Low': '🟢'
}

status_colors = {
    'Unread': '🔵',
    'Read': '⚪',
    'Acknowledged': '🟢',
    'Resolved': '✅'
}

# Display notifications
for idx, notif in filtered_notifications.head(20).iterrows():
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 4, 2, 2])
        
        with col1:
            st.markdown(f"{priority_colors[notif['priority']]}")
            st.caption(f"{status_colors[notif['status']]}")
        
        with col2:
            time_ago = datetime.now() - notif['timestamp']
            if time_ago.days > 0:
                time_str = f"{time_ago.days}d ago"
            elif time_ago.seconds > 3600:
                time_str = f"{time_ago.seconds//3600}h ago"
            else:
                time_str = f"{time_ago.seconds//60}m ago"
            
            st.markdown(f"**{notif['title']}**")
            st.caption(f"{notif['client']} • {notif['type']} • {time_str}")
            st.write(notif['message'])
        
        with col3:
            st.markdown(f"**RM:** {notif['rm_assigned']}")
            st.markdown(f"**Priority:** {notif['priority']}")
            if notif['action_required']:
                st.markdown("⚡ **Action Required**")
        
        with col4:
            if st.button("Mark Read", key=f"read_{notif['id']}"):
                st.success("Marked as read!")
            
            if notif['action_required']:
                if st.button("Take Action", key=f"action_{notif['id']}"):
                    st.success("Action initiated!")
        
        st.divider()

# Analytics tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "⏰ Timeline", "🎯 Actions", "⚙️ Settings"])

with tab1:
    st.subheader("📊 Notification Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Notifications by priority
        priority_counts = notification_df['priority'].value_counts()
        fig_priority = px.pie(
            values=priority_counts.values,
            names=priority_counts.index,
            title="Notifications by Priority",
            color_discrete_map={
                'Critical': '#dc3545',
                'High': '#fd7e14',
                'Medium': '#ffc107',
                'Low': '#28a745'
            }
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    
    with col2:
        # Notifications by type
        type_counts = notification_df['type'].value_counts()
        fig_type = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Notifications by Type"
        )
        st.plotly_chart(fig_type, use_container_width=True)
    
    # Daily notification trend
    daily_notifications = notification_df.groupby(notification_df['timestamp'].dt.date).size().reset_index(name='count')
    fig_trend = px.line(
        daily_notifications,
        x='timestamp',
        y='count',
        title="Daily Notification Volume"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    st.subheader("⏰ Notification Timeline")
    
    # Recent notifications timeline
    recent_notifications = notification_df.head(15).copy()
    recent_notifications['hours_ago'] = (datetime.now() - recent_notifications['timestamp']).dt.total_seconds() / 3600
    
    fig_timeline = px.scatter(
        recent_notifications,
        x='hours_ago',
        y='priority',
        size='action_required',
        color='type',
        hover_data=['client', 'title'],
        title="Recent Notifications Timeline"
    )
    fig_timeline.update_xaxis(title="Hours Ago")
    st.plotly_chart(fig_timeline, use_container_width=True)

with tab3:
    st.subheader("🎯 Action Items Dashboard")
    
    # Action required notifications
    action_notifications = notification_df[notification_df['action_required'] == True]
    
    st.markdown(f"**{len(action_notifications)} notifications require action**")
    
    for _, action in action_notifications.head(10).iterrows():
        with st.expander(f"{priority_colors[action['priority']]} {action['title']} - {action['client']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Message:** {action['message']}")
                st.markdown(f"**Type:** {action['type']}")
                st.markdown(f"**Category:** {action['category']}")
                
                days_until_due = (action['due_date'] - datetime.now()).days
                if days_until_due < 0:
                    st.markdown(f"**Due:** ⚠️ Overdue by {abs(days_until_due)} days")
                else:
                    st.markdown(f"**Due:** {days_until_due} days")
            
            with col2:
                st.markdown(f"**RM:** {action['rm_assigned']}")
                st.markdown(f"**Priority:** {action['priority']}")
                st.markdown(f"**Source:** {action['source']}")
                
                if st.button("Complete Action", key=f"complete_{action['id']}"):
                    st.success("Action completed!")

with tab4:
    st.subheader("⚙️ Notification Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Alert Preferences**")
        
        email_notifications = st.checkbox("Email Notifications", value=True)
        sms_alerts = st.checkbox("SMS Alerts for Critical", value=True)
        desktop_notifications = st.checkbox("Desktop Notifications", value=False)
        mobile_push = st.checkbox("Mobile Push Notifications", value=True)
        
        st.markdown("**Frequency Settings**")
        digest_frequency = st.selectbox("Daily Digest", ["Disabled", "Morning", "Evening", "Both"])
        summary_frequency = st.selectbox("Weekly Summary", ["Disabled", "Monday", "Friday"])
    
    with col2:
        st.markdown("**Priority Thresholds**")
        
        critical_threshold = st.slider("Critical Alert Threshold", 1, 10, 8)
        high_threshold = st.slider("High Priority Threshold", 1, 10, 6)
        
        st.markdown("**Auto-Actions**")
        auto_acknowledge = st.checkbox("Auto-acknowledge read notifications", value=False)
        auto_escalate = st.checkbox("Auto-escalate overdue actions", value=True)
        smart_filtering = st.checkbox("AI-powered smart filtering", value=True)
        
        if st.button("💾 Save Settings"):
            st.success("Notification settings saved!")

# Quick actions sidebar
with st.sidebar:
    st.subheader("🚀 Quick Actions")
    
    if st.button("📬 Mark All as Read"):
        st.success("All notifications marked as read!")
    
    if st.button("🔔 Create Custom Alert"):
        st.info("Custom alert dialog opened!")
    
    if st.button("📊 Generate Report"):
        st.success("Notification report generated!")
    
    if st.button("⚙️ Bulk Actions"):
        st.info("Bulk action menu opened!")
    
    st.subheader("📈 Quick Stats")
    
    today_notifications = len(notification_df[notification_df['timestamp'].dt.date == datetime.now().date()])
    st.metric("Today's Notifications", today_notifications)
    
    response_time = random.uniform(15, 45)
    st.metric("Avg Response Time", f"{response_time:.0f} min")
    
    resolution_rate = random.uniform(85, 95)
    st.metric("Resolution Rate", f"{resolution_rate:.1f}%")

st.markdown("""
---
**RM Notifications Features:**
- 🔔 Real-time notification system with priority management
- 📊 Comprehensive analytics and reporting
- ⚡ Action item tracking and management
- 🎯 Smart filtering and categorization
- 📱 Multi-channel alert delivery (Email, SMS, Push)
- 🤖 AI-powered notification intelligence
""")

