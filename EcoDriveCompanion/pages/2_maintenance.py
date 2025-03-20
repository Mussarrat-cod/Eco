import streamlit as st
from utils.data_manager import DataManager
from utils.openai_helper import analyze_maintenance_needs
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Vehicle Maintenance | Eco-Driving Assistant",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS with dark theme
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

    .chart-container {
        background-color: var(--background-medium);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        border-left: 4px solid var(--primary);
    }
    
    .maintenance-card {
        background-color: var(--background-medium);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        margin-bottom: 12px;
        border-left: 3px solid var(--primary);
    }
    
    .maintenance-item {
        background-color: #19321E;
        border-left: 5px solid var(--primary);
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        position: relative;
    }
    
    .maintenance-due {
        background-color: #32231B;
        border-left: 5px solid var(--warning);
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    
    /* Button styling */
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
    
    /* Override Streamlit's default theme */
    .stApp {
        background-color: var(--background-dark);
    }
    
    h1, h2, h3, h4, h5, h6, .stMarkdown p {
        color: var(--text-light);
    }
    
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Table styling */
    div[data-testid="stTable"] table {
        border-radius: 8px;
        overflow: hidden;
    }
    
    div[data-testid="stTable"] th {
        background-color: var(--primary-dark);
        color: white;
    }
    
    div[data-testid="stTable"] td {
        background-color: var(--background-medium);
        color: var(--text-light);
    }
</style>
""", unsafe_allow_html=True)

# Page title with dynamic background
st.markdown("""
<div style="background: linear-gradient(90deg, rgba(27,94,32,0.8) 0%, rgba(46,125,50,0.7) 100%); 
            border-radius: 10px; padding: 20px; margin-bottom: 30px; position: relative; overflow: hidden;">
    <div style="position: absolute; top: 0; right: 0; font-size: 150px; opacity: 0.1; transform: translate(15%, -30%);">🔧</div>
    <h1 style="margin: 0; color: #ECEFF1; font-size: 2.5rem;">Vehicle Maintenance Tracker</h1>
    <p style="color: #B0BEC5; margin-top: 5px; font-size: 1.1rem;">
        Keep your vehicle in optimal condition for better efficiency and lower emissions.
    </p>
</div>
""", unsafe_allow_html=True)

# Get maintenance data
maintenance_data = DataManager.get_maintenance_schedule()

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["📆 Maintenance Schedule", "➕ Record Maintenance", "🤖 AI Recommendations"])

with tab1:
    # Display maintenance overview
    st.subheader("Current Maintenance Schedule")
    st.dataframe(maintenance_data, use_container_width=True)
    
    # Highlight upcoming maintenance
    st.markdown("<h3 style='color: #81C784; margin-top: 30px;'>Upcoming Maintenance</h3>", unsafe_allow_html=True)
    
    due_soon = maintenance_data[maintenance_data['status'] == 'Due Soon']
    if not due_soon.empty:
        for _, item in due_soon.iterrows():
            st.markdown(f"""
                <div class="maintenance-due">
                    <h4 style="color: #FFC107; margin-top: 0;">⚠️ {item['item']}</h4>
                    <p style="color: #B0BEC5;">Due on: <strong>{item['next_due']}</strong> (Interval: {item['interval_km']} km)</p>
                    <p style="color: #B0BEC5;">Last serviced: {item['last_service']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No maintenance due soon. Your vehicle is up to date!")
    
    # Maintenance history
    st.markdown("<h3 style='color: #81C784; margin-top: 30px;'>Maintenance History</h3>", unsafe_allow_html=True)
    completed = maintenance_data[maintenance_data['status'] == 'Completed']
    
    if not completed.empty:
        for _, item in completed.iterrows():
            st.markdown(f"""
                <div class="maintenance-item">
                    <h4 style="color: #81C784; margin-top: 0;">{item['item']}</h4>
                    <p style="color: #B0BEC5;">Last serviced: <strong>{item['last_service']}</strong></p>
                    <p style="color: #B0BEC5;">Next due: {item['next_due']} (Interval: {item['interval_km']} km)</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No maintenance history found.")

with tab2:
    # Add new maintenance record in a nicer card
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("Record New Maintenance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        maintenance_type = st.selectbox(
            "Maintenance Type",
            ["Oil Change", "Tire Rotation", "Air Filter", "Brake Service", "Fluid Check", "Battery Service", "Other"]
        )
    
    with col2:
        service_date = st.date_input("Service Date", datetime.now())
    
    with col3:
        mileage = st.number_input("Current Mileage (km)", min_value=0)
    
    notes = st.text_area("Maintenance Notes", placeholder="Enter any additional details about the service...")
    
    if st.button("Record Maintenance", use_container_width=True):
        st.success("Maintenance record added successfully!")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Maintenance tips
    st.markdown("<h3 style='color: #81C784; margin-top: 30px;'>Maintenance Tips</h3>", unsafe_allow_html=True)
    
    tips = [
        {
            "title": "Regular Oil Changes",
            "content": "Regular oil changes extend engine life and improve fuel efficiency. Follow manufacturer recommendations for oil type and change intervals."
        },
        {
            "title": "Tire Pressure Checks",
            "content": "Check tire pressure monthly. Properly inflated tires improve fuel economy and handling while reducing wear."
        },
        {
            "title": "Air Filter Maintenance",
            "content": "A clean air filter can improve acceleration and fuel economy. Check it during oil changes and replace when dirty."
        }
    ]
    
    for tip in tips:
        st.markdown(f"""
            <div class="maintenance-item">
                <h4 style="color: #81C784; margin-top: 0;">{tip['title']}</h4>
                <p style="color: #B0BEC5;">{tip['content']}</p>
            </div>
        """, unsafe_allow_html=True)

with tab3:
    # AI Maintenance Analysis with better styling
    st.subheader("AI Maintenance Analysis")
    
    try:
        maintenance_context = {
            "current_mileage": mileage,
            "maintenance_history": maintenance_data.to_dict(),
            "vehicle_age": 3  # Example value
        }
        
        analysis = analyze_maintenance_needs(maintenance_context)
        analysis_dict = json.loads(analysis)
        
        st.markdown("<h3 style='color: #81C784; margin-top: 10px;'>Recommendations</h3>", unsafe_allow_html=True)
        
        for recommendation in analysis_dict.get('recommendations', []):
            st.markdown(f"""
                <div class="maintenance-item">
                    <h4 style="color: #81C784; margin-top: 0;">💡 Recommendation</h4>
                    <p style="color: #B0BEC5;">{recommendation}</p>
                </div>
            """, unsafe_allow_html=True)
        
        if analysis_dict.get('urgent_items', []):
            st.markdown("<h3 style='color: #F44336; margin-top: 20px;'>Urgent Maintenance Required</h3>", unsafe_allow_html=True)
            
            for item in analysis_dict['urgent_items']:
                st.markdown(f"""
                    <div class="maintenance-due">
                        <h4 style="color: #F44336; margin-top: 0;">⚠️ Urgent</h4>
                        <p style="color: #B0BEC5;">{item}</p>
                    </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Unable to generate maintenance analysis: {str(e)}")
        
        # Fallback recommendations
        st.markdown("<h3 style='color: #81C784; margin-top: 20px;'>General Recommendations</h3>", unsafe_allow_html=True)
        
        fallback_recommendations = [
            "Check fluid levels (engine oil, coolant, brake fluid) regularly",
            "Inspect tires for wear and maintain proper inflation",
            "Replace air filter every 15,000-30,000 km",
            "Follow manufacturer-recommended maintenance schedule"
        ]
        
        for rec in fallback_recommendations:
            st.markdown(f"""
                <div class="maintenance-item">
                    <h4 style="color: #81C784; margin-top: 0;">💡 Recommendation</h4>
                    <p style="color: #B0BEC5;">{rec}</p>
                </div>
            """, unsafe_allow_html=True)
