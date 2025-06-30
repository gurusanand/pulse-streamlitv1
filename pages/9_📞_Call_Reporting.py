import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="Call Reporting & Meeting Management",
    page_icon="📞",
    layout="wide"
)

st.title("📞 Call Reporting & Meeting Management")
st.markdown("Log and generate call/meeting reports with AI assistance, MS Teams/Zoom integration, and action item tracking")

# Generate sample call/meeting data
@st.cache_data
def generate_call_data():
    meeting_types = ['Client Call', 'Internal Meeting', 'Prospect Call', 'Review Meeting', 'Training Session']
    platforms = ['MS Teams', 'Zoom', 'Phone', 'In-Person', 'Google Meet']
    statuses = ['Completed', 'Scheduled', 'Cancelled', 'Rescheduled']
    
    calls = []
    for i in range(150):
        call_date = datetime.now() - timedelta(days=random.randint(0, 90))
        call = {
            'call_id': f'CALL-{3000 + i}',
            'meeting_type': random.choice(meeting_types),
            'client_name': f'Client {chr(65 + i % 26)}{i % 50}',
            'participants': random.randint(2, 8),
            'duration_minutes': random.randint(15, 120),
            'platform': random.choice(platforms),
            'date': call_date,
            'status': random.choice(statuses),
            'rm_name': random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams', 'David Brown', 'Lisa Davis']),
            'transcript_available': random.choice([True, False]),
            'ai_summary_generated': random.choice([True, False]),
            'action_items_count': random.randint(0, 8),
            'follow_up_required': random.choice([True, False]),
            'satisfaction_rating': random.uniform(7.0, 10.0) if random.random() > 0.3 else None,
            'deal_value_discussed': random.uniform(0, 10000000) if random.random() > 0.5 else 0,
            'next_meeting_scheduled': random.choice([True, False]),
            'recording_available': random.choice([True, False])
        }
        calls.append(call)
    
    return pd.DataFrame(calls)

calls_df = generate_call_data()

# Call reporting overview
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_calls = len(calls_df[calls_df['status'] == 'Completed'])
    calls_this_week = len(calls_df[
        (calls_df['status'] == 'Completed') & 
        (calls_df['date'] >= datetime.now() - timedelta(days=7))
    ])
    st.metric(
        label="📞 Total Calls",
        value=total_calls,
        delta=f"+{calls_this_week} this week"
    )

with col2:
    total_duration = calls_df[calls_df['status'] == 'Completed']['duration_minutes'].sum()
    avg_duration = calls_df[calls_df['status'] == 'Completed']['duration_minutes'].mean()
    st.metric(
        label="⏱️ Total Duration",
        value=f"{total_duration/60:.1f} hours",
        delta=f"Avg: {avg_duration:.0f} min"
    )

with col3:
    total_action_items = calls_df['action_items_count'].sum()
    completed_action_items = int(total_action_items * 0.73)  # Assume 73% completion rate
    st.metric(
        label="✅ Action Items",
        value=f"{completed_action_items}/{total_action_items}",
        delta="73% completion rate"
    )

with col4:
    avg_satisfaction = calls_df['satisfaction_rating'].mean()
    satisfaction_trend = 0.3  # Positive trend
    st.metric(
        label="😊 Avg Satisfaction",
        value=f"{avg_satisfaction:.1f}/10",
        delta=f"+{satisfaction_trend:.1f}"
    )

# Main interface tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 New Call Report", "📋 Call History", "🎯 Action Items", "📊 Analytics", "⚙️ Settings"])

with tab1:
    st.subheader("📝 Create New Call Report")
    
    # Call report form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Meeting Details**")
        
        meeting_type = st.selectbox(
            "Meeting Type",
            options=['Client Call', 'Internal Meeting', 'Prospect Call', 'Review Meeting', 'Training Session']
        )
        
        client_name = st.text_input("Client/Participant Name")
        
        meeting_date = st.date_input("Meeting Date", value=datetime.now().date())
        meeting_time = st.time_input("Meeting Time", value=datetime.now().time())
        
        duration = st.number_input("Duration (minutes)", min_value=5, max_value=480, value=60, step=5)
        
        platform = st.selectbox(
            "Platform",
            options=['MS Teams', 'Zoom', 'Phone', 'In-Person', 'Google Meet']
        )
        
        participants = st.text_area("Participants", placeholder="List all participants...")
    
    with col2:
        st.markdown("**Integration Options**")
        
        # MS Teams/Zoom integration
        integration_enabled = st.checkbox("🔗 Auto-import from Teams/Zoom", value=True)
        
        if integration_enabled:
            st.info("✅ Connected to MS Teams and Zoom. Meeting details will be auto-populated.")
            
            # Simulated integration options
            auto_transcript = st.checkbox("📝 Auto-generate transcript", value=True)
            auto_summary = st.checkbox("🤖 AI-powered summary", value=True)
            auto_action_items = st.checkbox("🎯 Extract action items automatically", value=True)
            auto_sentiment = st.checkbox("😊 Sentiment analysis", value=False)
        
        # Recording options
        st.markdown("**Recording & Documentation**")
        
        recording_available = st.checkbox("🎥 Recording available")
        transcript_available = st.checkbox("📄 Transcript available")
        
        if transcript_available:
            transcript_quality = st.selectbox(
                "Transcript Quality",
                options=['Excellent', 'Good', 'Fair', 'Poor']
            )
    
    # Meeting content
    st.markdown("**Meeting Content**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        meeting_objective = st.text_area(
            "Meeting Objective",
            placeholder="What was the purpose of this meeting?"
        )
        
        key_discussion_points = st.text_area(
            "Key Discussion Points",
            placeholder="Summarize the main topics discussed...",
            height=150
        )
    
    with col2:
        outcomes_decisions = st.text_area(
            "Outcomes & Decisions",
            placeholder="What decisions were made? What are the next steps?",
            height=150
        )
        
        deal_value = st.number_input(
            "Deal Value Discussed (£)",
            min_value=0,
            value=0,
            step=100000,
            format="%d"
        )
    
    # Action items section
    st.markdown("**Action Items**")
    
    # Dynamic action items
    if 'action_items' not in st.session_state:
        st.session_state.action_items = []
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_action_item = st.text_input("Add Action Item", placeholder="Describe the action item...")
    
    with col2:
        if st.button("➕ Add Action Item"):
            if new_action_item:
                st.session_state.action_items.append({
                    'item': new_action_item,
                    'assignee': '',
                    'due_date': datetime.now() + timedelta(days=7),
                    'priority': 'Medium',
                    'status': 'Open'
                })
                st.rerun()
    
    # Display action items
    if st.session_state.action_items:
        for i, item in enumerate(st.session_state.action_items):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                
                with col1:
                    st.text(item['item'])
                
                with col2:
                    assignee = st.text_input(f"Assignee {i}", value=item['assignee'], key=f"assignee_{i}")
                    st.session_state.action_items[i]['assignee'] = assignee
                
                with col3:
                    due_date = st.date_input(f"Due Date {i}", value=item['due_date'], key=f"due_{i}")
                    st.session_state.action_items[i]['due_date'] = due_date
                
                with col4:
                    priority = st.selectbox(f"Priority {i}", ['High', 'Medium', 'Low'], 
                                          index=['High', 'Medium', 'Low'].index(item['priority']), key=f"priority_{i}")
                    st.session_state.action_items[i]['priority'] = priority
                
                with col5:
                    if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state.action_items.pop(i)
                        st.rerun()
    
    # AI assistance section
    st.markdown("**🤖 AI Assistance**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 Generate AI Summary"):
            with st.spinner("Generating AI summary..."):
                # Simulate AI processing
                import time
                time.sleep(2)
                
                ai_summary = f"""
                **AI-Generated Meeting Summary:**
                
                Meeting Type: {meeting_type}
                Duration: {duration} minutes
                Platform: {platform}
                
                **Key Points:**
                • Discussed {client_name}'s business requirements and growth plans
                • Reviewed current banking relationship and identified expansion opportunities
                • Addressed concerns about interest rates and market conditions
                • Explored potential for additional credit facilities
                
                **Sentiment Analysis:** Positive (8.2/10)
                **Engagement Level:** High
                **Follow-up Required:** Yes
                """
                
                st.success("AI summary generated!")
                st.text_area("AI Summary", value=ai_summary, height=200)
    
    with col2:
        if st.button("🎯 Extract Action Items"):
            with st.spinner("Extracting action items..."):
                time.sleep(1.5)
                
                extracted_items = [
                    "Send credit proposal by Friday",
                    "Schedule follow-up meeting with CFO",
                    "Provide market analysis report",
                    "Review compliance requirements"
                ]
                
                st.success("Action items extracted!")
                for item in extracted_items:
                    st.write(f"• {item}")
    
    with col3:
        if st.button("📊 Analyze Sentiment"):
            with st.spinner("Analyzing sentiment..."):
                time.sleep(1)
                
                sentiment_results = {
                    "Overall Sentiment": "Positive",
                    "Confidence Score": "8.7/10",
                    "Client Satisfaction": "High",
                    "Engagement Level": "Very High",
                    "Risk Indicators": "None detected"
                }
                
                st.success("Sentiment analysis complete!")
                for key, value in sentiment_results.items():
                    st.write(f"**{key}:** {value}")
    
    # Save options
    st.markdown("**Save Options**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Save Draft"):
            st.success("Call report saved as draft!")
    
    with col2:
        if st.button("✅ Complete Report"):
            st.success("Call report completed and saved!")
            st.balloons()
    
    with col3:
        if st.button("📧 Email Report"):
            st.success("Call report emailed to participants!")
    
    with col4:
        if st.button("📅 Schedule Follow-up"):
            st.success("Follow-up meeting scheduled!")

with tab2:
    st.subheader("📋 Call History & Reports")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        type_filter = st.multiselect(
            "Meeting Type",
            options=calls_df['meeting_type'].unique(),
            default=calls_df['meeting_type'].unique()
        )
    
    with col2:
        rm_filter = st.multiselect(
            "Relationship Manager",
            options=calls_df['rm_name'].unique(),
            default=calls_df['rm_name'].unique()
        )
    
    with col3:
        platform_filter = st.multiselect(
            "Platform",
            options=calls_df['platform'].unique(),
            default=calls_df['platform'].unique()
        )
    
    with col4:
        date_range = st.date_input(
            "Date Range",
            value=[datetime.now().date() - timedelta(days=30), datetime.now().date()],
            max_value=datetime.now().date()
        )
    
    # Apply filters
    filtered_calls = calls_df[
        (calls_df['meeting_type'].isin(type_filter)) &
        (calls_df['rm_name'].isin(rm_filter)) &
        (calls_df['platform'].isin(platform_filter))
    ]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_calls = filtered_calls[
            (filtered_calls['date'].dt.date >= start_date) &
            (filtered_calls['date'].dt.date <= end_date)
        ]
    
    # Search functionality
    search_query = st.text_input("🔍 Search calls...", placeholder="Search by client name, content, or participants")
    
    if search_query:
        search_mask = filtered_calls['client_name'].str.contains(search_query, case=False, na=False)
        filtered_calls = filtered_calls[search_mask]
    
    # Display calls
    st.markdown(f"**Showing {len(filtered_calls)} calls**")
    
    for idx, call in filtered_calls.head(20).iterrows():
        with st.expander(f"📞 {call['meeting_type']} - {call['client_name']} ({call['date'].strftime('%Y-%m-%d')})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Date:** {call['date'].strftime('%Y-%m-%d %H:%M')}")
                st.markdown(f"**Duration:** {call['duration_minutes']} minutes")
                st.markdown(f"**Platform:** {call['platform']}")
                st.markdown(f"**RM:** {call['rm_name']}")
            
            with col2:
                st.markdown(f"**Participants:** {call['participants']}")
                st.markdown(f"**Status:** {call['status']}")
                if call['satisfaction_rating']:
                    st.markdown(f"**Satisfaction:** {call['satisfaction_rating']:.1f}/10")
                if call['deal_value_discussed'] > 0:
                    st.markdown(f"**Deal Value:** £{call['deal_value_discussed']:,.0f}")
            
            with col3:
                # Status indicators
                if call['transcript_available']:
                    st.markdown("✅ Transcript Available")
                if call['ai_summary_generated']:
                    st.markdown("🤖 AI Summary Generated")
                if call['recording_available']:
                    st.markdown("🎥 Recording Available")
                if call['action_items_count'] > 0:
                    st.markdown(f"🎯 {call['action_items_count']} Action Items")
            
            # Action buttons
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                if st.button("👁️ View", key=f"view_{call['call_id']}"):
                    st.info("Opening detailed call report...")
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_{call['call_id']}"):
                    st.info("Opening call report for editing...")
            
            with col3:
                if st.button("📄 Transcript", key=f"transcript_{call['call_id']}"):
                    if call['transcript_available']:
                        st.success("Opening transcript...")
                    else:
                        st.warning("Transcript not available")
            
            with col4:
                if st.button("🎥 Recording", key=f"recording_{call['call_id']}"):
                    if call['recording_available']:
                        st.success("Opening recording...")
                    else:
                        st.warning("Recording not available")
            
            with col5:
                if st.button("📧 Share", key=f"share_{call['call_id']}"):
                    st.success("Call report shared!")

with tab3:
    st.subheader("🎯 Action Items Management")
    
    # Generate sample action items
    @st.cache_data
    def generate_action_items():
        priorities = ['High', 'Medium', 'Low']
        statuses = ['Open', 'In Progress', 'Completed', 'Overdue']
        
        action_items = []
        for i in range(50):
            due_date = datetime.now() + timedelta(days=random.randint(-10, 30))
            status = random.choice(statuses)
            
            # Make overdue items actually overdue
            if status == 'Overdue':
                due_date = datetime.now() - timedelta(days=random.randint(1, 15))
            
            action_items.append({
                'id': f'ACTION-{4000 + i}',
                'item': f'Action item {i+1}: Follow up on client requirements and provide detailed proposal',
                'assignee': random.choice(['Sarah Johnson', 'Michael Chen', 'Emma Williams', 'David Brown', 'Lisa Davis']),
                'client': f'Client {chr(65 + i % 26)}{i % 30}',
                'priority': random.choice(priorities),
                'status': status,
                'due_date': due_date,
                'created_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'call_id': f'CALL-{3000 + random.randint(0, 149)}',
                'estimated_hours': random.randint(1, 8),
                'completion_percentage': random.randint(0, 100) if status in ['In Progress', 'Completed'] else 0
            })
        
        return pd.DataFrame(action_items)
    
    action_items_df = generate_action_items()
    
    # Action items overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_actions = len(action_items_df)
        open_actions = len(action_items_df[action_items_df['status'] == 'Open'])
        st.metric(
            label="📋 Total Actions",
            value=total_actions,
            delta=f"{open_actions} open"
        )
    
    with col2:
        overdue_actions = len(action_items_df[action_items_df['status'] == 'Overdue'])
        st.metric(
            label="⚠️ Overdue",
            value=overdue_actions,
            delta="Needs attention"
        )
    
    with col3:
        completed_actions = len(action_items_df[action_items_df['status'] == 'Completed'])
        completion_rate = (completed_actions / total_actions) * 100
        st.metric(
            label="✅ Completed",
            value=completed_actions,
            delta=f"{completion_rate:.1f}% rate"
        )
    
    with col4:
        avg_completion_time = 5.2  # days
        st.metric(
            label="⏱️ Avg Completion",
            value=f"{avg_completion_time:.1f} days",
            delta="↓ 0.8 days"
        )
    
    # Action items filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            options=action_items_df['status'].unique(),
            default=['Open', 'In Progress', 'Overdue']
        )
    
    with col2:
        priority_filter = st.multiselect(
            "Priority",
            options=action_items_df['priority'].unique(),
            default=action_items_df['priority'].unique()
        )
    
    with col3:
        assignee_filter = st.multiselect(
            "Assignee",
            options=action_items_df['assignee'].unique(),
            default=action_items_df['assignee'].unique()
        )
    
    with col4:
        due_filter = st.selectbox(
            "Due Date",
            options=["All", "Today", "This Week", "Next Week", "Overdue"]
        )
    
    # Apply filters
    filtered_actions = action_items_df[
        (action_items_df['status'].isin(status_filter)) &
        (action_items_df['priority'].isin(priority_filter)) &
        (action_items_df['assignee'].isin(assignee_filter))
    ]
    
    # Apply due date filter
    if due_filter == "Today":
        filtered_actions = filtered_actions[filtered_actions['due_date'].dt.date == datetime.now().date()]
    elif due_filter == "This Week":
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        week_end = week_start + timedelta(days=6)
        filtered_actions = filtered_actions[
            (filtered_actions['due_date'] >= week_start) &
            (filtered_actions['due_date'] <= week_end)
        ]
    elif due_filter == "Next Week":
        next_week_start = datetime.now() + timedelta(days=7-datetime.now().weekday())
        next_week_end = next_week_start + timedelta(days=6)
        filtered_actions = filtered_actions[
            (filtered_actions['due_date'] >= next_week_start) &
            (filtered_actions['due_date'] <= next_week_end)
        ]
    elif due_filter == "Overdue":
        filtered_actions = filtered_actions[filtered_actions['status'] == 'Overdue']
    
    # Action items table
    st.markdown(f"**Showing {len(filtered_actions)} action items**")
    
    # Prepare display dataframe
    display_actions = filtered_actions.copy()
    display_actions['Days Until Due'] = (display_actions['due_date'] - datetime.now()).dt.days
    
    # Status indicators
    def get_status_indicator(row):
        if row['status'] == 'Completed':
            return '✅ Completed'
        elif row['status'] == 'Overdue':
            return '🚨 Overdue'
        elif row['status'] == 'In Progress':
            return '🔄 In Progress'
        else:
            return '📋 Open'
    
    display_actions['Status Icon'] = display_actions.apply(get_status_indicator, axis=1)
    
    # Priority indicators
    def get_priority_indicator(priority):
        if priority == 'High':
            return '🔴 High'
        elif priority == 'Medium':
            return '🟡 Medium'
        else:
            return '🟢 Low'
    
    display_actions['Priority Icon'] = display_actions['priority'].apply(get_priority_indicator)
    
    # Select columns for display
    action_columns = [
        'item', 'assignee', 'client', 'Priority Icon', 'Status Icon',
        'due_date', 'Days Until Due', 'completion_percentage'
    ]
    
    st.dataframe(
        display_actions[action_columns],
        use_container_width=True,
        column_config={
            "item": "Action Item",
            "assignee": "Assignee",
            "client": "Client",
            "Priority Icon": "Priority",
            "Status Icon": "Status",
            "due_date": "Due Date",
            "Days Until Due": "Days Until Due",
            "completion_percentage": st.column_config.ProgressColumn(
                "Progress",
                min_value=0,
                max_value=100,
                format="%d%%"
            )
        }
    )
    
    # Action items analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Action items by status
        status_counts = filtered_actions['status'].value_counts()
        
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Action Items by Status",
            color_discrete_map={
                'Open': '#6c757d',
                'In Progress': '#007bff',
                'Completed': '#28a745',
                'Overdue': '#dc3545'
            }
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Action items by assignee
        assignee_counts = filtered_actions['assignee'].value_counts()
        
        fig_assignee = px.bar(
            x=assignee_counts.values,
            y=assignee_counts.index,
            orientation='h',
            title="Action Items by Assignee"
        )
        st.plotly_chart(fig_assignee, use_container_width=True)
    
    # SLA adherence tracking
    st.markdown("**📊 SLA Adherence & Performance**")
    
    # Calculate SLA metrics
    sla_metrics = {
        'High Priority SLA': '24 hours',
        'Medium Priority SLA': '72 hours',
        'Low Priority SLA': '7 days',
        'Overall SLA Adherence': '87.3%',
        'Average Response Time': '4.2 hours',
        'Average Completion Time': '5.2 days'
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        for i, (metric, value) in enumerate(list(sla_metrics.items())[:2]):
            st.metric(label=metric, value=value)
    
    with col2:
        for i, (metric, value) in enumerate(list(sla_metrics.items())[2:4]):
            st.metric(label=metric, value=value)
    
    with col3:
        for i, (metric, value) in enumerate(list(sla_metrics.items())[4:]):
            st.metric(label=metric, value=value)

with tab4:
    st.subheader("📊 Call & Meeting Analytics")
    
    # Analytics overview
    col1, col2 = st.columns(2)
    
    with col1:
        # Calls by type
        type_counts = calls_df['meeting_type'].value_counts()
        
        fig_types = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="Calls by Type"
        )
        st.plotly_chart(fig_types, use_container_width=True)
    
    with col2:
        # Platform usage
        platform_counts = calls_df['platform'].value_counts()
        
        fig_platforms = px.bar(
            x=platform_counts.index,
            y=platform_counts.values,
            title="Platform Usage"
        )
        st.plotly_chart(fig_platforms, use_container_width=True)
    
    # Time-based analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily call volume
        daily_calls = calls_df.groupby(calls_df['date'].dt.date).size().reset_index(name='call_count')
        daily_calls = daily_calls.tail(30)  # Last 30 days
        
        fig_daily = px.line(
            daily_calls,
            x='date',
            y='call_count',
            title="Daily Call Volume (Last 30 Days)"
        )
        st.plotly_chart(fig_daily, use_container_width=True)
    
    with col2:
        # Average duration by type
        avg_duration = calls_df.groupby('meeting_type')['duration_minutes'].mean().reset_index()
        
        fig_duration = px.bar(
            avg_duration,
            x='meeting_type',
            y='duration_minutes',
            title="Average Duration by Meeting Type"
        )
        st.plotly_chart(fig_duration, use_container_width=True)
    
    # Performance metrics
    st.markdown("**Performance Metrics**")
    
    performance_data = calls_df.groupby('rm_name').agg({
        'call_id': 'count',
        'duration_minutes': 'sum',
        'action_items_count': 'sum',
        'satisfaction_rating': 'mean',
        'deal_value_discussed': 'sum'
    }).round(2)
    
    performance_data.columns = ['Total Calls', 'Total Duration (min)', 'Action Items', 'Avg Satisfaction', 'Total Deal Value']
    performance_data['Total Deal Value'] = performance_data['Total Deal Value'] / 1000000  # Convert to millions
    
    st.dataframe(performance_data, use_container_width=True)

with tab5:
    st.subheader("⚙️ Integration Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Platform Integrations**")
        
        # MS Teams integration
        teams_connected = st.checkbox("🔗 Microsoft Teams", value=True)
        if teams_connected:
            st.success("✅ Connected to MS Teams")
            teams_auto_import = st.checkbox("Auto-import meeting details", value=True)
            teams_transcript = st.checkbox("Auto-generate transcripts", value=True)
            teams_recording = st.checkbox("Auto-save recordings", value=False)
        
        # Zoom integration
        zoom_connected = st.checkbox("🔗 Zoom", value=True)
        if zoom_connected:
            st.success("✅ Connected to Zoom")
            zoom_auto_import = st.checkbox("Auto-import meeting details", value=True, key="zoom_import")
            zoom_transcript = st.checkbox("Auto-generate transcripts", value=True, key="zoom_transcript")
            zoom_recording = st.checkbox("Auto-save recordings", value=False, key="zoom_recording")
        
        # Other platforms
        google_meet = st.checkbox("🔗 Google Meet", value=False)
        webex = st.checkbox("🔗 Cisco Webex", value=False)
    
    with col2:
        st.markdown("**AI & Automation Settings**")
        
        # AI settings
        ai_summary = st.checkbox("🤖 Auto-generate AI summaries", value=True)
        ai_action_items = st.checkbox("🎯 Auto-extract action items", value=True)
        ai_sentiment = st.checkbox("😊 Sentiment analysis", value=True)
        ai_follow_up = st.checkbox("📅 Suggest follow-up actions", value=True)
        
        # Notification settings
        st.markdown("**Notification Settings**")
        
        email_notifications = st.checkbox("📧 Email notifications", value=True)
        slack_notifications = st.checkbox("💬 Slack notifications", value=False)
        mobile_notifications = st.checkbox("📱 Mobile push notifications", value=True)
        
        # SLA settings
        st.markdown("**SLA Configuration**")
        
        high_priority_sla = st.number_input("High Priority SLA (hours)", min_value=1, max_value=72, value=24)
        medium_priority_sla = st.number_input("Medium Priority SLA (hours)", min_value=1, max_value=168, value=72)
        low_priority_sla = st.number_input("Low Priority SLA (days)", min_value=1, max_value=30, value=7)
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")

# Recent activities
st.subheader("📋 Recent Call Activities")

recent_activities = [
    {"time": "10 min ago", "icon": "📞", "message": "Client call completed with TechCorp - 45 minutes", "user": "Sarah Johnson"},
    {"time": "1 hour ago", "icon": "🤖", "message": "AI summary generated for Manufacturing Inc meeting", "user": "System"},
    {"time": "2 hours ago", "icon": "🎯", "message": "3 action items created from Healthcare Plus call", "user": "Michael Chen"},
    {"time": "3 hours ago", "icon": "📄", "message": "Transcript processed for RetailChain prospect call", "user": "System"},
    {"time": "4 hours ago", "icon": "📅", "message": "Follow-up meeting scheduled with EnergyPlus", "user": "Emma Williams"},
    {"time": "5 hours ago", "icon": "✅", "message": "Action item completed: Send proposal to StartupXYZ", "user": "David Brown"},
    {"time": "6 hours ago", "icon": "🚨", "message": "SLA breach alert: High priority action overdue", "user": "System"},
    {"time": "1 day ago", "icon": "📊", "message": "Weekly call report generated - 47 calls completed", "user": "System"}
]

for activity in recent_activities:
    col1, col2, col3 = st.columns([1, 8, 2])
    
    with col1:
        st.markdown(f"<div style='font-size: 1.5em; text-align: center;'>{activity['icon']}</div>", 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**{activity['time']}** - {activity['message']}")
    
    with col3:
        st.markdown(f"*{activity['user']}*")

