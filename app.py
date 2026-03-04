import streamlit as st

st.set_page_config(
    page_title="AI Fitness Hub",
    layout="wide",
    page_icon="💪"
)

st.title("💪 AI Fitness Pro")
st.subheader("Your AI-Powered Health & Nutrition Companion")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### What this app does:
    - 📊 Calculates your BMR, TDEE & BMI
    - 🥗 Generates AI-powered meal plans
    - 🏋️ Creates personalized workout routines
    - 💧 Gives hydration & recovery advice
    """)
    if st.button("Get Started →"):
        st.success("Use the sidebar to navigate to the **Calculator** page first!")

with col2:
    st.info(
        "💡 **BMR** — Calories your body burns at complete rest.\n\n"
        "**TDEE** — BMR adjusted for your daily activity level.\n\n"
        "**BMI** — Body Mass Index, a measure of body fat based on height & weight."
    )

st.divider()

st.image(
    "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&q=80&w=1000",
    caption="Consistency is Key",
    use_container_width=True
)