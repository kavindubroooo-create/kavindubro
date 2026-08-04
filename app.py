import asyncio
import pandas as pd
import re
import streamlit as st
from playwright.async_api import async_playwright

st.set_page_config(
    page_title="Facebook Numeric ID Extractor", page_icon="🎯", layout="wide"
)

# Completely Hide Streamlit Header, Toolbar, Footer & Deploy Button
hide_menu_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stAppDeployButton {display:none;}
header {visibility: hidden;}
[data-testid="stHeader"] {visibility: hidden; display: none;}
[data-testid="stToolbar"] {visibility: hidden; display: none;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Advanced Cyberpunk UI Styling with Kavindu Bro Badge
st.markdown(
    """
    <style>
    .stApp {
        background: #090a0f;
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
        border: 1px solid #00ffcc;
        color: #00ffcc;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 1rem;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0,255,204,0.3);
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
    .result-box {
        background: #12151c;
        border: 1px solid #00ffcc33;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="header-container">
        <div class="main-header">[🎯] FACEBOOK NUMERIC ID EXTRACTOR</div>
        <div class="credit-badge">⚡ kavindu bro</div>
    </div>
    """,
    unsafe_allow_html=True,
)

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


async def get_real_facebook_id(link):
  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X)"
            " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5"
            " Mobile/15E148 Safari/604.1"
        )
    )
    page = await context.new_page()

    real_url = link
    numeric_id = "Not Found"

    try:
      # Go to link and wait until network is idle or redirected
      response = await page.goto(link, timeout=15000, wait_until="commit")
      # Wait for final redirection url
      await page.wait_for_load_state("domcontentloaded", timeout=10000)
      real_url = page.url
      html_content = await page.content()

      # 1. Check final URL for ?id=XXXXX or profile.php?id=XXXXX
      match_id = re.search(r"[?&]id=(\d+)", real_url)
      if match_id:
        numeric_id = match_id.group(1)
      else:
        # 2. Check Open Graph meta url tag
        og_url_match = re.search(
            r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)["\']',
            html_content,
            re.IGNORECASE,
        )
        if og_url_match:
          og_url = og_url_match.group(1)
          m_og = re.search(r"[?&]id=(\d+)", og_url)
          if m_og:
            numeric_id = m_og.group(1)

        # 3. Deep search patterns in page source
        if numeric_id == "Not Found":
          patterns = [
              r'"user_id"\s*:\s*"(\d+)"',
              r'"profile_id"\s*:\s*"(\d+)"',
              r'"entity_id"\s*:\s*"(\d+)"',
              r"user_id=(\d+)",
              r"profile\.php\?id=(\d+)",
              r'"owner_id"\s*:\s*"(\d+)"',
              r'actor_id["\s:]+"(\d+)"',
              r'\\/profile\\.php\\?id=(\d+)',
          ]
          for pat in patterns:
            m = re.search(pat, html_content)
            if m:
              numeric_id = m.group(1)
              break
    except Exception as e:
      real_url = f"Error: {str(e)}"
      numeric_id = "Failed"

    await browser.close()
    return real_url, numeric_id


if st.button("EXTRACT NUMERIC IDS"):
  if links_input.strip():
    links = [l.strip() for l in links_input.split("\n") if l.strip()]
    results = []
    extracted_ids_list = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    async def process_all_links():
      for idx, link in enumerate(links):
        status_text.text(
            f"Processing target {idx+1} of {len(links)} (Headless Browser)..."
        )
        real_url, numeric_id = await get_real_facebook_id(link)

        results.append({
            "Index": idx + 1,
            "Original Link": link,
            "Real URL": real_url,
            "Facebook Numeric ID": numeric_id,
        })
        extracted_ids_list.append(numeric_id)
        progress_bar.progress((idx + 1) / len(links))

    # Run async function in Streamlit
    asyncio.run(process_all_links())

    progress_bar.empty()
    status_text.empty()

    st.success(">>> EXTRACTION COMPLETED!")
    st.markdown("### RESULTS DASHBOARD")

    for res in results:
      st.markdown(
          f"""
            <div class="result-box">
                <b>#{res['Index']} Original:</b> <span style="color:#888;">{res['Original Link']}</span><br>
                <b>Real URL:</b> <span style="color:#aaa; font-size: 0.9em;">{res['Real URL']}</span>
            </div>
            """,
          unsafe_allow_html=True,
      )
      st.text("Facebook Numeric ID (Click copy icon on the right):")
      st.code(res["Facebook Numeric ID"], language="text")
      st.markdown("---")

    st.markdown(
        "### [📋] BULK IDS OUTPUT (Click top-right copy icon to copy all"
        " stacked IDs):"
    )
    bulk_ids_text = "\n".join(extracted_ids_list)
    st.code(bulk_ids_text, language="text")

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