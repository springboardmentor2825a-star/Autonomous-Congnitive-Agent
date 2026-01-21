import streamlit as st
import requests

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Autonomous Cognitive Engine",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Autonomous Cognitive Engine")
st.caption("Deep Research & Long-Horizon Tasks")

st.divider()

# -------------------------------
# USER INPUT
# -------------------------------
goal = st.text_area(
    "🎯 Enter your research goal",
    placeholder="Example: Research autonomous AI agent failure modes",
    height=120
)

run_button = st.button("🚀 Start Research")

# -------------------------------
# BACKEND CONFIG
# -------------------------------
API_URL = "http://127.0.0.1:8000/api/research/"

# -------------------------------
# RUN AGENT
# -------------------------------
if run_button:
    if not goal.strip():
        st.error("Please enter a goal.")
        st.stop()

    st.success("Research started…")
    with st.spinner("Agents are thinking…"):
        try:
            response = requests.post(
                API_URL,
                json={"goal": goal},
                timeout=600
            )
        except Exception as e:
            st.error(f"Backend connection error: {e}")
            st.stop()

    if response.status_code != 200:
        st.error(f"Backend error: {response.text}")
        st.stop()

    data = response.json()

    st.divider()

    # -------------------------------
    # CRITICAL FIX: SHOW FULL OUTPUT
    # -------------------------------
    st.subheader("🧠 Execution Output (All Agents)")

    # Case 1: Backend returns logs (list)
    if isinstance(data, dict) and "logs" in data:
        for log in data["logs"]:
            st.write(log)

    # Case 2: Backend returns plain output text
    elif isinstance(data, dict) and "output" in data:
        st.text(data["output"])

    # Case 3: Backend returns structured JSON
    else:
        # Show EVERYTHING exactly like Postman
        st.json(data)

    st.success("✅ Research completed successfully")
