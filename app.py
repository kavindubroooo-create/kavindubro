import re
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Facebook Numeric ID Extractor Pro",
    page_icon="🚀",
    layout="wide",
)

# Hide Streamlit Menu, Footer, Deploy Button, and Header for clean UI
hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Advanced Professional Cyberpunk UI Styling with Kavindu Bro Badge
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
        <div class="main-header">🚀 Facebook Numeric ID Extractor Pro</div>
        <div class="credit-badge">By Kavindu Bro</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Main App Interface
st.write(
    "Paste your mixed bulk Facebook links (Original, Lite, Share/Short links)"
    " below to extract all Numeric IDs at once:"
)

# User Input for Bulk Data
input_data = st.text_area(
    "Facebook Links / Bulk Text:",
    height=150,
    placeholder=(
        "Paste mixed links here (e.g., https://www.facebook.com/share/... or"
        " lite links)..."
    ),
)


def extract_numeric_id(link):
  link = link.strip()
  if not link.startswith("http"):
    link = "https://" + link

  # 1. Check direct profile.php?id=
  match = re.search(r"profile\.php\?id=(\d+)", link)
  if match:
    return match.group(1)

  # 2. Check direct numeric path in URL
  match_num = re.search(r"facebook\.com/([0-9]{5,})", link)
  if match_num:
    return match_num.group(1)

  # 3. Resolve share/short/lite links using requests and redirects
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0"
            " Mobile/15E148 Safari/604.1"
        )
    }
    res = requests.get(link, headers=headers, allow_redirects=True, timeout=4)
    final_url = res.url

    # Check profile.php?id in final redirected URL
    match = re.search(r"profile\.php\?id=(\d+)", final_url)
    if match:
      return match.group(1)

    match_num = re.search(r"facebook\.com/([0-9]{5,})", final_url)
    if match_num:
      return match_num.group(1)

    # Search page HTML content for user/actor/entity IDs
    html = res.text
    uid_match = re.search(
        r'"userID"\s*:\s*"(\d+)"|"entity_id"\s*:\s*"(\d+)"|"actor_id"\s*:\s*"(\d+)"',
        html,
    )
    if uid_match:
      return uid_match.group(1) or uid_match.group(2) or uid_match.group(3)

  except:
    pass

  # Fallback: if it's already an ID or couldn't be resolved, return as is
  return link


if st.button("Extract All IDs"):
  if input_data:
    # Find all URLs from the text
    urls = re.findall(r"https?://[^\s]+|www\.[^\s]+", input_data)
    if not urls:
      urls = [line.strip() for line in input_data.splitlines() if line.strip()]

    extracted_ids = []
    for u in urls:
      eid = extract_numeric_id(u)
      if eid:
        extracted_ids.append(eid)

    if extracted_ids:
      # Combine all extracted IDs into a single bulk text block
      bulk_result = "\n".join(extracted_ids)

      st.success(
          f"Successfully extracted {len(extracted_ids)} IDs! Copy all at once"
          " below:"
      )

      # Single code block with copy button for the entire bulk data
      st.code(bulk_result, language="text")
    else:
      st.warning(
          "No valid links found in the text. Please check your input."
      )
  else:
    st.warning("Please enter some data or links first.")