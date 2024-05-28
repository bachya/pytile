import streamlit as st
import pandas as pd

# Initialize the inventory dataframe
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Item Name'])
    st.session_state.page = "login_page"

# Define the login page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "test" and password == "test":
            st.session_state.page = "main_page"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# Define the main page
def main_page():
    st.title("Welcome to the Main Page")
    st.markdown("**Easy Tag**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Link Item"):
            st.session_state.page = "add_item_page"
            st.experimental_rerun()
    with col2:
        if st.button("Locate Item"):
            st.session_state.page = "locate_item_page"
            st.experimental_rerun()

# Define the add item page
def add_item_page():
    st.title("Add Item")
    item_name = st.text_input("Item Name")
    if st.button("Add"):
        new_item = pd.DataFrame({'Serial Number': [len(st.session_state.inventory) + 1], 'Item Name': [item_name]})
        st.session_state.inventory = pd.concat([st.session_state.inventory, new_item])
        st.write(f"Added {item_name} to the directoy with Serial Number {len(st.session_state.inventory)}")
    if st.button("Go Back"):
        st.session_state.page = "main_page"
        st.experimental_rerun()
import base64

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""

          
            <audio style="display:none;" controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

import threading
import base64
import streamlit as st

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            Your browser does not support the audio element.
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def locate_item_page():
    st.title("Locate Item")
    st.write("Inventory:")
    unique_id = st.session_state.get('page_id', 0)  # Get a unique page ID if already set, otherwise default to 0
    for index, row in st.session_state.inventory.iterrows():
        item_key = f"locate_{index}_{unique_id}"  # Append the unique_id to the key
        if st.button(f"Locate {row['Item Name']}", key=item_key):
            st.image("https://github.com/Aishamdawood/images/blob/92aed9e6d82fa9842f51a8ee8e86b93e8061fca2/ringing.gif?raw=true",  width=100, use_column_width=False)  # Replace with the direct link to your image file
            autoplay_audio("rining.mp3")
            st.write(f"Locating {row['Item Name']} in the inventory")
        unique_id = unique_id + 1  # Increment the unique ID after rendering the page

    if st.button("Found"):
        st.write("Item found!")

    if st.button("Go Back", key=f"go_back_{unique_id}"):
        st.session_state.page = "main_page"
        st.experimental_rerun()   
# Set the page layout to "wide"
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Display the login page by default
if st.session_state.page == "login_page":
    login_page()
elif st.session_state.page == "main_page":
    main_page()
elif st.session_state.page == "add_item_page":
    add_item_page()
elif st.session_state.page == "locate_item_page":
    locate_item_page()