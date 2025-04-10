import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
from streamlit_lottie import st_lottie
import requests

# Load Animation from URL
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

# -- Load Model --
model_file_path = "app/Emission_tracer (2).sav"
try:
    with open(model_file_path, "rb") as f:
        loaded_model = pickle.load(f)
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# -- Prediction Function --
def predict_emission(features):
    input_array = np.array(features).reshape(1, -1)
    prediction = loaded_model.predict(input_array)
    return prediction[0]

# -- Eco Tip --
def get_eco_tip(emission):
    if emission > 800:
        return "🚫 Try using public transport or switching to electric!"
    elif emission > 500:
        return "⚠️ Consider reducing fuel usage and track electricity use."
    else:
        return "✅ Great job! You're being eco-conscious! 🌍"

# -- Save Emission Record --
def save_emission_to_csv(data):
    file_path = "emission_history.csv"
    df = pd.DataFrame([data])
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

# -- Load Emission History --
def load_emission_history():
    file_path = "emission_history.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # Return empty DataFrame with same structure
        return pd.DataFrame(columns=["Electricity", "Vehicle", "Fuel", "Liters", "Distance", "CO2 Emission"])


# ---------- Main App ----------
def main():
    st.set_page_config(page_title="CarbonIQ", layout="wide")
    st.title("🌱CarbonIQ")
    st.markdown("""
    Welcome to **CarbonIQ** – your smart CO₂ tracking companion.  
    Our mission: **Make the Earth cleaner, smarter, and greener.** 🌍
    ---
    """)
    st.markdown("""
        <style>
        div[class*="stTabs"] button {
            font-size: 18px !important;
            font-weight: bold !important;
            color: #4CAF50 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    plant_anim = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_4kx2q32n.json")

    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔍 Emission Calculator", "📊 Emission History", "💡 Eco Tips"])

    # ---------------- Tab 1: Home ----------------
    with tab1:
        st.image("app/assets/pexels-fatih-turan-63325184-9835979.jpg", width=2000)

        st.header("📌 Key Features of CarbonIQ", divider="green")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("🔍 Real-Time Emission Calculator")
            st.write("Predict CO₂ emissions from your electricity and vehicle usage.🌱")

        with col2:
            st.markdown("#### 📈 Track Your History")
            st.write("Monitor and reflect on your carbon emissions over time. 📊🌍")

        with col3:
            st.markdown("#### 💡 Get Eco-Friendly Tips")
            st.write("Receive personalized suggestions to reduce your carbon footprint. 🌱🌎")

        st.markdown("---")
        st.subheader("🌱 Ready to take action?")
        st.markdown("Click on the **Emission Calculator** tab to begin!")

    # ---------------- Tab 2: Calculator ----------------


    with tab2:
         st.header("🔍 CO₂ Emission Calculator")

    electricity_kwh = st.number_input("🔌 Electricity Used (kWh)", min_value=0.0)

    vehicle_type_dict = {"Car": 1, "Bus": 2, "Bike": 3, "Truck": 4}
    fuel_type_dict = {"Diesel": 0, "EV": 1, "CNG": 2, "Petrol": 3}
    emission_place = {"Mixed": 0, "Electricity": 1}

    vehicle_name = st.selectbox("🚗 Vehicle Type", list(vehicle_type_dict.keys()))
    fuel_name = st.selectbox("⛽ Fuel Type", list(fuel_type_dict.keys()))
    fuel_liters = st.number_input("🛢️ Fuel Used (liters)", min_value=0.0)
    distance_km = st.number_input("🛣️ Distance Traveled (km)", min_value=0.0)
    emission_type = st.selectbox("🏭 Emission Source", list(emission_place.keys()))

    vehicle_type = vehicle_type_dict[vehicle_name]
    fuel_type = fuel_type_dict[fuel_name]
    emission_source = emission_place[emission_type]

    if st.button("🌿 Calculate CO₂ Emission"):
        features = [electricity_kwh, vehicle_type, fuel_type, fuel_liters, distance_km, emission_source]
        prediction = predict_emission(features)

        prediction_kg = prediction   # 🔥 Convert grams → kilograms

        save_emission_to_csv({
            "Electricity (kWh)": electricity_kwh,
            "Vehicle": vehicle_name,
            "Fuel": fuel_name,
            "Fuel Used (liters)": fuel_liters,
            "Distance (km)": distance_km,
            "CO2 Emission (kg)": prediction_kg
        })

        st.success(f"🌍 Estimated CO₂ Emission: **{prediction_kg:.2f} kg**")
        st.info(get_eco_tip(prediction))


    # ---------------- Tab 3: History ----------------
    with tab3:
        st.header("📊 Emission Dashboard")
        df = load_emission_history()

        if df.empty:
            st.warning("No records found. Try making a prediction first.")
        else:
            st.dataframe(df.tail(10), use_container_width=True)

            fuel_filter = st.multiselect("Filter by Fuel Type", df["Fuel"].unique(), default=df["Fuel"].unique())
            filtered_df = df[df["Fuel"].isin(fuel_filter)]

            st.subheader("📉 CO₂ Emission Trend")
            st.line_chart(filtered_df["co2_emissions_kg"])


            st.subheader("📊 CO₂ by Fuel")
            fuel_summary = filtered_df.groupby("Fuel")["CO2 Emission (g)"].sum()
            st.bar_chart(fuel_summary)

    # ---------------- Tab 4: Tips ----------------
    with tab4:
        st.header("💡 Eco-Friendly Habits")
        if plant_anim:
            st_lottie(plant_anim, height=180, key="eco_tips_anim")
        st.markdown("""
        ### 🌱 Tips to Lower Your Carbon Footprint:
        - 💡 Use energy-efficient appliances  
        - 🚌 Opt for public transport or carpool  
        - 🔌 Unplug devices when not in use  
        - 🥦 Try meatless meals once a week  
        - 🚲 Use a bicycle or walk for nearby travel  
        - 🏡 Insulate your home to save energy  
        - ♻️ Reduce, Reuse, Recycle whenever possible  
        """)


if __name__ == "__main__":
    main()
