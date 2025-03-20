import streamlit as st
import os
import openai
import datetime
import plotly.express as px
import pandas as pd
import random

# Define eco-driving tips
eco_tips = [
    {
        "title": "Maintain Steady Speed",
        "content": "Use cruise control on highways to maintain a steady speed. Constant speed changes reduce fuel efficiency by up to 20%.",
        "icon": "🚘",
        "bg_image": "https://images.unsplash.com/photo-1541348263662-e068662d82af?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3"
    },
    {
        "title": "Avoid Rapid Acceleration",
        "content": "Gentle acceleration can significantly improve fuel economy. Try to accelerate smoothly and gradually when possible.",
        "icon": "🏎️",
        "bg_image": "https://images.unsplash.com/photo-1504215680853-026ed2a45def?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3"
    },
    {
        "title": "Proper Tire Inflation",
        "content": "Keep your tires properly inflated. Under-inflated tires can decrease gas mileage by about 0.2% for every 1 PSI drop.",
        "icon": "🛞",
        "bg_image": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3"
    },
    {
        "title": "Reduce Idling Time",
        "content": "Turn off your engine when stopped for more than 60 seconds. Excessive idling wastes fuel and increases emissions unnecessarily.",
        "icon": "⏱️",
        "bg_image": "https://images.unsplash.com/photo-1493238792000-8113da705763?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3"
    },
    {
        "title": "Plan Efficient Routes",
        "content": "Combine errands into one trip and plan the most efficient route. This reduces total distance traveled and avoids cold starts.",
        "icon": "🗺️",
        "bg_image": "https://images.unsplash.com/photo-1551312838-3010d9a4d937?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3"
    },
    {
        "title": "Remove Excess Weight",
        "content": "Clear out unnecessary items from your vehicle. Every extra 100 pounds can reduce fuel economy by about 1%.",
        "icon": "⚖️",
        "bg_image": "https://images.unsplash.com/photo-1581278759334-9c37c44c745b?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3"
    }
]

# Check if the API key is available
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    # For demo purposes only - don't hardcode API keys in production
    # You can use a placeholder for the demo or handle it differently
    api_key = "Your API key here"  # Replace with your actual API key for testing

# Initialize OpenAI client
openai.api_key = api_key

# Configure the page with custom theme settings
st.set_page_config(
    page_title="Eco-Driving Assistant",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.ecodrivecompanion.com/help',
        'Report a bug': 'https://www.ecodrivecompanion.com/bug',
        'About': 'Eco-Drive Companion helps you drive more efficiently and reduce your carbon footprint.'
    }
)

# Custom CSS for better UI with simplified styles
st.markdown("""
<style>
    /* Base theme colors - simplified */
    :root {
        --primary-dark: #1B5E20;
        --primary-main: #2E7D32;
        --primary-light: #4CAF50;
        --background-dark: #1E1E1E;
        --background-light: #263238;
        --text-light: #ECEFF1;
        --text-dark: #B0BEC5;
    }
    
    /* Simple background - better performance */
    .stApp {
        background-color: var(--background-dark);
        background-image: url('https://images.unsplash.com/photo-1557692538-9564c4b2cd33?auto=format&fit=crop&q=60&w=500&ixlib=rb-4.0.3');
        background-size: 400px;
        background-repeat: repeat;
        background-position: center;
        background-blend-mode: soft-light;
        background-opacity: 0.1;
    }
    
    /* Fix for Streamlit elements to ensure proper rendering */
    .stMarkdown, .stButton, .stSelectbox, .stRadio, .stMetric {
        position: relative;
        z-index: 5;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        color: var(--primary-light);
        margin-bottom: 0;
        position: relative;
        z-index: 5;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: var(--text-dark);
        font-style: italic;
        margin-bottom: 2rem;
        position: relative;
        z-index: 5;
    }
    
    /* Card styling */
    .metric-card {
        background-color: var(--background-light);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        border-left: 4px solid var(--primary-light);
        color: var(--text-light);
        position: relative;
        overflow: hidden;
        transition: transform 0.3s, box-shadow 0.3s;
        background-image: url('https://images.unsplash.com/photo-1523961131990-5ea7c61b2107?auto=format&fit=crop&q=60&w=200&ixlib=rb-4.0.3');
        background-size: 100px;
        background-position: right bottom;
        background-repeat: no-repeat;
        background-blend-mode: soft-light;
        background-opacity: 0.15;
        margin-bottom: 0.5rem;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    /* Section headers */
    .section-header {
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
        color: var(--primary-light);
        border-bottom: 1px solid var(--primary-light);
        padding-bottom: 8px;
    }
    
    /* Dynamic header with clean eco-driving themed image */
    .dynamic-header {
        background: linear-gradient(90deg, rgba(27,94,32,0.75) 0%, rgba(46,125,50,0.75) 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        color: white;
        position: relative;
        z-index: 1;
        background-image: url('https://images.unsplash.com/photo-1605618325400-327c61f1d455?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3');
        background-size: cover;
        background-position: center;
        background-blend-mode: overlay;
        overflow: hidden;
    }
    
    /* Welcome card with sleek car image */
    .welcome-card-container {
        background-color: var(--background-light);
        padding: 30px 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        color: var(--text-light);
        position: relative;
        z-index: 1;
        background-image: url('https://images.unsplash.com/photo-1610647752706-3bb12232b3ab?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3');
        background-size: cover;
        background-position: center;
        background-blend-mode: overlay;
        background-color: rgba(24, 30, 36, 0.75);
        border-left: 5px solid #9CCC65;
        overflow: hidden;
    }
    
    .welcome-content {
        position: relative;
        z-index: 2;
        padding: 20px;
        background-color: rgba(0,0,0,0.6);
        border-radius: 10px;
        margin: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .welcome-heading {
        margin-top: 0;
        color: #9CCC65;
        font-size: 1.9rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.7);
        position: relative;
        z-index: 3;
    }
    
    .welcome-text {
        font-size: 1.05rem;
        text-shadow: 0 1px 3px rgba(0,0,0,0.6);
        max-width: 80%;
        color: #E0E0E0;
        position: relative;
        z-index: 3;
    }
    
    .eco-score-container {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        padding: 8px 18px;
        position: relative;
        z-index: 3;
        background-color: rgba(27, 94, 32, 0.9);
        border-radius: 20px;
    }
    
    /* Tip card with eco-driving themed image */
    .tip-card {
        background-color: var(--background-light);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid var(--primary-light);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: var(--text-light);
        position: relative;
        overflow: hidden;
        z-index: 1;
        background-image: url('https://images.unsplash.com/photo-1566935534912-68d2fff4a673?auto=format&fit=crop&q=80&w=500&ixlib=rb-4.0.3');
        background-size: cover;
        background-position: center;
        background-blend-mode: soft-light;
        background-color: rgba(38, 50, 56, 0.9);
        transition: transform 0.3s;
    }
    
    .tip-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    /* Activity card styling */
    .activity-card {
        background-color: var(--background-light);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        transition: transform 0.2s, box-shadow 0.2s;
        border-left: 4px solid var(--primary-light);
    }
    
    .activity-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .activity-icon {
        font-size: 28px;
        margin-right: 15px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .activity-content {
        flex-grow: 1;
    }
    
    .activity-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .activity-title {
        font-weight: bold;
        color: var(--text-light);
        font-size: 1.1rem;
    }
    
    .activity-date {
        color: var(--text-dark);
        font-size: 0.9rem;
        background-color: rgba(0,0,0,0.2);
        padding: 3px 10px;
        border-radius: 12px;
    }
    
    .activity-details {
        color: var(--text-dark);
        margin-top: 6px;
    }
    
    .activity-tag {
        font-size: 0.8rem;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        margin-top: 8px;
    }
    
    .activity-tag-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: white;
        margin-right: 5px;
    }
    
    /* Score badge */
    .eco-score-badge {
        display: inline-flex;
        align-items: center;
        padding: 5px 15px;
        background-color: var(--primary-dark);
        color: white;
        border-radius: 20px;
        font-weight: bold;
        margin-top: 10px;
    }
    
    /* Streamlit element overrides */
    [data-testid="stMetricValue"] {
        font-weight: bold;
        color: var(--text-light);
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-dark);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for user profile and app settings
with st.sidebar:
    # Dynamic user avatar with initials instead of static image
    user_name = st.text_input("Name", value="John Doe")
    initials = "".join([name[0] for name in user_name.split() if name])
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="background-color: #4CAF50; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; margin-right: 15px;">
            {initials}
        </div>
        <div>
            <div style="font-weight: bold; color: #ECEFF1;">{user_name}</div>
            <div style="color: #B0BEC5;">Eco Driver</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    vehicle_model = st.text_input("Vehicle", value="Toyota Prius")
    
    # Display a dynamic vehicle icon based on the model name
    vehicle_icon = "🚗"
    if "suv" in vehicle_model.lower() or "truck" in vehicle_model.lower():
        vehicle_icon = "🚙"
    elif "electric" in vehicle_model.lower() or "ev" in vehicle_model.lower() or "tesla" in vehicle_model.lower():
        vehicle_icon = "🔋"
    elif "hybrid" in vehicle_model.lower() or "prius" in vehicle_model.lower():
        vehicle_icon = "♻️"
    
    st.markdown(f"""
    <div style="background-color: #263238; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 24px; margin-right: 10px;">{vehicle_icon}</div>
            <div>
                <div style="font-weight: bold; color: #ECEFF1;">{vehicle_model}</div>
                <div style="color: #B0BEC5;">Your vehicle</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### App Settings")
    theme = st.selectbox("Theme", ["Dark Green", "Dark Blue", "Dark Purple"])
    unit_system = st.radio("Unit System", ["Metric (km, L)", "Imperial (mi, gal)"])
    
    st.markdown("---")
    
    # Quick navigation with advanced styling
    st.markdown("### Quick Navigation")
    
    # Create navigation buttons with icons and hover effects
    st.markdown("""
    <style>
    .nav-button {
        background-color: #263238;
        border: none;
        color: #ECEFF1;
        padding: 12px 16px;
        text-align: left;
        text-decoration: none;
        display: flex;
        align-items: center;
        margin: 8px 0;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        width: 100%;
    }
    
    .nav-button:hover {
        background-color: #1B5E20;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    .nav-icon {
        font-size: 20px;
        margin-right: 10px;
        width: 24px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Driving Analysis", use_container_width=True):
        st.switch_page("pages/1_driving_analysis.py")
    if st.button("🔧 Vehicle Maintenance", use_container_width=True):
        st.switch_page("pages/2_maintenance.py")
    if st.button("🌱 Carbon Footprint", use_container_width=True):
        st.switch_page("pages/3_carbon_footprint.py")

# Main content area
st.markdown("<h1 class='main-header'>🚗 Eco-Driving Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your personal companion for sustainable driving</p>", unsafe_allow_html=True)

# Welcome card - simplified
current_date = datetime.datetime.now().strftime("%B %d, %Y")
current_hour = datetime.datetime.now().hour
if current_hour < 12:
    greeting = "Good morning"
elif current_hour < 17:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

# Dynamic header with clean design and eco-friendly car image
st.markdown("""
<div class="dynamic-header">
    <div style="position: relative; z-index: 2; padding: 25px; background-color: rgba(0,0,0,0.4); border-radius: 10px; margin: 5px;">
        <h2 style="margin-top: 0; font-size: 2.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.6); position: relative; z-index: 3; color: white;">Your Eco-Driving Dashboard</h2>
        <p style="font-size: 1.1rem; max-width: 80%; text-shadow: 0 1px 3px rgba(0,0,0,0.6); position: relative; z-index: 3; color: #E0E0E0;">Track your performance, reduce emissions, and save money with smart driving insights</p>
        
        <div style="position: absolute; bottom: 15px; right: 20px; font-size: 28px; opacity: 0.9; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.5));">🚗</div>
        <div style="position: absolute; top: 15px; right: 25px; font-size: 24px; opacity: 0.8; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.5));">🌿</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Welcome card with clean design and luxury hybrid car image
st.markdown(f"""
<div class="welcome-card-container">
    <div style="position: relative; z-index: 2; padding: 25px; background-color: rgba(0,0,0,0.5); border-radius: 10px; margin: 5px;">
        <h3 style="margin-top: 0; color: #9CCC65; font-size: 1.9rem; text-shadow: 0 2px 4px rgba(0,0,0,0.7); position: relative; z-index: 3;">{greeting}, {user_name}!</h3>
        <p style="font-size: 1.05rem; text-shadow: 0 1px 3px rgba(0,0,0,0.6); max-width: 85%; color: #E0E0E0; position: relative; z-index: 3; margin-bottom: 20px;">Today is {current_date}. Enjoy your eco-friendly driving experience.</p>
        <div style="display: inline-flex; align-items: center; gap: 8px; background-color: rgba(27, 94, 32, 0.8); padding: 8px 18px; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); position: relative; z-index: 3;">
            <span style="font-size: 20px; filter: drop-shadow(0 2px 3px rgba(0,0,0,0.3));">🌟</span>
            <span style="font-weight: bold; text-shadow: 0 1px 2px rgba(0,0,0,0.5); color: white;">Current Eco-Score: 85%</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Metrics in cards with custom styling - using improved structure
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='metric-card' style="position: relative; z-index: 1;">
        <div style="background-color: rgba(38, 50, 56, 0.9); border-radius: 10px; padding: 10px; position: relative; z-index: 2;">
            <div style="position: absolute; top: -10px; right: 10px; font-size: 18px; opacity: 0.6; transform: rotate(10deg); text-shadow: 0 2px 4px rgba(0,0,0,0.5);">⭐</div>
            <div style="position: relative; z-index: 5; padding: 5px 0;">
    """, unsafe_allow_html=True)
    st.metric(
        label="Current Eco Score", 
        value="85%", 
        delta="↑ 3%", 
        delta_color="normal"
    )
    st.markdown("</div></div></div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card' style="position: relative; z-index: 1;">
        <div style="background-color: rgba(38, 50, 56, 0.9); border-radius: 10px; padding: 10px; position: relative; z-index: 2;">
            <div style="position: absolute; top: -10px; right: 10px; font-size: 18px; opacity: 0.6; transform: rotate(10deg); text-shadow: 0 2px 4px rgba(0,0,0,0.5);">🌍</div>
            <div style="position: relative; z-index: 5; padding: 5px 0;">
    """, unsafe_allow_html=True)
    st.metric(
        label="Monthly CO2 Savings", 
        value="45 kg", 
        delta="↓ 12 kg", 
        delta_color="inverse"
    )
    st.markdown("</div></div></div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-card' style="position: relative; z-index: 1;">
        <div style="background-color: rgba(38, 50, 56, 0.9); border-radius: 10px; padding: 10px; position: relative; z-index: 2;">
            <div style="position: absolute; top: -10px; right: 10px; font-size: 18px; opacity: 0.6; transform: rotate(10deg); text-shadow: 0 2px 4px rgba(0,0,0,0.5);">🔧</div>
            <div style="position: relative; z-index: 5; padding: 5px 0;">
    """, unsafe_allow_html=True)
    st.metric(
        label="Next Maintenance", 
        value="15 days", 
        delta="Oil Change"
    )
    st.markdown("</div></div></div>", unsafe_allow_html=True)

# Interactive quick actions section
st.markdown("<h3 class='section-header'>Quick Actions</h3>", unsafe_allow_html=True)

# Use standard Streamlit components instead of HTML
quick_action_col1, quick_action_col2, quick_action_col3 = st.columns(3)

with quick_action_col1:
    if st.button("🚶 Start New Trip", use_container_width=True):
        st.session_state.start_trip = True
        st.success("Trip tracking started!")

with quick_action_col2:
    if st.button("📅 Schedule Maintenance", use_container_width=True):
        st.info("Redirecting to maintenance scheduling...")
        st.switch_page("pages/2_maintenance.py")

with quick_action_col3:
    if st.button("📊 View Full Reports", use_container_width=True):
        st.info("Generating comprehensive reports...")

# Recent activity with improved styling
st.markdown("<h3 class='section-header'>Recent Activity</h3>", unsafe_allow_html=True)

# Add filter controls
col1, col2 = st.columns([3, 1])
with col1:
    activity_filter = st.selectbox(
        "Filter by activity type:",
        ["All Activities", "Trips", "Maintenance", "Fuel"],
        index=0
    )
with col2:
    sort_order = st.radio(
        "Sort by:",
        ["Newest First", "Oldest First"],
        horizontal=True
    )

# Activity data
activity_data = {
    'Date': ['2024-01-15', '2024-01-14', '2024-01-13', '2024-01-10', '2024-01-08'],
    'Activity': ['Completed Trip', 'Maintenance Check', 'Fuel Refill', 'Completed Trip', 'Tire Pressure Check'],
    'Details': ['25 km, Eco Score: 87', 'Tire Pressure Check', '35L, $45', '18 km, Eco Score: 82', 'All tires adjusted to 32 PSI'],
    'Type': ['Trip', 'Maintenance', 'Fuel', 'Trip', 'Maintenance']
}

# Filter and sort data
import pandas as pd
df = pd.DataFrame(activity_data)
if activity_filter != "All Activities":
    filtered_type = activity_filter[:-1] if activity_filter.endswith("s") else activity_filter
    df = df[df['Type'] == filtered_type]

# Sort data based on selection
df['Date'] = pd.to_datetime(df['Date'])
if sort_order == "Newest First":
    df = df.sort_values(by='Date', ascending=False)
else:
    df = df.sort_values(by='Date', ascending=True)
df['Date'] = df['Date'].dt.strftime('%b %d, %Y')

# Simple activity cards using standard components with dynamic styling
if not df.empty:
    for _, row in df.iterrows():
        col1, col2 = st.columns([1, 4])
        
        # Set background color based on activity type
        if row['Type'] == 'Trip':
            bg_color = "#1B3C20"
            icon = "🚗"
            border_color = "#4CAF50"
        elif row['Type'] == 'Maintenance':
            bg_color = "#1A3855"
            icon = "🔧"
            border_color = "#2196F3"
        elif row['Type'] == 'Fuel':
            bg_color = "#553319"
            icon = "⛽"
            border_color = "#FF9800"
        else:
            bg_color = "#263238"
            icon = "📋"
            border_color = "#9E9E9E"
        
        with col1:
            st.markdown(f'<div style="font-size:36px; text-align:center; margin-top:10px;">{icon}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color: {bg_color}; padding: 12px; border-radius: 8px; margin-bottom: 12px; 
                      border-left: 4px solid {border_color}; box-shadow: 0 3px 6px rgba(0,0,0,0.2); 
                      transition: transform 0.2s; position: relative;"
                 onmouseover="this.style.transform='translateY(-3px)'"
                 onmouseout="this.style.transform='translateY(0)'">
                <div>
                    <strong style="color: #ECEFF1; font-size: 1.1rem;">{row['Activity']}</strong> 
                    <span style="float:right; color: #B0BEC5; font-size:0.9rem; background-color: rgba(0,0,0,0.2); 
                          padding: 2px 10px; border-radius: 12px;">{row['Date']}</span>
                </div>
                <div style="color: #B0BEC5; margin-top: 8px;">{row['Details']}</div>
                <div style="margin-top: 8px;">
                    <span style="background-color: {border_color}; color: white; padding: 3px 10px; 
                          border-radius: 12px; font-size: 0.8rem; display: inline-flex; align-items: center;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; 
                              background-color: white; margin-right: 5px;"></span>
                        {row['Type']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No activities found. Try changing your filter settings.")

# Driving tips section with simplified styling
st.markdown("<h3 class='section-header'>Today's Eco-Driving Tip</h3>", unsafe_allow_html=True)

# Randomize tips when page loads
if 'tip_changed' in st.session_state and st.session_state.tip_changed:
    daily_tip = random.choice(eco_tips)
    st.session_state.tip_changed = False  # Reset the flag
else:
    daily_tip = random.choice(eco_tips)  # Or keep the previous tip

# Enhance the eco-driving tip display with dynamic background image and improved styling
st.markdown(f"""
<div class="tip-card" style="background-image: url('{daily_tip["bg_image"]}');">
    <div style="position: relative; z-index: 2; display: flex; align-items: flex-start; padding: 15px; background-color: rgba(0,0,0,0.65); border-radius: 10px; margin: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
        <div style="font-size: 36px; margin-right: 20px; position: relative; z-index: 3; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">{daily_tip["icon"]}</div>
        <div style="flex: 1; position: relative; z-index: 3;">
            <h4 style="margin-top:0; color: #4CAF50; font-size: 1.3rem; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.7);">{daily_tip["title"]}</h4>
            <p style="line-height: 1.5; color: #E0E0E0; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">{daily_tip["content"]}</p>
            <div style="margin-top: 10px;">
                <span style="background-color: rgba(76, 175, 80, 0.7); color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; display: inline-flex; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background-color: white; margin-right: 5px;"></span>
                    Eco Tip
                </span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add button to get more eco tips
if st.button("🔄 Show me another tip", use_container_width=True):
    st.session_state.refresh_tip = True
    st.session_state.tip_changed = True  # Set the flag to indicate a tip change

# Footer with links
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; padding: 10px 0; color: #B0BEC5;">
    <span>© 2024 EcoDrive Companion</span>
    <span>
        <a href="#" style="text-decoration: none; margin-right: 15px; color: #4CAF50;">Privacy Policy</a>
        <a href="#" style="text-decoration: none; margin-right: 15px; color: #4CAF50;">Terms of Service</a>
        <a href="#" style="text-decoration: none; color: #4CAF50;">Help & Support</a>
    </span>
</div>
""", unsafe_allow_html=True)

# Sample data for demonstration
data = {
    'date': pd.date_range(start='2023-01-01', periods=30),
    'eco_score': [random.randint(50, 100) for _ in range(30)],
    'fuel_consumption': [random.uniform(5, 15) for _ in range(30)],
}

driving_data = pd.DataFrame(data)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Overview", "Detailed Analysis", "Trip History"])

# Overview Page
if page == "Overview":
    st.title("Driving Behavior Analysis")
    st.markdown("Gain insights into your driving patterns and receive personalized tips to improve your eco-driving score.")

    # Date Range Selector
    start_date, end_date = st.sidebar.date_input("Select Date Range", [datetime.date(2023, 1, 1), datetime.date(2023, 1, 30)])
    
    # Convert start_date and end_date to datetime64[ns]
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on date range
    filtered_data = driving_data[(driving_data['date'] >= start_date) & (driving_data['date'] <= end_date)]

    # Display Eco-Score Trend
    st.subheader("Eco-Score Trend")
    fig = px.line(filtered_data, x='date', y='eco_score', title='Eco-Score Over Time', markers=True)
    st.plotly_chart(fig)

    # Display Fuel Consumption Trend
    st.subheader("Fuel Consumption Trend")
    fig2 = px.line(filtered_data, x='date', y='fuel_consumption', title='Fuel Consumption Over Time', markers=True)
    st.plotly_chart(fig2)

# Detailed Analysis Page
elif page == "Detailed Analysis":
    st.title("Detailed Driving Analysis")
    st.markdown("Analyze your driving behavior in detail.")

    # Add more detailed analysis features here...
    st.markdown("### Key Metrics")
    avg_fuel = driving_data['fuel_consumption'].mean()
    st.metric(label="Average Fuel Consumption", value=f"{avg_fuel:.2f} L/100km")

# Trip History Page
elif page == "Trip History":
    st.title("Trip History")
    st.markdown("View your past trips and their details.")

    # Display trip history with filters
    st.dataframe(driving_data)

# Footer
st.markdown("---")
st.markdown("© 2023 Eco-Driving Assistant")
