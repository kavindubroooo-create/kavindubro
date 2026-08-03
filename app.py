import pandas as pd
import re
import requests
import streamlit as st

st.set_page_config(
    page_title="Facebook Numeric ID Extractor", page_icon="🎯", layout="wide"
)

# Advanced Cyberpunk UI Styling
st.markdown(
    """
    <style>
    .stApp {
        background: #090a0f;
        color: #00ffcc;
        font-family: 'Courier New', monospace;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00ffcc;
        text-shadow: 0 0 10px rgba(0,255,204,0.5);
        text-align: center;
        margin-bottom: 20px;
    }
    .stTextArea textarea {
        background-color: #12151c !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc !important;
        border-radius: 8px;
    }
    .stButton button {
        background: linear-gradient(45deg, #00ffcc, #0077ff);
        color: #090a0f;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        width: 100%;
        padding: 10px;
    }
    .metric-card {
        background: #12151c;
        border: 1px solid #00ffcc;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-header">[🎯] FACEBOOK NUMERIC ID EXTRACTOR</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
  st.text(">>> INPUT FACEBOOK SHARE / PROFILE LINKS (ONE PER LINE):")
  links_input = st.text_area(
      "", height=150, placeholder="https://www.facebook.com/share/..."
  )

with col2:
  st.markdown("### SYSTEM STATS")
  st.markdown(
      """
    <div class="metric-card">
        <p style="margin:0; font-size:14px; color:#888;">STATUS</p>
        <h3 style="margin:0; color:#00ffcc;">READY</h3>
    </div>
    """,
      unsafe_allow_html=True,
  )

if st.button("EXTRACT NUMERIC IDS"):
  if links_input.strip():
    links = [l.strip() for l in links_input.split("\n") if l.strip()]
    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS"
            " X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0"
            " Mobile/15E148 Safari/604.1"
        )
    }

    for idx, link in enumerate(links):
      status_text.text(f"Processing target {idx+1} of {len(links)}...")
      numeric_id = "Not Found"
      real_url = link

      try:
        response = requests.get(
            link, headers=headers, allow_redirects=True, timeout=8
        )
        real_url = response.url
        html_content = response.text

        # 1. Check URL for id= parameter
        match_id = re.search(r"[?&]id=(\d+)", real_url)
        if match_id:
          numeric_id = match_id.group(1)
        else:
          # 2. Search HTML for mobile app schema links (e.g., fb://profile/...)
          fb_app_match = re.search(
              r"fb://(?:profile|page)/(\d+)", html_content
          )
          if fb_app_match:
            numeric_id = fb_app_match.group(1)
          else:
            # 3. Search HTML for user_id, profile_id, or entity_id patterns
            patterns = [
                r'"user_id"\s*:\s*"(\d+)"',
                r'"profile_id"\s*:\s*"(\d+)"',
                r'"entity_id"\s*:\s*"(\d+)"',
                r"user_id=(\d+)",
                r"profile\.php\?id=(\d+)",
                r'"owner_id"\s*:\s*"(\d+)"',
                r'actor_id["\s:]+"(\d+)"',
            ]
            for pat in patterns:
              m = re.search(pat, html_content)
              if m:
                numeric_id = m.group(1)
                break
      except Exception as e:
        real_url = f"Error: {str(e)}"
        numeric_id = "Failed"

      results.append({
          "Index": idx + 1,
          "Original Link": link,
          "Real URL": real_url,
          "Facebook Numeric ID": numeric_id,
      })
      progress_bar.progress((idx + 1) / len(links))

    progress_bar.empty()
    status_text.empty()

    st.success(">>> EXTRACTION COMPLETED!")

    st.markdown("### RESULTS DASHBOARD")
    st.dataframe(results, use_container_width=True)

    df = pd.DataFrame(results)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="DOWNLOAD RESULTS AS CSV",
        data=csv,
        file_name="facebook_numeric_ids.csv",
        mime="text/csv",
    )
  else:
    st.warning("Please enter at least one URL.")