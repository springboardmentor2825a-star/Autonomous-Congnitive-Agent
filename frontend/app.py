import streamlit as st
import requests

st.set_page_config(page_title="Deep Research Cognitive Engine", layout="centered")

st.title("🔬 Autonomous Cognitive Engine for Deep Research")

goal = st.text_input("Enter a long-horizon research goal:")

if st.button("Run Research Agent"):
    if goal.strip():
        response = requests.post(
            "http://localhost:8000/research/run",
            json={"goal": goal}
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Perception")
            st.write(data["perception"])

            st.subheader("Research Plan")
            for step in data["plan"]:
                st.write("•", step)

            st.subheader("Execution Trace")
            for trace in data["execution_trace"]:
                st.write(trace)

            st.subheader("Long-Term Memory")
            st.write(data["long_term_memory"])
        else:
            st.error("Backend error")
    else:
        st.warning("Please enter a research goal")

