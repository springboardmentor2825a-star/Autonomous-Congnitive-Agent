import streamlit as st
import requests
import json

st.set_page_config(page_title="Autonomous Engine", layout="wide")
BACKEND_URL = "http://localhost:8000"

st.title("🧠 Autonomous Cognitive Engine")

if "messages" not in st.session_state:
    st.session_state.messages = []

goal = st.text_input("High-level goal:")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Execute"):
        if goal:
            with st.spinner("Agent working..."):
                response = requests.post(f"{BACKEND_URL}/execute", json={"goal": goal})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.messages.append({"role": "user", "content": goal})
                    st.session_state.messages.append({"role": "assistant", "content": data["output"], "conf": data["confidence"], "escalate": data["escalate"]})
                else:
                    st.error("Backend error")

with col2:
    if st.button("👤 Escalate to Human"):
        st.info("Escalated! Review agent output.")

# Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "conf" in msg:
            st.metric("Confidence", f"{msg['conf']:.2f}")
            if msg["escalate"]:
                st.warning("Low confidence - Human review recommended")

# Memory
with st.sidebar:
    st.subheader("Recent Memory")
    # Fetch memory via API or session; simplified here
    st.info("Memory persists in backend.")
