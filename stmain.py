import streamlit as st
import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE_URL=os.getenv("base_url")
 
st.title("Student Management Portal")
 
menu = ["Add Student", "Get Student", "Update Student", "Delete Student"]
choice = st.sidebar.radio("Choose Action", menu)
 
if choice == "Add Student":
    st.header("Add Student")
    id = st.text_input("ID",key="add_id")
    name = st.text_input("Name", key="add_name")
    section = st.text_input("Section", key="add_section")
    cgpa = st.number_input("CGPA", key="add_cgpa")
 
    if st.button("Save Student"):
        payload = {"id": id, "name": name, "section": section, "cgpa": cgpa}
        res = requests.post(f"{BASE_URL}/students", json=payload)
        if res.status_code == 200:
            st.success(f"Student '{name}' saved successfully!")
        else:
            st.error("Failed to save student")
 

if choice == "Get Student":
    st.header("Get Student by Roll Number")
    roll_no = st.text_input("Enter Roll Number",key="get_roll")
 
    if st.button("Fetch Student"):
        res = requests.get(f"{BASE_URL}/students/{roll_no}")
        if res.status_code == 200:
            data = res.json()
            if "id" in data:
                st.success("Student Found!")
                st.table([data])
            else:
                st.warning("Student not found")
        else:
            st.error("Couldn't fetch student")
 
if choice == "Update Student":
    st.header("Update Student")
    roll_no = st.text_input("Roll No to Update", key="upd_roll")
    name = st.text_input("New Name", key="upd_name")
    section = st.text_input("New Section", key="upd_section")
    cgpa = st.number_input("New CGPA",key="upd_cgpa")
 
    if st.button("Update"):
        payload = {"id": roll_no, "name": name, "section": section, "cgpa": cgpa}
        res = requests.put(f"{BASE_URL}/students/{roll_no}", json=payload)
        if res.status_code == 200:
            st.success("Student updated successfully!")
        else:
            st.error("Failed to update student")
 

if choice == "Delete Student":
    st.header("Delete Student")
    roll_no = st.text_input("Roll No to Delete", key="del_roll")
 
    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/students/{roll_no}")
        if res.status_code == 200:
            st.success("Student deleted successfully!")
        elif res.status_code == 404:
            st.warning("Student not found")
        else:
            st.error("Failed to delete student")
 