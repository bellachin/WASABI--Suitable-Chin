import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks


SideBarLinks(show_home=True)

st.title("System Update Management")

# Section: Retrieve Current System Status
if st.button("Fetch Update"):
    response = requests.get("http://web-api:4000/a/system-update")
    if response.status_code == 200:
        data = response.json() 
        if data:
            df = pd.DataFrame(data)
            st.table(df)  
        else:
            st.warning("No updates found.")
    else:
        st.error("Failed to fetch system status.")

# Section: Submit System Report
st.header("Submit System Report")
update_type = st.text_input("Update Type", key="create_update_type")
description = st.text_area("Description", key="create_description")
if st.button("Submit Report"):
    if update_type and description:
        payload = {
            "update_type": update_type,
            "description": description,
        }
        response = requests.post("http://web-api:4000/a/system-update", json=payload)
        if response.status_code == 200:
            st.success("System report submitted successfully!")
        else:
            st.error("Failed to submit system report.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Update Health Monitoring Configuration
st.header("System Health Update")
update_id = st.text_input("Update ID to Modify", key="update_update_id")
new_description = st.text_area("New Description", key="update_new_description")
if st.button("Update Configuration"):
    if update_id and new_description:
        payload = {
            "update_id": update_id,
            "description": new_description
        }
        response = requests.put("http://web-api:4000/a/system-update", json=payload)
        if response.status_code == 200:
            st.success("Configuration updated successfully!")
        else:
            st.error("Failed to update configuration.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Clear Outdated Logs
st.header("Clear Outdated Logs")
if st.button("Clear Logs Older Than Retention Policy"):
    response = requests.delete("http://web-api:4000/a/system-update/logs")
    if response.status_code == 200:
        st.success("Outdated logs cleared successfully!")
    else:
        st.error("Failed to clear outdated logs.")
