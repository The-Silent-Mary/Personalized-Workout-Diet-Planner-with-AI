import streamlit as st

st.set_page_config(page_title="Calculator", page_icon="📊", layout="wide")
st.title("📊 Personal Metrics Calculator")

with st.form("metrics_form"):
    col1, col2 = st.columns(2)

    with col1:
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        height = st.number_input("Height (cm)", min_value=120, max_value=230, value=170)
        age    = st.number_input("Age", min_value=15, max_value=80, value=25)

    with col2:
        gender   = st.selectbox("Gender", ["Male", "Female"])
        activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Very Active"])
        goal     = st.selectbox("Goal", ["Lose Weight", "Maintain", "Build Muscle"])

    submitted = st.form_submit_button("Calculate", use_container_width=True)

if submitted:
    # BMR — Mifflin-St Jeor
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    multipliers = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Very Active": 1.725}
    tdee = bmr * multipliers[activity]

    # Calorie target
    if goal == "Lose Weight":
        target_cal = tdee - 400
    elif goal == "Build Muscle":
        target_cal = tdee + 300
    else:
        target_cal = tdee

    # BMI
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        bmi_category = "Underweight"
    elif bmi < 25:
        bmi_category = "Normal weight"
    elif bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"

    # Macros (approximate)
    protein_g = round(weight * 2.0)          # 2g per kg
    fat_g     = round(target_cal * 0.25 / 9) # 25% of calories from fat
    carb_g    = round((target_cal - protein_g * 4 - fat_g * 9) / 4)

    # Save to session
    st.session_state["user_data"] = {
        "weight": weight, "height": height, "age": age,
        "gender": gender, "activity": activity, "goal": goal,
        "bmr": round(bmr), "tdee": round(target_cal),
        "bmi": round(bmi, 1), "bmi_category": bmi_category,
        "protein_g": protein_g, "fat_g": fat_g, "carb_g": carb_g,
    }

    st.success("✅ Data saved! Head to **AI Planner** in the sidebar.")
    st.divider()

    # Results
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Daily Calories", f"{round(target_cal)} kcal")
    c2.metric("⚡ BMR",            f"{round(bmr)} kcal")
    c3.metric("📏 BMI",            f"{round(bmi, 1)}")
    c4.metric("🏷️ BMI Category",   bmi_category)

    st.divider()
    st.subheader("🍽️ Recommended Macros")
    m1, m2, m3 = st.columns(3)
    m1.metric("🥩 Protein", f"{protein_g}g / day")
    m2.metric("🫙 Fats",    f"{fat_g}g / day")
    m3.metric("🌾 Carbs",   f"{carb_g}g / day")
