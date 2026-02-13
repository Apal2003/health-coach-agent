# health-coach-agent
GenAI 4 GenZ Session 2 Challenge in AI Agents 

# 🏥 Personal Health Coach — AI Agent

A health monitoring agent that compresses medical history and wellness data, providing personalized recommendations with lower processing costs.


## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Step-by-Step Build Guide](#step-by-step-build-guide)
- [Core Features](#core-features)
- [Testing](#testing)
- [Submission Checklist](#submission-checklist)

---

## Project Overview

This project builds an **AI-powered health coaching agent** that:

1. Accepts a user's medical history and daily wellness data (sleep, steps, mood, meals)
2. **Compresses** that data using summarization to reduce token usage
3. Sends the compressed context to Claude for analysis
4. Returns **personalized health recommendations** (diet, exercise, sleep tips)

The key challenge is building efficient context compression so the agent can handle weeks/months of health data without hitting token limits or incurring high API costs.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| LLM API | Anthropic Claude (`claude-sonnet-4-5-20250929`) |
| Data Storage | JSON files (or SQLite for persistence) |
| Web Interface | Streamlit |
| Environment | `python-dotenv` |

---

## Project Structure

```
personal-health-coach/
├── main.py                       # Entry point
├── agent.py                      # Core agent logic
├── compressor.py                 # Health data compression module
├── recommender.py                # Recommendation generator
├── app.py                        # Streamlit web UI
├── data/
│   ├── sample_health_data.json   # Sample user data
│   └── user_profile.json         # User profile storage
├── prompts/
│   └── system_prompt.txt         # Agent system prompt
├── requirements.txt
├── .env                          # API keys (never commit this!)
└── README.md
```

---

## Step-by-Step Build Guide

### ✅ Step 1 — Setup Your Environment (Day 1)

**1a. Install dependencies**

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

# Install required packages
pip install anthropic python-dotenv streamlit
```

**1b. Create your `.env` file**

```env
ANTHROPIC_API_KEY=your_api_key_here
```

**1c. Create `.gitignore`** (important — never leak your API key)

```
.env
venv/
__pycache__/
*.pyc
data/temp_upload.json
```

**1d. Create `requirements.txt`**

```
anthropic>=0.25.0
python-dotenv>=1.0.0
streamlit>=1.30.0
```

---

### ✅ Step 2 — Define the Health Data Schema (Day 1)

Create `data/sample_health_data.json`:

```json
{
  "user_id": "user_001",
  "profile": {
    "age": 28,
    "weight_kg": 70,
    "height_cm": 175,
    "conditions": ["mild anxiety", "iron deficiency"],
    "goals": ["improve sleep", "increase energy"]
  },
  "daily_logs": [
    {
      "date": "2025-02-01",
      "sleep_hours": 6.5,
      "steps": 4200,
      "water_liters": 1.5,
      "mood": "tired",
      "meals": ["oatmeal", "coffee", "pizza", "chips"],
      "exercise": "none",
      "notes": "Felt sluggish all day"
    },
    {
      "date": "2025-02-02",
      "sleep_hours": 7.5,
      "steps": 8500,
      "water_liters": 2.2,
      "mood": "good",
      "meals": ["eggs", "salad", "grilled chicken", "fruit"],
      "exercise": "30 min walk",
      "notes": "Good energy today"
    }
  ]
}
```

---

### ✅ Step 3 — Build the Data Compressor (Day 2)

This is the **most important part** of the project. The compressor summarizes raw daily logs into a compact health snapshot, dramatically reducing token costs.

Create `compressor.py`:

```python
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def compress_health_data(health_data: dict) -> str:
    """
    Compresses weeks of daily health logs into a concise summary
    using Claude, dramatically reducing token usage in later calls.
    """
    raw_logs = json.dumps(health_data["daily_logs"], indent=2)
    profile = json.dumps(health_data["profile"], indent=2)

    compression_prompt = f"""
You are a medical data summarizer. Given the following raw daily health logs,
create a CONCISE but information-rich health summary (max 300 words).

Focus on:
- Average sleep, steps, hydration
- Notable patterns (e.g., low sleep correlates with bad mood)
- Nutrition quality trends
- Exercise consistency
- Any concerning patterns

User Profile:
{profile}

Daily Logs (last {len(health_data['daily_logs'])} days):
{raw_logs}

Output a compressed health snapshot only. No extra commentary.
"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=400,
        messages=[{"role": "user", "content": compression_prompt}]
    )

    return response.content[0].text
```

---

### ✅ Step 4 — Build the Recommendation Agent (Day 3)

Create `recommender.py`:

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are a compassionate, expert personal health coach with knowledge in nutrition,
fitness, sleep science, and mental wellness.

You receive a compressed health summary and provide:
1. Top 3 personalized health recommendations (specific and actionable)
2. One positive observation (what they are doing well)
3. One priority focus area for the next 7 days

Keep your tone warm, encouraging, and non-judgmental.
Recommendations must be realistic for everyday people.
"""

def get_recommendations(compressed_summary: str, user_question: str = None) -> str:
    """
    Takes a compressed health summary and returns personalized recommendations.
    """
    user_message = f"Here is my health summary:\n\n{compressed_summary}"

    if user_question:
        user_message += f"\n\nI also have a specific question: {user_question}"

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    return response.content[0].text
```

---

### ✅ Step 5 — Build the Main Agent Pipeline (Day 4)

Create `agent.py`:

```python
from compressor import compress_health_data
from recommender import get_recommendations
import json

def run_health_agent(data_path: str, user_question: str = None):
    """
    Main agent pipeline:
    1. Load health data
    2. Compress it (saves tokens!)
    3. Generate recommendations
    """
    print("Loading health data...")
    with open(data_path, "r") as f:
        health_data = json.load(f)

    print("Compressing health history...")
    compressed = compress_health_data(health_data)
    print(f"\n--- Compressed Summary ---\n{compressed}\n")

    print("Generating personalized recommendations...")
    recommendations = get_recommendations(compressed, user_question)
    print(f"\n--- Your Health Coach Says ---\n{recommendations}\n")

    # Measure token savings
    raw_chars = len(json.dumps(health_data["daily_logs"]))
    compressed_chars = len(compressed)
    savings = ((raw_chars - compressed_chars) / raw_chars) * 100
    print(f"Data compression: {savings:.1f}% reduction in size")

    return {
        "compressed_summary": compressed,
        "recommendations": recommendations,
        "compression_ratio": f"{savings:.1f}%"
    }
```

Create `main.py`:

```python
from agent import run_health_agent

if __name__ == "__main__":
    result = run_health_agent(
        data_path="data/sample_health_data.json",
        user_question="Why do I feel so tired even after sleeping 7 hours?"
    )
```

Run it:

```bash
python main.py
```

---

### ✅ Step 6 — Add a Web Interface (Day 5)

Create `app.py`:

```python
import streamlit as st
import json
import os
from agent import run_health_agent

st.set_page_config(page_title="Personal Health Coach", page_icon="🏥")
st.title("🏥 Personal Health Coach")
st.write("Upload your health data and get AI-powered personalized recommendations.")

uploaded_file = st.file_uploader("Upload health_data.json", type="json")
user_question = st.text_input(
    "Ask a specific question (optional)",
    placeholder="e.g., Why am I so tired after sleeping 7 hours?"
)

if uploaded_file and st.button("Get My Recommendations", type="primary"):
    health_data = json.load(uploaded_file)

    os.makedirs("data", exist_ok=True)
    with open("data/temp_upload.json", "w") as f:
        json.dump(health_data, f)

    with st.spinner("Analyzing your health data..."):
        result = run_health_agent("data/temp_upload.json", user_question or None)

    st.subheader("📊 Compressed Health Summary")
    st.info(result["compressed_summary"])

    st.subheader("💡 Your Personalized Recommendations")
    st.success(result["recommendations"])

    st.caption(f"Data compression achieved: {result['compression_ratio']} reduction")
```

Run the web app:

```bash
streamlit run app.py
```

---

### ✅ Step 7 — Test & Submit (Days 6–7)

**Test different user scenarios:**

```bash
# Test with different health profiles by editing sample_health_data.json

# Scenario 1: Poor sleep user
# Set sleep_hours to 4-5 for all days

# Scenario 2: Sedentary user
# Set steps to under 2000, exercise to "none"

# Scenario 3: Great health habits
# Set 8hr sleep, 10k steps, healthy meals
```

**Verify token savings are significant (aim for >50% reduction)**

**Final checks before submission:**

```bash
# Make sure .env is not tracked
git status    # .env should NOT appear

# Run a clean test
python main.py
```

---

## Core Features

- **Data Compression** — Summarizes weeks of health logs into ~300-word snapshots (60–80% token reduction)
- **Personalized Recommendations** — Tailored advice based on individual health profile and patterns
- **Pattern Recognition** — Identifies correlations like low sleep correlating with poor mood and bad diet
- **Q&A Support** — Users can ask specific follow-up health questions
- **Web UI** — Streamlit interface for non-technical users

---

## Testing

```bash
# Run the command-line agent
python main.py

# Run the web interface
streamlit run app.py

# Quick test with a custom question
python -c "
from agent import run_health_agent
run_health_agent('data/sample_health_data.json', 'How can I improve my energy?')
"
```

**Expected output:**

```
Loading health data...
Compressing health history...

--- Compressed Summary ---
[200–300 word health snapshot...]

Generating personalized recommendations...

--- Your Health Coach Says ---
[3 actionable recommendations + positive note + weekly focus...]

Data compression: 65.3% reduction in size
```

---

## Submission Checklist

- [ ] Agent loads and processes health data correctly
- [ ] Compression reduces token/data size by more than 50%
- [ ] Recommendations are personalized (not generic)
- [ ] Code is clean and well-commented
- [ ] `.env` is in `.gitignore` and NOT committed
- [ ] `sample_health_data.json` is included for reviewers to test
- [ ] README is complete with setup instructions
- [ ] (Bonus) Streamlit app runs without errors

---

## 💡 Bonus Ideas to Stand Out

- Add **trend detection** — "Your sleep has improved 3 days in a row!"
- Support **multi-week compression** by chaining weekly summaries
- Add a **health score** (0–100) based on averages
- Flag **nutritional gaps** from meal data
- Build **weekly check-in reminders** using a scheduler

---

## License

MIT License — Free to use and modify for learning purposes.
