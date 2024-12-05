import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks


st.title("Student Information Management")

# Section: Get Student Details
st.header("View Student Details")
student_id_detail = st.text_input("Enter Student ID to Fetch Details", key="student_id_detail")
if st.button("Fetch Student Details"):
    if student_id_detail:
        student = get_student(student_id_detail)
        if student:
            student_data = {
                "StudentID": student[0],
                "FirstName": student[1],
                "LastName": student[2],
                "Major": student[3],
                "Is Mentor": student[4],
                "WCFI": student[5],
            }
            st.dataframe(student_data)
        else:
            st.error("No student found with this ID.")
    else:
        st.warning("Please enter a Student ID.")

# Section: Update Student Information
st.header("Update Student Information")
update_student_id = st.text_input("Student ID", key="update_student_id")
update_first_name = st.text_input("First Name", key="update_first_name")
update_last_name = st.text_input("Last Name", key="update_last_name")
update_major = st.text_input("Major", key="update_major")
update_is_mentor = st.checkbox("Is Mentor", value=False, key="update_is_mentor")
update_wcfi = st.text_input("WCFI", key="update_wcfi")
if st.button("Update Student Information"):
    if update_student_id:
        success = update_student_details(
            update_student_id,
            update_first_name,
            update_last_name,
            update_major,
            update_is_mentor,
            update_wcfi
        )
        if success:
            st.success("Student information updated successfully!")
        else:
            st.error("Failed to update student information or Student ID not found.")
    else:
        st.warning("Please provide a valid Student ID.")