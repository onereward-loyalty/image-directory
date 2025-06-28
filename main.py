# import streamlit as st
# import os
# import json
# import requests
# from PIL import Image
# from io import BytesIO
# import base64

# IMGUR_CLIENT_ID = "ca638108d533025"
# JSON_FILE = "reward_images.json"

# # Initialize JSON
# def load_data():
#     if not os.path.exists(JSON_FILE):
#         with open(JSON_FILE, 'w') as f:
#             json.dump({}, f)
#     with open(JSON_FILE, 'r') as f:
#         return json.load(f)

# def save_data(data):
#     with open(JSON_FILE, 'w') as f:
#         json.dump(data, f, indent=4)

# # Upload image to Imgur
# def upload_to_imgur(image_bytes):
#     headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
#     data = {"image": base64.b64encode(image_bytes).decode("utf-8")}
#     response = requests.post("https://api.imgur.com/3/image", headers=headers, data=data)
#     if response.status_code == 200:
#         return response.json()["data"]["link"]
#     else:
#         st.error("Upload failed.")
#         return None

# # Copy to clipboard button (JS hack)
# def clipboard_button(link):
#     b64 = base64.b64encode(link.encode()).decode()
#     return f"""
#     <button onclick="navigator.clipboard.writeText('{link}'); this.innerText='Copied!';">Copy</button>
#     """

# # App
# st.set_page_config(page_title="Reward Image Directory", layout="wide")
# st.title("🏆 Reward Image Directory with Imgur")

# data = load_data()

# # Sidebar
# st.sidebar.header("📁 Folder Manager")
# folders = list(data.keys())

# # Create or select folder
# selected_folder = st.sidebar.selectbox("Select Folder", folders + ["+ Create New Folder"])
# if selected_folder == "+ Create New Folder":
#     new_folder = st.sidebar.text_input("New Folder Name")
#     if st.sidebar.button("Create Folder") and new_folder:
#         if new_folder not in data:
#             data[new_folder] = []
#             save_data(data)
#             st.rerun()
#         else:
#             st.sidebar.warning("Folder already exists.")
# else:
#     # Upload image
#     uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
#     if uploaded_file and st.sidebar.button("Upload to Imgur"):
#         img_bytes = uploaded_file.read()
#         link = upload_to_imgur(img_bytes)
#         if link:
#             data[selected_folder].append({
#                 "filename": uploaded_file.name,
#                 "imgur_link": link
#             })
#             save_data(data)
#             st.success(f"Uploaded: {link}")
#             st.rerun()

# # Gallery View
# if selected_folder and selected_folder != "+ Create New Folder":
#     st.subheader(f"📷 Gallery - {selected_folder}")
#     columns = st.columns(3)
#     for i, entry in enumerate(data[selected_folder]):
#         with columns[i % 3]:
#             st.image(entry["imgur_link"], use_container_width=True)
#             st.code(entry["imgur_link"], language="markdown")
#             st.markdown(clipboard_button(entry["imgur_link"]), unsafe_allow_html=True)

import streamlit as st
import os
import json
import requests
import base64

# 🔐 Imgur Client ID (keep secret in production)
IMGUR_CLIENT_ID = "ca638108d533025"
JSON_FILE = "reward_images.json"

# ----------------- JSON Utilities -----------------
def load_data():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w') as f:
            json.dump({}, f)
    with open(JSON_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ----------------- Imgur Upload -----------------
def upload_to_imgur(image_bytes):
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    data = {"image": base64.b64encode(image_bytes).decode("utf-8")}
    response = requests.post("https://api.imgur.com/3/image", headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        st.error("Upload to Imgur failed.")
        return None

# ----------------- Copy Button -----------------
def clipboard_button(link):
    return f"""
    <button onclick="navigator.clipboard.writeText('{link}'); this.innerText='Copied!';" style="margin-top:5px;">Copy</button>
    """

# ----------------- App Layout -----------------
st.set_page_config(page_title="One Reward Image Directory", layout="wide")
st.markdown("# One Reward Image Directory")
st.markdown("Upload images, organize them by folders, and share Imgur links.")

# Load and Save JSON
data = load_data()

# ----------------- Sidebar -----------------
st.sidebar.header("📁 Folder Manager")
folders = list(data.keys())
selected_folder = st.sidebar.selectbox("Select Folder", folders + ["+ Create New Folder"])

# Folder creation
if selected_folder == "+ Create New Folder":
    new_folder = st.sidebar.text_input("New Folder Name")
    if st.sidebar.button("Create Folder") and new_folder.strip():
        if new_folder in data:
            st.sidebar.warning("Folder already exists.")
        else:
            data[new_folder] = []
            save_data(data)
            st.rerun()

# File upload
if selected_folder != "+ Create New Folder":
    uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_file and st.sidebar.button("Upload to Server"):
        img_bytes = uploaded_file.read()
        imgur_link = upload_to_imgur(img_bytes)
        if imgur_link:
            data[selected_folder].append({
                "filename": uploaded_file.name,
                "imgur_link": imgur_link
            })
            save_data(data)
            st.success(f"Uploaded successfully to One Reward Server.")
            st.rerun()

# ----------------- Gallery -----------------
if selected_folder != "+ Create New Folder" and selected_folder in data:
    st.subheader(f"📷 Gallery - `{selected_folder}`")

    entries = data[selected_folder]
    if not entries:
        st.info("No images uploaded yet.")
    else:
        images_per_row = 4
        for i in range(0, len(entries), images_per_row):
            row_entries = entries[i:i + images_per_row]
            cols = st.columns(images_per_row)
            for col, entry in zip(cols, row_entries):
                with col:
                    st.image(entry["imgur_link"], use_container_width=True)
                    st.code(entry["imgur_link"], language="markdown")
                    # st.markdown(clipboard_button(entry["imgur_link"]), unsafe_allow_html=True)


# ----------------- Optional: Styling -----------------
st.markdown("""
    <style>
    .stImage > img {
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)
