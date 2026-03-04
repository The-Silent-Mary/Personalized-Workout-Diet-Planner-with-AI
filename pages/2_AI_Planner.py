import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Planner", page_icon="🥗", layout="wide")
st.title("🥗 AI Personalized Planner (Gemini AI)")

if "user_data" not in st.session_state:
    st.error("⚠️ Please fill in your details on the **Calculator** page first.")
    st.stop()

data = st.session_state["user_data"]

# Load API key from Streamlit secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ Gemini API key not found. Add it to your Streamlit secrets (see README).")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Show user summary
with st.expander("👤 Your Profile Summary", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎯 Goal",          data["goal"])
    c2.metric("🔥 Daily Calories", f"{data['tdee']} kcal")
    c3.metric("📏 BMI",            f"{data['bmi']} ({data['bmi_category']})")
    c4.metric("🥩 Protein Target", f"{data['protein_g']}g")

st.divider()

plan_type = st.radio(
    "What would you like to generate?",
    ["🍽️ Meal Plan Only", "🏋️ Workout Plan Only", "📋 Full Plan (Meal + Workout)"],
    horizontal=True
)

if st.button("✨ Generate My Plan", use_container_width=True):
    if "Meal" in plan_type and "Workout" in plan_type:
        content_request = """
        1. Full day meal plan (Breakfast, Lunch, Dinner, Snacks) with approximate calories per meal
        2. Weekly workout routine (Day-by-day, with sets and reps)
        3. Daily protein, carb, and fat targets
        4. Recovery and sleep advice
        5. Hydration recommendation
        """
    elif "Meal" in plan_type:
        content_request = """
        1. Full day meal plan (Breakfast, Lunch, Dinner, Snacks) with approximate calories per meal
        2. Daily protein, carb, and fat targets
        3. Meal prep tips
        """
    else:
        content_request = """
        1. Weekly workout routine (Day-by-day, with sets and reps)
        2. Warm-up and cool-down guidance
        3. Recovery and sleep advice
        4. Hydration recommendation
        """

    prompt = f"""
    Create a detailed, structured fitness plan for the following user.

    User Profile:
    - Gender: {data['gender']}
    - Age: {data['age']} years
    - Weight: {data['weight']} kg
    - Height: {data['height']} cm
    - Activity Level: {data['activity']}
    - Goal: {data['goal']}
    - Daily Calorie Target: {data['tdee']} kcal
    - BMI: {data['bmi']} ({data['bmi_category']})
    - Protein Target: {data['protein_g']}g | Fat Target: {data['fat_g']}g | Carb Target: {data['carb_g']}g

    Please include:
    {content_request}

    Format it clearly with headers and bullet points. Be specific and practical.
    """

    with st.spinner("🤖 Generating your personalized plan..."):
        try:
            response = model.generate_content(prompt)
            st.markdown("## 📋 Your Personalized Plan")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error generating plan: {e}")