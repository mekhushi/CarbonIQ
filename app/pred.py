import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie

# ---------- Utility Functions ----------
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def predict_emission(features):
    # Placeholder prediction logic
    return sum(features) * 10

def save_emission_to_csv(record):
    df = pd.DataFrame([record])
    try:
        existing = pd.read_csv("emission_history.csv")
        df = pd.concat([existing, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv("emission_history.csv", index=False)

def load_emission_history():
    try:
        return pd.read_csv("emission_history.csv")
    except FileNotFoundError:
        return pd.DataFrame()

def get_eco_tip(prediction):
    if prediction < 100:
        return "You're doing great! Keep it up 🌿"
    elif prediction < 300:
        return "Nice! Try using more public transport 🚍"
    else:
        return "Consider reducing your electricity or fuel use 💡"

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

    plant_anim = load_lottie_url("https://assets6.lottiefiles.com/packages/lf20_4kx2q32n.json")

    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔍 Emission Calculator", "📊 Emission History", "💡 Eco Tips"])

    # ---------------- Tab 1: Home ----------------
    with tab1:
       
        st.image(r"C:\Users\Khushi Singh\Downloads\pexels-fatih-turan-63325184-9835979.jpg", width=2000)
        image_path = r"C:\Users\Khushi Singh\Downloads\pexels-fatih-turan-63325184-9835979.jpg"

    
        st.header("📌 Key Features of CarbonIQ" , divider = "green")
       
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("🔍 Real-Time Emission Calculator")
            st.write("Predict CO₂ emissions from your electricity and vehicle usage.🌱")

        with col2:
           
            st.markdown("#### 📈 Track Your History")
            st.write("See your past emission records and proThe Track Your History feature in CarbonIQ allows you to monitor and reflect on your carbon emissions over time.  📊🌍.")


        with col3:
           
            st.markdown("#### 💡 Get Eco-Friendly Tips")
            st.write("Get personalized tips to lower your carbon footprint.CarbonIQ not only helps you track emissions but also guides you with eco-friendly tips tailored to your lifestyle. These tips are designed to help you adopt sustainable habits in your daily routine—be it at home, work, or while commuting  🌱🌎")

        st.markdown("---")
        st.subheader("🌱 Ready to take action?")
        st.markdown("Click on the **Emission Calculator** tab to begin!")

    # ---------------- Tab 2: Calculator ----------------
    with tab2:
        st.header("🔍 CO₂ Emission Calculator")

        electricity_kwh = st.number_input("🔌 Electricity Used (kWh)", min_value=0.0, format="%.2f")

        vehicle_type_dict = {"Car": 1, "Bus": 2, "Bike": 3, "Truck": 4}
        fuel_type_dict = {"Diesel": 0, "EV": 1, "CNG": 2, "Petrol": 3}
        emission_place = {"Mixed": 0, "Electricity": 1}

        vehicle_name = st.selectbox("🚗 Vehicle Type", list(vehicle_type_dict.keys()))
        fuel_name = st.selectbox("⛽ Fuel Type", list(fuel_type_dict.keys()))
        fuel_liters = st.number_input("🛢️ Fuel Used (liters)", min_value=0.0, format="%.2f")
        distance_km = st.number_input("🛣️ Distance Traveled (km)", min_value=0.0, format="%.2f")
        emission_type = st.selectbox("🏭 Emission Source", list(emission_place.keys()))

        vehicle_type = vehicle_type_dict[vehicle_name]
        fuel_type = fuel_type_dict[fuel_name]
        emission_source = emission_place[emission_type]

        if st.button("🌿 Calculate CO₂ Emission"):
            features = [electricity_kwh, vehicle_type, fuel_type, fuel_liters, distance_km, 0.0]
            prediction = predict_emission(features)

            save_emission_to_csv({
                "Electricity": electricity_kwh,
                "Vehicle": vehicle_name,
                "Fuel": fuel_name,
                "Liters": fuel_liters,
                "Distance": distance_km,
                "CO2 Emission (g)": prediction
            })

            st.success(f"🌍 Estimated CO₂ Emission: **{prediction:.2f} grams**")
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
            st.line_chart(filtered_df["CO2 Emission (g)"])

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
