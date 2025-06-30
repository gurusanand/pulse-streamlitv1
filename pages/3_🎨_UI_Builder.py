import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(
    page_title="UI Builder",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 UI Builder")
st.markdown("Drag-and-drop page builder for custom layouts")

# Initialize session state for UI builder
if 'canvas_widgets' not in st.session_state:
    st.session_state.canvas_widgets = []

if 'selected_template' not in st.session_state:
    st.session_state.selected_template = None

# UI Builder tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🧩 Widget Library", 
    "📐 Canvas", 
    "⚙️ Properties", 
    "💾 Templates"
])

with tab1:
    st.header("🧩 Widget Library")
    st.markdown("Drag widgets to the canvas to build your custom page")
    
    # Widget categories
    widget_categories = {
        "📊 Analytics Widgets": {
            "KPI Card": {
                "description": "Display key performance indicators",
                "icon": "📈",
                "properties": ["title", "value", "delta", "color"]
            },
            "Line Chart": {
                "description": "Time series data visualization", 
                "icon": "📉",
                "properties": ["data_source", "x_axis", "y_axis", "color"]
            },
            "Bar Chart": {
                "description": "Categorical data comparison",
                "icon": "📊", 
                "properties": ["data_source", "x_axis", "y_axis", "orientation"]
            },
            "Pie Chart": {
                "description": "Proportional data display",
                "icon": "🥧",
                "properties": ["data_source", "values", "labels", "colors"]
            },
            "Gauge Chart": {
                "description": "Progress and performance gauge",
                "icon": "⏲️",
                "properties": ["value", "min_value", "max_value", "thresholds"]
            }
        },
        "💼 Business Widgets": {
            "Client Card": {
                "description": "Client information display",
                "icon": "👤",
                "properties": ["client_name", "industry", "revenue", "risk_score"]
            },
            "Deal Card": {
                "description": "Deal summary and status",
                "icon": "💰",
                "properties": ["deal_name", "value", "stage", "probability"]
            },
            "News Feed": {
                "description": "Latest news and updates",
                "icon": "📰",
                "properties": ["source", "category", "count", "refresh_rate"]
            },
            "Risk Indicator": {
                "description": "Risk level display",
                "icon": "⚠️",
                "properties": ["risk_level", "threshold", "color_scheme", "alerts"]
            },
            "Activity Timeline": {
                "description": "Recent activities and events",
                "icon": "📅",
                "properties": ["time_range", "event_types", "user_filter", "limit"]
            }
        },
        "📋 Data Widgets": {
            "Data Table": {
                "description": "Tabular data display",
                "icon": "📋",
                "properties": ["data_source", "columns", "pagination", "sorting"]
            },
            "Search Box": {
                "description": "Data search and filtering",
                "icon": "🔍",
                "properties": ["placeholder", "search_fields", "filters", "suggestions"]
            },
            "Filter Panel": {
                "description": "Advanced filtering controls",
                "icon": "🎛️",
                "properties": ["filter_fields", "date_range", "categories", "operators"]
            },
            "Export Button": {
                "description": "Data export functionality",
                "icon": "📤",
                "properties": ["export_formats", "data_scope", "filename", "permissions"]
            }
        },
        "🎛️ Control Widgets": {
            "Action Button": {
                "description": "Interactive button",
                "icon": "🔘",
                "properties": ["label", "action", "style", "permissions"]
            },
            "Form Input": {
                "description": "Data input field",
                "icon": "📝",
                "properties": ["input_type", "label", "validation", "placeholder"]
            },
            "Dropdown": {
                "description": "Selection dropdown",
                "icon": "📋",
                "properties": ["options", "default_value", "multiple", "searchable"]
            },
            "Toggle Switch": {
                "description": "Boolean control",
                "icon": "🔄",
                "properties": ["label", "default_state", "action", "style"]
            },
            "Date Picker": {
                "description": "Date selection control",
                "icon": "📅",
                "properties": ["date_format", "range_mode", "min_date", "max_date"]
            }
        }
    }
    
    # Display widget categories
    for category, widgets in widget_categories.items():
        with st.expander(category, expanded=True):
            for widget_name, widget_info in widgets.items():
                col1, col2, col3 = st.columns([1, 4, 1])
                
                with col1:
                    st.markdown(f"<div style='font-size: 2em; text-align: center;'>{widget_info['icon']}</div>", 
                              unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{widget_name}**")
                    st.markdown(f"*{widget_info['description']}*")
                    st.markdown(f"Properties: {', '.join(widget_info['properties'])}")
                
                with col3:
                    if st.button("➕", key=f"add_{widget_name}", help=f"Add {widget_name} to canvas"):
                        # Add widget to canvas
                        new_widget = {
                            "id": f"widget_{len(st.session_state.canvas_widgets) + 1}",
                            "type": widget_name,
                            "category": category,
                            "icon": widget_info['icon'],
                            "properties": {prop: f"Default {prop}" for prop in widget_info['properties']},
                            "position": {"x": 0, "y": len(st.session_state.canvas_widgets) * 100},
                            "size": {"width": 300, "height": 200}
                        }
                        st.session_state.canvas_widgets.append(new_widget)
                        st.success(f"✅ Added {widget_name} to canvas!")
                        st.rerun()

with tab2:
    st.header("📐 Canvas")
    st.markdown("Your custom page layout")
    
    if not st.session_state.canvas_widgets:
        st.info("👈 Add widgets from the Widget Library to start building your page")
        
        # Show empty canvas placeholder
        st.markdown("""
        <div style="
            border: 2px dashed #ccc; 
            height: 400px; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            background-color: #f9f9f9;
            border-radius: 10px;
            margin: 20px 0;
        ">
            <div style="text-align: center; color: #666;">
                <h3>📐 Empty Canvas</h3>
                <p>Drag widgets here to build your custom page</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display canvas with widgets
        st.markdown("### 🎨 Page Preview")
        
        # Canvas controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🗑️ Clear Canvas"):
                st.session_state.canvas_widgets = []
                st.rerun()
        
        with col2:
            if st.button("↩️ Undo Last"):
                if st.session_state.canvas_widgets:
                    st.session_state.canvas_widgets.pop()
                    st.rerun()
        
        with col3:
            grid_mode = st.checkbox("📏 Show Grid", value=True)
        
        with col4:
            preview_mode = st.selectbox("👁️ Preview", ["Desktop", "Tablet", "Mobile"])
        
        # Render widgets on canvas
        for i, widget in enumerate(st.session_state.canvas_widgets):
            with st.container():
                # Widget header with controls
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{widget['icon']} {widget['type']}** (ID: {widget['id']})")
                
                with col2:
                    if st.button("⚙️", key=f"config_{widget['id']}", help="Configure widget"):
                        st.session_state.selected_widget = widget['id']
                
                with col3:
                    if st.button("📋", key=f"copy_{widget['id']}", help="Copy widget"):
                        copied_widget = widget.copy()
                        copied_widget['id'] = f"widget_{len(st.session_state.canvas_widgets) + 1}"
                        st.session_state.canvas_widgets.append(copied_widget)
                        st.rerun()
                
                with col4:
                    if st.button("🗑️", key=f"delete_{widget['id']}", help="Delete widget"):
                        st.session_state.canvas_widgets = [w for w in st.session_state.canvas_widgets if w['id'] != widget['id']]
                        st.rerun()
                
                # Widget preview based on type
                if widget['type'] == "KPI Card":
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(
                            label=widget['properties'].get('title', 'KPI Title'),
                            value=widget['properties'].get('value', '123'),
                            delta=widget['properties'].get('delta', '12%')
                        )
                
                elif widget['type'] == "Line Chart":
                    # Sample chart data
                    import plotly.express as px
                    import pandas as pd
                    import numpy as np
                    
                    sample_data = pd.DataFrame({
                        'x': range(10),
                        'y': np.random.randint(10, 100, 10)
                    })
                    fig = px.line(sample_data, x='x', y='y', title=widget['properties'].get('title', 'Sample Chart'))
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{widget['id']}")
                
                elif widget['type'] == "Data Table":
                    # Sample table data
                    sample_df = pd.DataFrame({
                        'Column 1': ['Value 1', 'Value 2', 'Value 3'],
                        'Column 2': [100, 200, 300],
                        'Column 3': ['A', 'B', 'C']
                    })
                    st.dataframe(sample_df, use_container_width=True, key=f"table_{widget['id']}")
                
                elif widget['type'] == "Client Card":
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; background: white;">
                        <h4>🏢 {widget['properties'].get('client_name', 'Sample Client')}</h4>
                        <p><strong>Industry:</strong> {widget['properties'].get('industry', 'Technology')}</p>
                        <p><strong>Revenue:</strong> £{widget['properties'].get('revenue', '5.2M')}</p>
                        <p><strong>Risk Score:</strong> {widget['properties'].get('risk_score', '7.5/10')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                else:
                    # Generic widget preview
                    st.markdown(f"""
                    <div style="border: 2px dashed #3b82f6; padding: 20px; border-radius: 8px; text-align: center; background: #f0f9ff;">
                        <h3>{widget['icon']} {widget['type']}</h3>
                        <p>Widget preview would appear here</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")

with tab3:
    st.header("⚙️ Widget Properties")
    
    if 'selected_widget' not in st.session_state:
        st.info("👈 Select a widget from the canvas to configure its properties")
    else:
        # Find selected widget
        selected_widget = None
        for widget in st.session_state.canvas_widgets:
            if widget['id'] == st.session_state.selected_widget:
                selected_widget = widget
                break
        
        if selected_widget:
            st.markdown(f"### Configuring: {selected_widget['icon']} {selected_widget['type']}")
            
            # Widget properties form
            with st.form(f"properties_{selected_widget['id']}"):
                st.subheader("📝 Widget Properties")
                
                # Dynamic property inputs based on widget type
                for prop_name, prop_value in selected_widget['properties'].items():
                    if prop_name in ['title', 'label', 'client_name', 'deal_name']:
                        new_value = st.text_input(prop_name.replace('_', ' ').title(), value=str(prop_value))
                    elif prop_name in ['value', 'revenue', 'risk_score']:
                        new_value = st.text_input(prop_name.replace('_', ' ').title(), value=str(prop_value))
                    elif prop_name in ['color', 'color_scheme']:
                        new_value = st.selectbox(
                            prop_name.replace('_', ' ').title(),
                            ['Blue', 'Green', 'Red', 'Purple', 'Orange'],
                            index=0
                        )
                    elif prop_name == 'data_source':
                        new_value = st.selectbox(
                            "Data Source",
                            ['Clients', 'Deals', 'Performance', 'Risk Metrics', 'Market Data'],
                            index=0
                        )
                    else:
                        new_value = st.text_input(prop_name.replace('_', ' ').title(), value=str(prop_value))
                    
                    selected_widget['properties'][prop_name] = new_value
                
                st.subheader("📐 Layout Properties")
                
                col1, col2 = st.columns(2)
                with col1:
                    width = st.number_input("Width (px)", value=selected_widget['size']['width'], min_value=100, max_value=1200)
                    x_position = st.number_input("X Position", value=selected_widget['position']['x'], min_value=0)
                
                with col2:
                    height = st.number_input("Height (px)", value=selected_widget['size']['height'], min_value=100, max_value=800)
                    y_position = st.number_input("Y Position", value=selected_widget['position']['y'], min_value=0)
                
                selected_widget['size']['width'] = width
                selected_widget['size']['height'] = height
                selected_widget['position']['x'] = x_position
                selected_widget['position']['y'] = y_position
                
                st.subheader("🎨 Style Properties")
                
                border_style = st.selectbox("Border Style", ["None", "Solid", "Dashed", "Dotted"])
                background_color = st.color_picker("Background Color", "#FFFFFF")
                text_color = st.color_picker("Text Color", "#000000")
                
                if st.form_submit_button("💾 Apply Changes"):
                    st.success("✅ Widget properties updated!")
                    st.rerun()

with tab4:
    st.header("💾 Page Templates")
    
    # Template management
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Available Templates")
        
        templates = {
            "Executive Dashboard": {
                "description": "KPIs, charts, and executive metrics",
                "widgets": ["KPI Card", "Line Chart", "Pie Chart", "Activity Timeline"],
                "preview": "📊📈📋📅"
            },
            "Client Overview": {
                "description": "Client-focused layout with relationship data",
                "widgets": ["Client Card", "Deal Card", "Risk Indicator", "Data Table"],
                "preview": "👤💰⚠️📋"
            },
            "Analytics Hub": {
                "description": "Data-heavy analytical dashboard",
                "widgets": ["Bar Chart", "Line Chart", "Gauge Chart", "Filter Panel"],
                "preview": "📊📈⏲️🎛️"
            },
            "Risk Dashboard": {
                "description": "Risk monitoring and compliance",
                "widgets": ["Risk Indicator", "Gauge Chart", "Data Table", "News Feed"],
                "preview": "⚠️⏲️📋📰"
            },
            "Deal Pipeline": {
                "description": "Sales pipeline and opportunity tracking",
                "widgets": ["Deal Card", "Bar Chart", "Search Box", "Export Button"],
                "preview": "💰📊🔍📤"
            }
        }
        
        for template_name, template_info in templates.items():
            with st.expander(f"{template_info['preview']} {template_name}"):
                st.markdown(f"**Description:** {template_info['description']}")
                st.markdown(f"**Widgets:** {', '.join(template_info['widgets'])}")
                
                col_preview, col_apply = st.columns([3, 1])
                with col_apply:
                    if st.button("Apply", key=f"apply_{template_name}"):
                        # Clear current canvas and apply template
                        st.session_state.canvas_widgets = []
                        
                        # Add template widgets
                        for i, widget_type in enumerate(template_info['widgets']):
                            # Find widget info from categories
                            widget_info = None
                            for category, widgets in widget_categories.items():
                                if widget_type in widgets:
                                    widget_info = widgets[widget_type]
                                    break
                            
                            if widget_info:
                                new_widget = {
                                    "id": f"template_widget_{i+1}",
                                    "type": widget_type,
                                    "category": category,
                                    "icon": widget_info['icon'],
                                    "properties": {prop: f"Template {prop}" for prop in widget_info['properties']},
                                    "position": {"x": (i % 2) * 350, "y": (i // 2) * 250},
                                    "size": {"width": 300, "height": 200}
                                }
                                st.session_state.canvas_widgets.append(new_widget)
                        
                        st.session_state.selected_template = template_name
                        st.success(f"✅ Applied template: {template_name}")
                        st.rerun()
    
    with col2:
        st.subheader("💾 Save Custom Template")
        
        if st.session_state.canvas_widgets:
            template_name = st.text_input("Template Name", placeholder="My Custom Dashboard")
            template_description = st.text_area("Description", placeholder="Describe your template...")
            
            if st.button("💾 Save Template"):
                if template_name:
                    # Save template logic would go here
                    st.success(f"✅ Template '{template_name}' saved successfully!")
                else:
                    st.error("Please enter a template name")
        else:
            st.info("Add widgets to the canvas before saving a template")
        
        st.subheader("📤 Export/Import")
        
        if st.session_state.canvas_widgets:
            # Export current layout
            layout_json = json.dumps(st.session_state.canvas_widgets, indent=2)
            
            st.download_button(
                label="📤 Export Layout",
                data=layout_json,
                file_name=f"pulse_layout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Import layout
        uploaded_file = st.file_uploader("📥 Import Layout", type=['json'])
        if uploaded_file:
            try:
                imported_layout = json.load(uploaded_file)
                if st.button("Apply Imported Layout"):
                    st.session_state.canvas_widgets = imported_layout
                    st.success("✅ Layout imported successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error importing layout: {str(e)}")

# Footer with canvas summary
if st.session_state.canvas_widgets:
    st.markdown("---")
    st.markdown(f"**Canvas Summary:** {len(st.session_state.canvas_widgets)} widgets | "
                f"Template: {st.session_state.selected_template or 'Custom'}")

