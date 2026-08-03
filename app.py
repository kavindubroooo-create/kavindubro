import base64

# හැකර් ස්ටයිල් සහ 'id bulk finder' නම ඇතුළත් ප්‍රධාන කෝඩ් එක
source_code = """
import streamlit as st
import requests
import re

# Hacker Theme Custom CSS Styling
st.markdown('''
    <style>
    .stApp {
        background-color: #050505;
        color: #00ff66;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3, p, label, .stMarkdown {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    .stTextArea textarea {
        background-color: #0d0d0d !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    .stButton button {
        background-color: #00ff66 !important;
        color: #050505 !important;
        font-weight: bold;
        border: none;
        font-family: 'Courier New', Courier, monospace !important;
    }
    .stButton button:hover {
        background-color: #00cc52 !important;
        color: #000000 !important;
    }
    table {
        color: #00ff66 !important;
        background-color: #0d0d0d !important;
    }
    th {
        background-color: #1a1a1a !important;
        color: #00ff66 !important;
    }
    td {
        color: #00ff66 !important;
    }
    </style>
''', unsafe_allow_html=True)

def extract_fb_info(url):
    url = url.strip()
    match_id = re.search(r'[?&]id=(\d+)', url)
    if match_id:
        return url, match_id.group(1)
    match_num = re.search(r'facebook\\.com/(\\d+)(?:/|$)?', url)
    if match_num:
        return url, match_num.group(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, allow_redirects=True, headers=headers, timeout=10)
        final_url = response.url
        match_id = re.search(r'[?&]id=(\d+)', final_url)
        if match_id:
            return final_url, match_id.group(1)
        match_num = re.search(r'facebook\\.com/(\\d+)(?:/|$)?', final_url)
        if match_num:
            return final_url, match_num.group(1)
        parts = final_url.rstrip('/').split('/')
        if len(parts) > 3 and 'facebook.com' in parts[2]:
            username = parts[3].split('?')[0]
            return final_url, username
        return final_url, 'Unknown'
    except Exception as e:
        return url, f"Error: {str(e)}"

st.title("[+] id bulk finder v1.0")
st.markdown("---")
st.write(">> ENTER TARGET FACEBOOK LINKS (PROFILE / SHARE) BELOW:")

links_input = st.text_area("Target List")

if st.button("EXECUTE EXTRACTION"):
    if links_input.strip():
        links = [l.strip() for l in links_input.split('\\n') if l.strip()]
        output_data = []
        
        with st.spinner(">> BYPASSING REDIRECTS & EXTRACTING IDS..."):
            for link in links:
                real_url, fb_id = extract_fb_info(link)
                output_data.append({"Original Link": link, "Real URL": real_url, "ID/User": fb_id})
        
        st.success(">> OPERATION SUCCESSFUL!")
        st.table(output_data)
    else:
        st.warning("[!] WARNING: TARGET LIST IS EMPTY.")
"""

# කෝඩ් එක Base64 වෙත සංකේතනය කිරීම
encoded = base64.b64encode(source_code.encode("utf-8")).decode("utf-8")

# ආරක්ෂිතව ක්‍රියාත්මක වන runner කෝඩ් එක සකස් කිරීම
runner_code = f"""import base64
import streamlit as st
import requests
import re

encrypted_data = "{encoded}"
exec(base64.b64decode(encrypted_data).decode('utf-8'))
"""

# app.py නමින් ෆයිල් එකක් ලෙස ඩිස්ක් එකට ලිවීම
with open("app.py", "w", encoding="utf-8") as f:
  f.write(runner_code)

print(
    "හැකර් තීම් සහ සංකේතනය සාර්ථකයි! අලුතින් හැදුණු 'app.py' ෆයිල් එක දැන් GitHub"
    " වෙත Upload කරන්න."
)