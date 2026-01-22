import streamlit as st
import requests

st.title("Autonomous Cognitive Engine")

goal = st.text_input("Enter your goal")

if st.button("Run"):
    res = requests.post(
        "http://127.0.0.1:8000/run",
        json={"goal": goal}
    )
    st.json(res.json())
