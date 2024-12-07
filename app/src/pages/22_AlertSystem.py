import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks

st.title("Alert System Management")
SideBarLinks(show_home=True)

# Section: Retrieve Audit Logs
st.header("Retrieve Audit Logs")
if st.button("Fetch Audit Logs"):
    try:
        response = requests.get("http://web-api:4000/a/alert-system/audit-logs")
        if response.status_code == 200:
            data = response.json()
            if data:
                # Convert data to a Pandas DataFrame for better visualization
                df = pd.DataFrame(data, columns=[
                    "AlertID", "ActivityType", "Description", "Severity",
                    "Timestamp", "Status", "GeneratedByType"
                ])
                st.write("Audit Logs:")
                st.dataframe(df)  # Display the DataFrame as an interactive table
            else:
                st.info("No audit logs found.")
        else:
            st.error(f"Failed to fetch audit logs: {response.status_code}")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")


# Section: Submit New Alert
st.header("Submit New Alert")
activity_type = st.text_input("Activity Type", key="create_activity_type")
description = st.text_area("Description", key="create_description")
severity = st.selectbox("Severity", ["Low", "Medium", "High"], key="create_severity")
generated_by = st.text_input("Generated By (User ID)", key="create_generated_by")
if st.button("Submit Alert"):
    if activity_type and description and severity and generated_by:
        payload = {
            "activity_type": activity_type,
            "description": description,
            "severity": severity,
            "generated_by": generated_by
        }
        response = requests.post("http://web-api:4000/a/alert-system", json=payload)
        if response.status_code == 200:
            st.success("Alert submitted successfully!")
        else:
            st.error("Failed to submit alert.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Update Alert Configuration
st.header("Update Alert Configuration")
alert_id = st.text_input("Alert ID to Update", key="update_alert_id")
status = st.selectbox("New Status", ["Pending", "Resolved"], key="update_status")
if st.button("Update Alert"):
    if alert_id and status:
        payload = {
            "alert_id": alert_id,
            "status": status
        }
        response = requests.put("http://web-api:4000/a/alert-system", json=payload)
        if response.status_code == 200:
            st.success("Alert updated successfully!")
        else:
            st.error("Failed to update alert.")
    else:
        st.warning("Please fill out all required fields.")

# Section: Delete Old Logs
st.header("Delete Old Logs")
if st.button("Delete Logs Older Than Retention Policy"):
    response = requests.delete("http://web-api:4000/a/alert-system/logs")
    if response.status_code == 200:
        st.success("Old logs deleted successfully!")
    else:
        st.error("Failed to delete old logs.")