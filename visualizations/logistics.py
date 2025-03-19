from geopy.distance import geodesic
import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import openrouteservice
from openrouteservice import convert

# Initialize ORS client
ORS_API_KEY = '5b3ce3597851110001cf6248afd4bb63fe3a470bb0061a1ac1d8a410'  # Replace with your ORS API key
client = openrouteservice.Client(key=ORS_API_KEY)

def get_coordinates(place):
    geolocator = Nominatim(user_agent="logistics_emission", timeout=10)
    location = geolocator.geocode(place)
    if location:
        return (location.latitude, location.longitude)
    return None

def calculate_distance_via_ors(origin, destination, profile):
    coords_origin = get_coordinates(origin)
    coords_dest = get_coordinates(destination)
    if coords_origin and coords_dest:
        coordinates = [coords_origin[::-1], coords_dest[::-1]]  # ORS expects (lon, lat)
        try:
            routes = client.directions(coordinates=coordinates, profile=profile)
            distance_m = routes['routes'][0]['summary']['distance']
            return round(distance_m / 1000, 2)  # Convert meters to kilometers
        except Exception as e:
            st.error(f"Error fetching data from ORS: {e}")
            return None
    else:
        st.error("Could not geocode the provided locations.")
        return None
    
# Constants
EMISSION_FACTOR = 1.58  # Emission factor per km per kg

# Transport modes and efficiency
TRANSPORT_MODES = {
    "Truck": {"profile": "driving-car", "preference": 'shortest', "efficiency": 1.9},  # Baseline
    "Rail": {"profile": "cycling-regular","preference": 'shortest', "efficiency": 0.6},  # More efficient
    # ORS doesn't support air routes; using geodesic distance as a proxy
    "Air": {"profile": None,"preference": 'shortest', "efficiency": 3.0}  # Less efficient
}

def  logist_vis():
# Streamlit UI
    st.title("📦 Logistics Emission Calculator")
    st.subheader("Auto-compute CO₂ emissions based on real-world distances")

# User Inputs
    material = st.selectbox("Select Material", ["Steel", "Wood", "Plastic", "Concrete"])
    transport_mode = st.radio("Select Transport Mode", list(TRANSPORT_MODES.keys()))
    origin = st.text_input("Enter Origin City", "Delhi")
    destination = st.text_input("Enter Destination City", "Mumbai")
    weight = st.number_input("Enter Material Weight (kg)", min_value=1, value=1000)

# Compute Distance
    if origin and destination:
        if transport_mode == "Air":
            # Use geodesic distance for air travel
            coords_origin = get_coordinates(origin)
            coords_dest = get_coordinates(destination)
            if coords_origin and coords_dest:
                distance = round(geodesic(coords_origin, coords_dest).km, 2)
            else:
                distance = None
        else:
            profile = TRANSPORT_MODES[transport_mode]["profile"]
            distance = calculate_distance_via_ors(origin, destination, profile)

        if distance:
            st.write(f"🚗 Estimated Distance: **{distance} km**")
        else:
            st.error("Could not calculate distance. Check city names.")
    else:
        st.warning("Please enter valid origin and destination.")

# Compute Emission
    if distance:
        efficiency_factor = TRANSPORT_MODES[transport_mode]["efficiency"]
        total_emission = round(distance * weight * EMISSION_FACTOR * efficiency_factor, 2)

    # Display Metrics
        st.metric(label="Total CO₂ Emission (kg)", value=total_emission)

        # Dataframe for comparison
        data = pd.DataFrame({
            "Transport Mode": list(TRANSPORT_MODES.keys()),
            "Emission (kg CO₂)": [
                round(distance * weight * EMISSION_FACTOR * TRANSPORT_MODES[mode]["efficiency"], 2)
                for mode in TRANSPORT_MODES.keys()
             ]
            })

    # Bar Chart
    st.subheader("Emission Comparison by Transport Mode")
    fig = px.bar(data, x="Transport Mode", y="Emission (kg CO₂)", color="Transport Mode", text="Emission (kg CO₂)")
    st.plotly_chart(fig, use_container_width=True)

    # Conclusion
    st.success(f"Transporting {weight} kg of {material} from {origin} to {destination} via {transport_mode} emits **{total_emission} kg CO₂**.")

