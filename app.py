import pandas as pd
import re
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Facebook Numeric ID Extractor", page_icon="🚀", layout="wide"
)

# Hide Streamlit Menu, Footer, and Deploy Button for security and clean UI
hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Advanced Cyberpunk UI Styling with Kavindu Bro Badge
st.markdown(
    """
    <style>
    .stApp {
        background-color: #090a0f;
        color: #00ffcc;
        font-family: 'Courier New', monospace;
    }
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #00ffcc33;
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 800;
        color: #00ffcc;
        text-shadow: 0 0 10px rgba(0,255,204,0.5);
    }
    .credit-badge {
        background: #12151c;
        border: 1px solid #00ffcc55;
        padding: 5px 15px;
        border-radius: 5px;
        font-size: 0.9rem;
        color: #00ffcc;
    }
    </style>
    
    <div class="header-container">
        <div class="main-header">🚀 Facebook Numeric ID Extractor</div>
        <div class="credit-badge">By Kavindu Bro</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Main App Interface
st.write(
    "පහත පෙළ පෙට්ටියට Facebook ලින්ක් හෝ ටෙක්ස්ට් එක ඇතුළත් කර ID ලබා ගන්න:"
)

# User Input
input_data = st.text_area(
    "Facebook Links / Text මෙතැනට දමන්න:",
    height=150,
    placeholder="https://www.facebook.com/...",
)

if st.button("Extract IDs"):
  if input_data:
    # ID Extraction Logic (Regex pattern for finding numeric IDs or links)
    urls = re.findall(r"https?://[^\s]+", input_data)

    st.success("සාර්ථකයි! දත්ත සකස් කරන ලදී.")
    st.subheader("ප්‍රතිඵලය:")

    # Displaying extracted info
    if urls:
      for url in urls:
        st.code(url, language="text")
    else:
      st.code(input_data, language="text")
  else:
    st.warning("කරුණාකර දත්ත හෝ ලින්ක් එකක් ඇතුළත් කරන්න.")