import streamlit as st 
import requests

FAST_API = "http://0.0.0.0:8000"

st.title("OmniSnapAI")
if st.button("movie"):
    requests.post(f"{FAST_API}/movie")
