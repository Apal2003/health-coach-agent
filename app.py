import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from health_agent import HealthCoachAgent
from compression import HealthDataCompressor
import json

# Initialize
if 'medical_history' not in st.session_state:
    st.session_state.medical_history = {
        'conditions': [],
        'medications': [],
        'allergies': []
    }

if 'wellness_data' not in st.session_state:
    st.session_state.wellness_data = []

st.title("🏥 Personal Health Coach Agent")
st.caption("AI-powered health monitoring with efficient data processing")

# Sidebar - Medical History
with st.sidebar:
    st.header("📋 Medical Profile")
    
    conditions = st.text_area("Medical Conditions (one per line)")
    medications = st.text_area("Current Medications (one per line)")
    allergies = st.text_area("Allergies (one per line)")
    
    if st.button("Save Medical Profile"):
        st.session_state.medical_history = {
            'conditions': [c.strip() for c in conditions.split('\n') if c.strip()],
            'medications': [m.strip() for m in medications.split('\n') if m.strip()],
            'allergies': [a.strip() for a in allergies.split('\n') if a.strip()]
        }
        st.success("Profile saved!")

# Main area - Daily Wellness Tracking
st.header("📊 Daily Wellness Log")

col1, col2 = st.columns(2)

with col1:
    sleep_hours = st.number_input("Sleep (hours)", 0.0, 24.0, 7.0, 0.5)
    exercise_mins = st.number_input("Exercise (minutes)", 0, 300, 30, 5)
    water_ml = st.number_input("Water intake (ml)", 0, 5000, 2000, 100)

with col2:
    stress_level = st.slider("Stress Level", 1, 10, 5)
    mood = st.selectbox("Mood", ["Great", "Good", "Okay", "Low", "Poor"])
    notes = st.text_input("Notes")

if st.button("Log Today's Data"):
    entry = {
        'date': datetime.now().isoformat(),
        'sleep_hours': sleep_hours,
        'exercise_minutes': exercise_mins,
        'water_intake_ml': water_ml,
        'stress_level': stress_level,
        'mood': mood,
        'notes': notes
    }
    st.session_state.wellness_data.append(entry)
    st.success("Data logged!")

# Display recent entries
if st.session_state.wellness_data:
    st.subheader("Recent Entries")
    df = pd.DataFrame(st.session_state.wellness_data[-7:])
    st.dataframe(df)

# Get AI Recommendations
st.header("🤖 AI Health Coach")

user_question = st.text_input("Ask your health coach anything:", 
                               placeholder="e.g., How can I improve my sleep?")

if st.button("Get Recommendations"):
    if not st.session_state.wellness_data:
        st.warning("Please log some wellness data first!")
    else:
        with st.spinner("Analyzing your health data..."):
            # Compress and summarize data
            compressor = HealthDataCompressor()
            summary = compressor.summarize_for_ai(
                st.session_state.medical_history,
                st.session_state.wellness_data
            )
            
            # Get AI recommendations
            agent = HealthCoachAgent()
            recommendations = agent.get_recommendations(summary, user_question)
            
            st.success("Recommendations:")
            st.write(recommendations)
            
            # Show trends
            trends = agent.analyze_trends(st.session_state.wellness_data)
            st.subheader("📈 Trends")
            col1, col2, col3 = st.columns(3)
            col1.metric("Sleep", trends.get('sleep_trend', 'N/A'))
            col2.metric("Exercise", trends.get('exercise_trend', 'N/A'))
            col3.metric("Stress", trends.get('stress_trend', 'N/A'))

# Export data
if st.session_state.wellness_data:
    st.download_button(
        "📥 Export Data",
        data=json.dumps({
            'medical_history': st.session_state.medical_history,
            'wellness_data': st.session_state.wellness_data
        }, indent=2),
        file_name=f"health_data_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )


