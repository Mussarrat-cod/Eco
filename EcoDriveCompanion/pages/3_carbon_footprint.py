import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_manager import DataManager
import pandas as pd
import numpy as np
import datetime

# Page Configuration
st.set_page_config(
    page_title="Carbon Footprint | Eco-Driving Assistant",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
    # Apply dark theme
    menu_items={
        'Get Help': 'https://www.ecodrivecompanion.com/help',
        'Report a bug': 'https://www.ecodrivecompanion.com/bug',
        'About': 'EcoDrive Companion helps track and reduce your carbon emissions while driving.'
    }
)

# Custom CSS
st.markdown("""
<style>
    /* Root variables for consistent theming */
    :root {
        --primary-darkest: #0C3D10;
        --primary-darker: #145218;
        --primary-dark: #1B5E20;
        --primary-main: #2E7D32;
        --primary-light: #4CAF50;
        --secondary-dark: #0D47A1;
        --secondary-main: #1976D2;
        --background-darker: #121212;
        --background-dark: #1E1E1E;
        --background-medium: #202A2E;
        --background-light: #263238;
        --text-light: #ECEFF1;
        --text-medium: #B0BEC5;
        --text-dark: #78909C;
    }

    .page-title {
        font-size: 2.3rem;
        font-weight: 600;
        color: var(--primary-light);
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    }

    .chart-container {
        background-color: var(--background-medium);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
        border-left: 4px solid var(--primary-light);
        color: var(--text-light);
    }

    .metric-container {
        background-color: var(--background-dark);
        background: linear-gradient(135deg, var(--background-dark) 0%, var(--background-medium) 100%);
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        margin-bottom: 25px;
        text-align: center;
        border-left: 4px solid var(--primary-light);
        color: var(--text-light);
    }

    .calculator-container {
        background-color: var(--background-medium);
        background: linear-gradient(135deg, #1A2327 0%, var(--background-medium) 100%);
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        margin-bottom: 25px;
        border-left: 4px solid var(--primary-light);
        color: var(--text-light);
    }

    .info-box {
        background-color: #162938;
        border-left: 5px solid var(--secondary-main);
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 22px;
        color: var(--text-light);
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
    }

    .eco-tip {
        background-color: #19321E;
        border-left: 5px solid var(--primary-light);
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: var(--text-light);
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
    }

    /* Button styling */
    .stButton>button {
        background-color: var(--primary-main);
        color: white;
        border: none;
        border-radius: 4px;
        transition: all 0.3s;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }

    .stButton>button:hover {
        background-color: var(--primary-dark);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }

    /* Radio buttons */
    .stRadio>div {
        background-color: var(--background-dark);
        padding: 10px;
        border-radius: 8px;
        color: var(--text-light);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        background-color: var(--background-dark);
        color: var(--text-light);
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary-dark) !important;
        color: white !important;
    }
    
    /* Background styling for charts and plots */
    .js-plotly-plot .plot-container .svg-container {
        background-color: transparent !important;
    }
    
    /* Metric overrides for dark background */
    [data-testid="stMetricValue"] {
        color: var(--text-light) !important;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-medium) !important;
    }
    
    /* Header styling */
    h1, h2, h3, h4 {
        color: var(--text-light);
    }
    
    /* General text styling */
    p, li, td, th {
        color: var(--text-medium);
    }
</style>
""", unsafe_allow_html=True)

# Page Title with dynamic background
st.markdown("""
<div style="position: relative; overflow: hidden; border-radius: 12px; margin-bottom: 30px; padding: 30px; background: linear-gradient(90deg, rgba(27,94,32,0.95) 0%, rgba(38,50,56,0.95) 100%);">
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.2;">
        <img src="https://images.unsplash.com/photo-1576661929310-a29e8fc38c7f?auto=format&fit=crop&q=80" style="width: 100%; height: 100%; object-fit: cover;">
    </div>
    <h1 style="color: white; font-size: 2.5rem; margin-bottom: 5px;">🌱 Carbon Footprint Analysis</h1>
    <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem;">Track, understand, and reduce your driving emissions</p>
</div>
""", unsafe_allow_html=True)

# Information Box with darker styling
st.markdown("""
<div class="info-box">
    <h4 style="color: #90CAF9; margin-top: 0;">Understanding Carbon Footprint</h4>
    <p>Your carbon footprint represents the total greenhouse gases (including CO₂ and methane) 
    generated by your driving activities. These emissions contribute to climate change, but with 
    conscious choices, you can significantly reduce your environmental impact while saving on fuel costs.</p>
</div>
""", unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "🧮 Calculator"])

with tab1:
    # Get emissions data
    emissions_data = DataManager.get_emissions_data()
    
    # Check if data is not empty and has at least 2 rows
    if not emissions_data.empty and len(emissions_data) >= 2:
        # Overall statistics
        total_emissions = emissions_data['emissions'].sum()
        average_emissions = emissions_data['emissions'].mean()
        recent_month_emissions = emissions_data['emissions'].iloc[-1]
        previous_month_emissions = emissions_data['emissions'].iloc[-2]
        
        # Add a dynamic gauge chart for current emissions
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=recent_month_emissions,
            delta={"reference": previous_month_emissions, "valueformat": ".1f"},
            gauge={
                "axis": {"range": [0, max(500, recent_month_emissions * 1.5)], "tickwidth": 1, "tickcolor": "#4CAF50"},
                "bar": {"color": "#4CAF50" if recent_month_emissions < previous_month_emissions else "#F44336"},
                "steps": [
                    {"range": [0, 200], "color": "#0A3E17"},  # Dark green
                    {"range": [200, 400], "color": "#9C6A00"},  # Dark amber
                    {"range": [400, 1000], "color": "#922016"}  # Dark red
                ],
                "threshold": {
                    "line": {"color": "white", "width": 2},
                    "thickness": 0.75,
                    "value": average_emissions
                }
            },
            number={"valueformat": ".0f", "font": {"color": "#ECEFF1", "size": 40}},
            title={"text": "Current Month CO₂ Emissions (kg)", "font": {"color": "#B0BEC5"}}
        ))
        
        fig.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#ECEFF1"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Key metrics in a row with improved styling
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.metric(
                label="Total CO2 Emissions",
                value=f"{total_emissions:.1f} kg",
                delta=f"{(emissions_data['emissions'].iloc[-1] - emissions_data['emissions'].iloc[-2]):.1f} kg",
                delta_color="inverse"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.metric(
                label="Monthly Average",
                value=f"{average_emissions:.1f} kg",
                delta=f"{(average_emissions - emissions_data['emissions'].iloc[0]):.1f} kg",
                delta_color="inverse"
            )
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col3:
            emissions_per_km = emissions_data['emissions'].sum() / emissions_data['distance'].sum() if emissions_data['distance'].sum() > 0 else 0
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.metric(
                label="Avg. Emissions per km",
                value=f"{emissions_per_km:.2f} kg/km",
                help="Lower values indicate more efficient driving"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Environmental Impact Section
        st.subheader("Environmental Impact")
        
        # Calculate equivalent values for context
        trees_needed = total_emissions / 25  # Approx. CO2 absorbed by one tree per year
        homes_equivalent = total_emissions / 5000  # Approx. annual CO2 from one home
        
        impact_col1, impact_col2 = st.columns(2)
        
        with impact_col1:
            st.markdown("""
            <div class="eco-tip">
                <h4>🌳 Trees Equivalent</h4>
                <p>Your emissions would require approximately <b>{:.1f} trees growing for one year</b> to offset.</p>
            </div>
            """.format(trees_needed), unsafe_allow_html=True)
        
        with impact_col2:
            st.markdown("""
            <div class="eco-tip">
                <h4>🏠 Home Energy Equivalent</h4>
                <p>Your emissions represent about <b>{:.2f}%</b> of an average home's annual energy usage.</p>
            </div>
            """.format(homes_equivalent * 100), unsafe_allow_html=True)
    
    else:
        st.warning("Not enough emissions data available. Please ensure your data has at least 2 entries.")

with tab2:
    if not emissions_data.empty and len(emissions_data) >= 2:
        # Time period selector
        period = st.radio(
            "Select Time Period:",
            ["Last 6 Months", "Last 12 Months", "All Data"],
            horizontal=True
        )
        
        if period == "Last 6 Months":
            filtered_data = emissions_data.iloc[-6:]
        elif period == "Last 12 Months":
            filtered_data = emissions_data.iloc[-12:]
        else:
            filtered_data = emissions_data
        
        # Enhanced Emissions trend chart
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Monthly Emissions Trend")
        
        fig_emissions = px.line(
            filtered_data,
            x='date',
            y='emissions',
            title=None,
            line_shape='spline',
            markers=True
        )
        
        fig_emissions.update_traces(
            line=dict(width=3, color='#4CAF50'),
            marker=dict(size=8, color='#2E7D32')
        )
        
        fig_emissions.update_layout(
            xaxis_title="Month",
            yaxis_title="CO₂ Emissions (kg)",
            xaxis=dict(showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
        
        # Add a target line (10% below average)
        target = filtered_data['emissions'].mean() * 0.9
        fig_emissions.add_shape(
            type="line",
            x0=filtered_data['date'].min(),
            y0=target,
            x1=filtered_data['date'].max(),
            y1=target,
            line=dict(color="rgba(255, 0, 0, 0.5)", width=2, dash="dash"),
        )
        
        fig_emissions.add_annotation(
            x=filtered_data['date'].max(),
            y=target,
            text="Target",
            showarrow=False,
            yshift=10,
            font=dict(color="red")
        )
        
        st.plotly_chart(fig_emissions, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Two charts side by side
        col1, col2 = st.columns(2)
        
        with col1:
            # Emissions vs. Distance
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Emissions vs. Distance")
            
            fig_scatter = px.scatter(
                filtered_data,
                x='distance',
                y='emissions',
                title=None,
                color='average_consumption',
                color_continuous_scale='Viridis',
                labels={"average_consumption": "Fuel Consumption (L/100km)"}
            )
            
            fig_scatter.update_traces(marker=dict(size=12, opacity=0.7))
            
            fig_scatter.update_layout(
                xaxis_title="Distance (km)",
                yaxis_title="CO₂ Emissions (kg)",
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Fuel efficiency trend
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Fuel Efficiency Trend")
            
            fig_efficiency = px.line(
                filtered_data,
                x='date',
                y='average_consumption',
                title=None,
                line_shape='spline',
                markers=True
            )
            
            fig_efficiency.update_traces(
                line=dict(width=3, color='#2196F3'),
                marker=dict(size=8, color='#1565C0')
            )
            
            fig_efficiency.update_layout(
                xaxis_title="Month",
                yaxis_title="Fuel Consumption (L/100km)",
                xaxis=dict(showgrid=False),
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_efficiency, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Monthly comparison with enhanced visualization
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Your Emissions vs. Average")
        
        comparison_data = pd.DataFrame({
            'Category': ['Your Average', 'Regional Average', 'National Average', 'Target'],
            'Emissions': [average_emissions, 350, 400, average_emissions * 0.8]
        })
        
        fig_comparison = px.bar(
            comparison_data,
            x='Category',
            y='Emissions',
            title=None,
            color='Category',
            color_discrete_map={
                'Your Average': '#4CAF50',
                'Regional Average': '#2196F3',
                'National Average': '#9E9E9E',
                'Target': '#FF9800'
            }
        )
        
        fig_comparison.update_layout(
            xaxis_title=None,
            yaxis_title="Monthly Emissions (kg CO₂)",
            legend_title=None,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_comparison, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Monthly breakdown
        st.subheader("Monthly Breakdown")
        
        # Add a month selector
        months = filtered_data['date'].dt.strftime('%B %Y').tolist()
        selected_month = st.selectbox("Select Month", months, index=len(months)-1)
        
        selected_idx = months.index(selected_month)
        month_data = filtered_data.iloc[selected_idx]
        
        cols = st.columns(4)
        
        with cols[0]:
            st.metric("CO₂ Emissions", f"{month_data['emissions']:.1f} kg")
        
        with cols[1]:
            st.metric("Distance", f"{month_data['distance']:.1f} km")
        
        with cols[2]:
            st.metric("Avg. Consumption", f"{month_data['average_consumption']:.1f} L/100km")
        
        with cols[3]:
            emissions_per_km = month_data['emissions'] / month_data['distance'] if month_data['distance'] > 0 else 0
            st.metric("Emissions per km", f"{emissions_per_km:.2f} kg/km")
        
    else:
        st.warning("Not enough data available for detailed analysis.")
    
with tab3:
    # Carbon footprint calculator with improved UI
    st.markdown("<div class='calculator-container'>", unsafe_allow_html=True)
    st.subheader("Carbon Footprint Calculator")
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        # Vehicle type presets
        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["Small Car (Petrol)", "Medium Car (Petrol)", "Large Car (Petrol)", "Small Car (Diesel)", 
             "Medium Car (Diesel)", "Hybrid", "Electric", "Custom"]
        )
        
        # Set default consumption based on vehicle type
        if vehicle_type == "Small Car (Petrol)":
            default_consumption = 7.0
        elif vehicle_type == "Medium Car (Petrol)":
            default_consumption = 8.5
        elif vehicle_type == "Large Car (Petrol)":
            default_consumption = 10.0
        elif vehicle_type == "Small Car (Diesel)":
            default_consumption = 5.5
        elif vehicle_type == "Medium Car (Diesel)":
            default_consumption = 6.5
        elif vehicle_type == "Hybrid":
            default_consumption = 4.5
        elif vehicle_type == "Electric":
            default_consumption = 0.0
        else:  # Custom
            default_consumption = 7.0
        
        distance = st.number_input("Distance (km)", min_value=0.0, value=100.0, step=10.0)
    
    with calc_col2:
        # Allow customization of consumption if "Custom" is selected
        if vehicle_type == "Custom":
            consumption = st.number_input("Fuel Consumption (L/100km)", min_value=0.0, value=default_consumption, step=0.5)
        else:
            consumption = default_consumption
            st.metric("Fuel Consumption", f"{consumption} L/100km")
        
        # For electric vehicles, use a different calculation approach
        if vehicle_type == "Electric":
            electricity_kwh = st.number_input("Electricity Consumption (kWh/100km)", min_value=0.0, value=18.0, step=1.0)
    
    # Calculate button with animation
    if st.button("Calculate Emissions", use_container_width=True):
        with st.spinner("Calculating your carbon footprint..."):
            try:
                # Different calculation for electric vehicles
                if vehicle_type == "Electric":
                    # Using average grid emissions factor (varies by country)
                    grid_factor = 0.4  # kg CO2 per kWh (example value)
                    emissions = (distance * electricity_kwh / 100) * grid_factor
                    fuel_text = f"{electricity_kwh} kWh/100km"
                else:
                    emissions = DataManager.calculate_carbon_footprint(distance, consumption)
                    fuel_text = f"{consumption} L/100km"
                
                # Success message with detailed breakdown
                st.success(f"Estimated CO2 emissions for this trip: {emissions:.2f} kg")
                
                # Display results in a nice format
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1A2734 0%, #1E2A20 100%); padding:20px; border-radius:10px; margin-top:20px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                    <h4 style="color: #4CAF50; margin-top: 0; border-bottom: 1px solid rgba(76, 175, 80, 0.3); padding-bottom: 10px;">Emission Analysis Results</h4>
                    <div style="display: flex; align-items: center; margin-bottom: 20px;">
                        <div style="font-size: 48px; margin-right: 20px; color: {('#4CAF50' if emissions < 50 else '#FFC107' if emissions < 100 else '#F44336')};">
                            {emissions:.1f}
                        </div>
                        <div>
                            <div style="font-size: 18px; color: #B0BEC5;">kg CO₂</div>
                            <div style="color: #78909C; font-size: 14px;">Total Emissions</div>
                        </div>
                    </div>
                    <table style="width:100%; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 8px 0; color: #B0BEC5;"><b>Vehicle Type:</b></td>
                            <td style="padding: 8px 0; color: #ECEFF1;">{vehicle_type}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 8px 0; color: #B0BEC5;"><b>Distance:</b></td>
                            <td style="padding: 8px 0; color: #ECEFF1;">{distance} km</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                            <td style="padding: 8px 0; color: #B0BEC5;"><b>Consumption:</b></td>
                            <td style="padding: 8px 0; color: #ECEFF1;">{fuel_text}</td>
                        </tr>
                    </table>
                    <div style="margin-top: 15px; background-color: rgba(76, 175, 80, 0.1); padding: 10px; border-radius: 5px; display: flex; align-items: center;">
                        <span style="color: #4CAF50; font-size: 20px; margin-right: 10px;">💡</span>
                        <span style="color: #B0BEC5;">This trip represents {(emissions / (average_emissions / 30)):.1f} days of your average monthly emissions.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add context to the calculation
                trees_needed = emissions / 25 * 365  # Approximate CO2 absorbed by one tree per year
                st.markdown(f"""
                <div class="eco-tip" style="position: relative; overflow: hidden;">
                    <div style="position: absolute; top: 0; right: 0; font-size: 80px; opacity: 0.05; transform: translate(20%, -30%);">🌳</div>
                    <h4 style="color: #81C784; margin-top: 0;">Environmental Impact</h4>
                    <p>If you made this trip daily for a year, it would require approximately <b style="color: #ECEFF1;">{trees_needed:.1f} trees</b> to offset the carbon emissions.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Reduction tips based on vehicle type with enhanced styling
                if vehicle_type.endswith("Petrol)") or vehicle_type.endswith("Diesel)"):
                    st.markdown("""
                    <div class="eco-tip" style="position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 0; right: 0; font-size: 80px; opacity: 0.05; transform: translate(20%, -30%);">🚗</div>
                        <h4 style="color: #81C784; margin-top: 0;">Combustion Engine Tips</h4>
                        <ul style="padding-left: 20px;">
                            <li>Keep your tires properly inflated to improve fuel efficiency by up to 3%.</li>
                            <li>Remove excess weight from your vehicle.</li>
                            <li>Consider carpooling or combining trips to reduce total mileage.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                elif vehicle_type == "Hybrid":
                    st.markdown("""
                    <div class="eco-tip" style="position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 0; right: 0; font-size: 80px; opacity: 0.05; transform: translate(20%, -30%);">♻️</div>
                        <h4 style="color: #81C784; margin-top: 0;">Hybrid Vehicle Tips</h4>
                        <ul style="padding-left: 20px;">
                            <li>Maximize electric-only driving in city conditions.</li>
                            <li>Use regenerative braking effectively by planning your stops.</li>
                            <li>Monitor your driving style with the vehicle's efficiency display.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                elif vehicle_type == "Electric":
                    st.markdown("""
                    <div class="eco-tip" style="position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 0; right: 0; font-size: 80px; opacity: 0.05; transform: translate(20%, -30%);">⚡</div>
                        <h4 style="color: #81C784; margin-top: 0;">Electric Vehicle Tips</h4>
                        <ul style="padding-left: 20px;">
                            <li>Charge during off-peak hours when the grid may use more renewable energy.</li>
                            <li>Consider installing solar panels to charge your vehicle.</li>
                            <li>Pre-heat or cool your car while plugged in to save battery for driving.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error calculating emissions: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Additional information
    st.markdown("""
    <div class="info-box">
        <h4>About Carbon Footprint Calculations</h4>
        <p>These calculations are based on average emission factors for different fuel types. The actual emissions
        may vary based on your specific vehicle, driving conditions, and fuel quality. For electric vehicles,
        emissions depend significantly on your local electricity grid's energy sources.</p>
    </div>
    """, unsafe_allow_html=True)
