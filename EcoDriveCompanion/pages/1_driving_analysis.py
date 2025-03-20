import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_manager import DataManager
from utils.openai_helper import get_driving_tips
import json
import pandas as pd
import datetime
import random

# Enable caching for better performance
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_driving_data():
    return DataManager.get_driving_history()

@st.cache_data(ttl=3600)  # Cache tips for 1 hour
def get_cached_driving_tips(data_dict):
    try:
        tips_json = get_driving_tips(data_dict)
        return json.loads(tips_json)
    except Exception as e:
        st.error(f"Unable to generate driving tips: {str(e)}")
        return {"tips": []}

# Page configuration
st.set_page_config(
    page_title="Driving Analysis | Eco-Driving Assistant",
    page_icon="🚦",
    layout="wide"
)

# Custom CSS with dark theme - optimized for performance
st.markdown("""
<style>
    :root {
        --primary-dark: #1B5E20;
        --primary: #2E7D32;
        --primary-light: #4CAF50;
        --accent: #81C784;
        --background-darkest: #121212;
        --background-dark: #1E1E1E;
        --background-medium: #202A2E;
        --text-light: #ECEFF1;
        --text-medium: #B0BEC5;
        --text-dark: #607D8B;
        --warning: #FFC107;
        --error: #F44336;
    }

    /* Text shadows for better performance */
    .text-shadow-sm {
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .text-shadow-md {
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }
    
    .text-shadow-lg {
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    }
    
    /* Common container styles */
    .card-container {
        background-color: var(--background-medium);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    /* Page header with dynamic background */
    .page-header {
        background: linear-gradient(90deg, rgba(27,94,32,0.85) 0%, rgba(46,125,50,0.85) 100%);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
        background-image: url('https://images.unsplash.com/photo-1553260188-75a8d6205b4e?auto=format&fit=crop&q=60&w=300');
        background-size: cover;
        background-position: center;
        background-blend-mode: overlay;
    }
    
    .page-header-content {
        position: relative;
        z-index: 2;
    }
    
    .page-title {
        margin: 0;
        color: #ECEFF1;
        font-size: 2.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .page-subtitle {
        color: #B0BEC5;
        margin-top: 5px;
        font-size: 1.1rem;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }
    
    /* Chart container styling */
    .chart-container {
        border-left: 4px solid var(--primary);
    }
    
    .chart-header {
        position: relative;
        z-index: 3;
        color: var(--primary-light);
        margin-bottom: 1rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .chart-container::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        width: 120px;
        background-image: url('https://images.unsplash.com/photo-1567808291548-fc3ee04dbcf0?auto=format&fit=crop&q=60&w=150');
        background-position: center right;
        background-repeat: no-repeat;
        background-size: cover;
        opacity: 0.1;
        z-index: 1;
    }
    
    /* Tips styling */
    .driving-tip {
        background-color: #19321E;
        border-left: 5px solid var(--primary);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
    }
    
    .driving-tip h4 {
        color: var(--accent);
        margin-top: 0;
        position: relative;
        z-index: 3;
    }
    
    .driving-tip p {
        position: relative;
        z-index: 3;
    }
    
    .tips-container {
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(25, 50, 30, 0.6);
        margin-top: 20px;
        margin-bottom: 30px;
        background-image: url('https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&q=60&w=200');
        background-size: cover;
        background-position: center;
        background-blend-mode: soft-light;
        position: relative;
        overflow: hidden;
    }
    
    .tips-header {
        color: #81C784;
        margin-top: 10px;
        margin-bottom: 20px;
        position: relative;
        z-index: 3;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
    }
    
    /* Score container styling */
    .score-title {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: var(--primary-light);
        text-shadow: 0 1px 3px rgba(0,0,0,0.4);
        position: relative;
        z-index: 3;
    }
    
    .score-container {
        background: linear-gradient(90deg, rgba(23, 61, 27, 0.85) 0%, rgba(27, 71, 32, 0.85) 50%, rgba(31, 81, 37, 0.85) 100%);
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
        background-image: url('https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&q=60&w=300');
        background-size: cover;
        background-position: center;
        background-blend-mode: overlay;
    }
    
    .score-content {
        position: relative;
        z-index: 2;
        background-color: rgba(0,0,0,0.5);
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
    }
    
    /* Trip card styling */
    .trip-card {
        background-color: var(--background-medium);
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        margin-bottom: 15px;
        border-left: 3px solid var(--primary);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .trip-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .trip-card::after {
        content: "🚗";
        position: absolute;
        bottom: 10px;
        right: 20px;
        font-size: 24px;
        opacity: 0.1;
        transform: rotate(-5deg);
    }
    
    .trip-card h4 {
        color: var(--text-light);
        margin-top: 0;
        position: relative;
        z-index: 2;
    }
    
    .trip-details {
        position: relative;
        z-index: 2;
    }
    
    .eco-score-circle {
        position: relative;
        z-index: 2;
    }
    
    .metric-label {
        font-weight: 600;
        color: var(--text-medium);
    }
    
    .filter-container {
        background-color: #162938;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid #2196F3;
    }
    
    /* UI controls styling */
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 4px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-light);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stSlider [data-baseweb=slider] {
        height: 6px;
    }
    
    .stSlider [data-baseweb=thumb] {
        background-color: var(--primary-light);
    }
    
    .stRadio>div {
        background-color: var(--background-medium);
        padding: 10px;
        border-radius: 5px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        background-color: var(--background-medium);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: white !important;
    }
    
    /* Override Streamlit's default theme */
    .stApp {
        background-color: var(--background-dark);
    }
    
    h1, h2, h3, h4, h5, h6, .stMarkdown p {
        color: var(--text-light);
    }
    
    .stSelectbox label, .stSlider label {
        color: var(--text-medium) !important;
    }
    
    /* Apply card-container class to chart and other containers */
    .chart-container, .tips-container, .score-container, .filter-container {
        @extend .card-container;
    }
</style>
""", unsafe_allow_html=True)

# Page title with dynamic background
st.markdown("""
<div class="page-header">
    <div class="page-header-content">
        <h1 class="page-title">Driving Behavior Analysis</h1>
        <p class="page-subtitle">
            Gain insights into your driving patterns and receive personalized tips to improve your eco-driving score.
        </p>
    </div>
    <div style="position: absolute; top: 10px; right: 20px; font-size: 50px; opacity: 0.8; text-shadow: 0 2px 5px rgba(0,0,0,0.6);">🚦</div>
    <div style="position: absolute; bottom: 10px; right: 80px; font-size: 35px; opacity: 0.7; text-shadow: 0 2px 5px rgba(0,0,0,0.6);">🚗</div>
</div>
""", unsafe_allow_html=True)

# Get driving data
driving_data = load_driving_data()

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "📝 Trip History"])

with tab1:
    # Display overall eco-score with gauge chart
    current_score = driving_data['eco_score'].iloc[-1]
    previous_score = driving_data['eco_score'].iloc[-2]
    score_change = current_score - previous_score
    
    st.markdown("""
    <div class='score-container'>
        <div class='score-content'>
            <h2 class='score-title'>Current Eco-Score</h2>
    """, unsafe_allow_html=True)
    
    # Create a gauge chart for the eco-score with dark theme - optimized for performance
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_score,
        delta={"reference": previous_score, "valueformat": ".0f", "font": {"color": "#B0BEC5"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#4CAF50", "tickmode": "array", "tickvals": [0, 50, 75, 100]},
            "bar": {"color": "#4CAF50" if current_score >= 75 else "#FFC107" if current_score >= 50 else "#F44336"},
            "steps": [
                {"range": [0, 50], "color": "#922016"},  # Dark red
                {"range": [50, 75], "color": "#9C6A00"},  # Dark amber
                {"range": [75, 100], "color": "#0A3E17"}  # Dark green
            ],
            "threshold": {
                "line": {"color": "white", "width": 3},
                "thickness": 0.75,
                "value": 85
            }
        },
        number={"font": {"color": "#ECEFF1", "size": 40}},
        title={"text": "Eco-Driving Score", "font": {"color": "#B0BEC5"}}
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#B0BEC5"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add interpretation text
    if current_score >= 85:
        interpretation = "Excellent! You're driving very efficiently."
    elif current_score >= 70:
        interpretation = "Good job! There's still room for improvement."
    elif current_score >= 50:
        interpretation = "Consider adjusting your driving habits for better efficiency."
    else:
        interpretation = "Your driving patterns need significant improvement for better efficiency."
        
    st.markdown(f"""
        <p style='text-align:center; font-size:1.1rem; color:#B0BEC5; text-shadow: 0 1px 2px rgba(0,0,0,0.3);'>{interpretation}</p>
        </div>
        <div style="position: absolute; bottom: 15px; right: 30px; font-size: 35px; opacity: 0.7; text-shadow: 0 2px 5px rgba(0,0,0,0.6);">🚗</div>
        <div style="position: absolute; top: 20px; right: 70px; font-size: 25px; opacity: 0.6; text-shadow: 0 2px 5px rgba(0,0,0,0.6);">🌿</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics in a row
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_fuel = driving_data['fuel_consumption'].mean()
        st.metric(
            label="Avg. Fuel Consumption",
            value=f"{avg_fuel:.1f} L/100km",
            delta=f"{avg_fuel - driving_data['fuel_consumption'].iloc[0]:.1f}",
            delta_color="inverse"
        )
    
    with col2:
        total_distance = driving_data['distance'].sum()
        st.metric(
            label="Total Distance",
            value=f"{total_distance:.1f} km",
            delta=f"{driving_data['distance'].iloc[-7:].sum() - driving_data['distance'].iloc[-14:-7].sum():.1f} km"
        )
    
    with col3:
        harsh_events = driving_data['harsh_braking'].sum() + driving_data['rapid_acceleration'].sum()
        recent_harsh = driving_data['harsh_braking'].iloc[-7:].sum() + driving_data['rapid_acceleration'].iloc[-7:].sum()
        previous_harsh = driving_data['harsh_braking'].iloc[-14:-7].sum() + driving_data['rapid_acceleration'].iloc[-14:-7].sum()
        st.metric(
            label="Harsh Driving Events",
            value=f"{harsh_events}",
            delta=f"{recent_harsh - previous_harsh}",
            delta_color="inverse"
        )
    
    # AI-powered driving tips with better styling
    st.markdown("""
    <div class='tips-container'>
        <h3 class='tips-header'>AI-Powered Driving Tips</h3>
        <div style="position: absolute; top: 10px; right: 20px; font-size: 40px; opacity: 0.5; text-shadow: 0 2px 5px rgba(0,0,0,0.5);">🚗</div>
        <div style="position: absolute; bottom: 15px; right: 70px; font-size: 25px; opacity: 0.4; text-shadow: 0 2px 5px rgba(0,0,0,0.5);">🌱</div>
    """, unsafe_allow_html=True)

    with st.spinner("Analyzing your driving patterns..."):
        try:
            # Get recent driving data (last 7 days)
            recent_data = driving_data.tail(7).to_dict()
            
            # Get driving tips from OpenAI
            tips_dict = get_cached_driving_tips(recent_data)
            
            # Display each tip with nicer styling
            if 'tips' in tips_dict and tips_dict['tips']:
                if 'tip_index' not in st.session_state:
                    st.session_state.tip_index = random.randint(0, len(tips_dict['tips']) - 1)

                # Display the tip based on the index
                daily_tip = tips_dict['tips'][st.session_state.tip_index]

                st.markdown(f"""
                    <div class='driving-tip'>
                        <div style="position: absolute; top: 0; right: 0; font-size: 80px; opacity: 0.08; transform: translate(20%, -30%);">💡</div>
                        <h4>Tip {st.session_state.tip_index + 1}</h4>
                        <p style="color: #B0BEC5;">{daily_tip}</p>
                    </div>
                """, unsafe_allow_html=True)

                if st.button("🔄 Show me another tip", use_container_width=True):
                    st.session_state.tip_index = random.randint(0, len(tips_dict['tips']) - 1)
                    st.experimental_rerun()  # Only if you have the correct version
            else:
                st.warning("No specific driving tips available at this time.")
        except Exception as e:
            st.error(f"Unable to generate driving tips: {str(e)}")
            # Display fallback tips with nicer styling
            fallback_tips = [
                "Practice gradual acceleration to improve fuel efficiency.",
                "Maintain a steady speed and avoid unnecessary braking.",
                "Regular vehicle maintenance keeps your car running efficiently."
            ]
            for i, tip in enumerate(fallback_tips, 1):
                st.markdown(f"""
                    <div class='driving-tip'>
                        <div style="position: absolute; top: 0; right: 0; font-size: 80px; opacity: 0.08; transform: translate(20%, -30%);">💡</div>
                        <h4>Tip {i}</h4>
                        <p style="color: #B0BEC5;">{tip}</p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    # Time period selector
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    period = st.radio(
        "Select Time Period:",
        ["Last 7 Days", "Last 14 Days", "Last 30 Days", "Custom Range"],
        horizontal=True
    )
    
    if period == "Custom Range":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                datetime.datetime.now() - datetime.timedelta(days=7)
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                datetime.datetime.now()
            )
        filtered_data = driving_data[(driving_data['date'].dt.date >= start_date) & 
                                     (driving_data['date'].dt.date <= end_date)]
    else:
        days = 7 if period == "Last 7 Days" else 14 if period == "Last 14 Days" else 30
        filtered_data = driving_data.tail(days)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Enhanced charts with better styling
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-header'>Eco-Score Trend</h3>", unsafe_allow_html=True)
        fig_score = px.line(
            filtered_data,
            x='date',
            y='eco_score',
            title=None,
            line_shape='linear',
            markers=True
        )
        fig_score.update_traces(line=dict(width=2, color='#4CAF50'), marker=dict(size=6))
        fig_score.update_layout(
            xaxis_title="Date",
            yaxis_title="Eco-Score",
            xaxis=dict(showgrid=False, color="#607D8B", nticks=8),
            yaxis=dict(range=[0, 100], color="#607D8B"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={"color": "#B0BEC5"},
            hovermode='x unified',
            margin=dict(l=50, r=20, t=30, b=50)
        )
        st.plotly_chart(fig_score, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-header'>Fuel Consumption Trend</h3>", unsafe_allow_html=True)
        fig_fuel = px.line(
            filtered_data,
            x='date',
            y='fuel_consumption',
            title=None,
            line_shape='linear',
            markers=True
        )
        fig_fuel.update_traces(line=dict(width=2, color='#2196F3'), marker=dict(size=6))
        fig_fuel.update_layout(
            xaxis_title="Date",
            yaxis_title="Fuel Consumption (L/100km)",
            xaxis=dict(showgrid=False, color="#607D8B", nticks=8),
            yaxis=dict(color="#607D8B"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={"color": "#B0BEC5"},
            hovermode='x unified',
            margin=dict(l=50, r=20, t=30, b=50)
        )
        st.plotly_chart(fig_fuel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Driving events analysis with improved charts
    st.markdown("<h3 style='color: var(--primary-light); margin-top: 30px; text-shadow: 0 1px 2px rgba(0,0,0,0.3);'>Driving Events Analysis</h3>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-header'>Harsh Braking Events</h3>", unsafe_allow_html=True)
        fig_braking = px.bar(
            filtered_data,
            x='date',
            y='harsh_braking',
            title=None,
            color_discrete_sequence=['#F44336']
        )
        fig_braking.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={"color": "#B0BEC5"},
            xaxis=dict(color="#607D8B", nticks=6),
            yaxis=dict(color="#607D8B"),
            bargap=0.3,
            margin=dict(l=50, r=20, t=30, b=50)
        )
        st.plotly_chart(fig_braking, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-header'>Rapid Acceleration Events</h3>", unsafe_allow_html=True)
        fig_accel = px.bar(
            filtered_data,
            x='date',
            y='rapid_acceleration',
            title=None,
            color_discrete_sequence=['#FF9800']
        )
        fig_accel.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={"color": "#B0BEC5"},
            xaxis=dict(color="#607D8B", nticks=6),
            yaxis=dict(color="#607D8B"),
            bargap=0.3,
            margin=dict(l=50, r=20, t=30, b=50)
        )
        st.plotly_chart(fig_accel, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Combined analysis chart - optimized for performance
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<h3 class='chart-header'>Combined Analysis</h3>", unsafe_allow_html=True)

    # Create a figure with secondary y-axis
    fig = go.Figure()

    # Add eco-score line - optimized with fewer points if possible
    fig.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['eco_score'],
        name='Eco-Score',
        line=dict(color='#4CAF50', width=2),
        mode='lines+markers',
        marker=dict(size=6)
    ))

    # Add harsh events bars with simplified configuration
    fig.add_trace(go.Bar(
        x=filtered_data['date'],
        y=filtered_data['harsh_braking'],
        name='Harsh Braking',
        marker_color='#F44336',
        opacity=0.7
    ))

    fig.add_trace(go.Bar(
        x=filtered_data['date'],
        y=filtered_data['rapid_acceleration'],
        name='Rapid Acceleration',
        marker_color='#FF9800',
        opacity=0.7
    ))

    # Update layout with optimized configuration
    fig.update_layout(
        title=None,
        xaxis_title="Date",
        yaxis_title="Eco-Score",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={"color": "#B0BEC5"},
        xaxis=dict(color="#607D8B", nticks=6),
        yaxis=dict(color="#607D8B"),
        barmode='group',
        bargap=0.2,
        hovermode='x unified',
        margin=dict(l=50, r=20, t=40, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#B0BEC5", size=11)
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    # Trip History with search and filter
    st.subheader("Trip History")
    
    # Add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_eco_score = st.slider("Minimum Eco-Score", 0, 100, 0)
    with col2:
        date_range = st.date_input(
            "Date Range",
            [
                datetime.datetime.now() - datetime.timedelta(days=30),
                datetime.datetime.now()
            ]
        )
    with col3:
        sort_by = st.selectbox(
            "Sort By",
            ["Date (newest first)", "Date (oldest first)", "Eco-Score (highest first)", "Eco-Score (lowest first)"]
        )
    
    # Filter and sort the data
    filtered_trips = driving_data[driving_data['eco_score'] >= min_eco_score].copy()
    
    if len(date_range) == 2:
        filtered_trips = filtered_trips[
            (filtered_trips['date'].dt.date >= date_range[0]) & 
            (filtered_trips['date'].dt.date <= date_range[1])
        ]
    
    # Apply sorting
    if sort_by == "Date (newest first)":
        filtered_trips = filtered_trips.sort_values(by='date', ascending=False)
    elif sort_by == "Date (oldest first)":
        filtered_trips = filtered_trips.sort_values(by='date', ascending=True)
    elif sort_by == "Eco-Score (highest first)":
        filtered_trips = filtered_trips.sort_values(by='eco_score', ascending=False)
    elif sort_by == "Eco-Score (lowest first)":
        filtered_trips = filtered_trips.sort_values(by='eco_score', ascending=True)
    
    # Display trips as cards with updated styling for dark theme
    if not filtered_trips.empty:
        for _, trip in filtered_trips.iterrows():
            eco_score_color = "#4CAF50" if trip['eco_score'] >= 75 else "#FFC107" if trip['eco_score'] >= 50 else "#F44336"
            
            st.markdown(f"""
                <div class='trip-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div class='trip-details'>
                            <h4 style="margin-top: 0;">{trip['date'].strftime('%B %d, %Y')}</h4>
                            <p style="color: #B0BEC5;"><span class='metric-label'>Distance:</span> {trip['distance']} km</p>
                            <p style="color: #B0BEC5;"><span class='metric-label'>Eco-Score:</span> <span style="color: {eco_score_color};">{trip['eco_score']}</span></p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No trips found for the selected filters.")