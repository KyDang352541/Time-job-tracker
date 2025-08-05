# main.py
import streamlit as st
import pandas as pd
from datetime import date
from utils.data_handler import load_teams, load_jobs, save_record, load_record
from utils.validation import validate_record

st.set_page_config(layout="wide")
st.title("Time & Job Tracker - Streamlit Version")

# --- Load config files ---
teams_df = load_teams()
jobs_df = load_jobs()

# --- Input Section ---
st.header("1. Nhập dữ liệu thông tin ngày làm")
col1, col2, col3 = st.columns(3)

with col1:
    selected_team = st.selectbox("Chọn Team", teams_df['Team'].unique())
with col2:
    team_leader = st.text_input("Tên Team Leader")
with col3:
    work_date = st.date_input("Ngày", value=date.today())

# --- Load team members ---
st.subheader("2. Danh sách thành viên")
members = teams_df[teams_df['Team'] == selected_team]['Member'].tolist()
data_rows = []

for member in members:
    st.markdown(f"#### {member}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        present = st.selectbox("Đi làm?", ["YES", "NO"], key=f"present_{member}")
    with col2:
        hours = st.number_input("Số giờ", min_value=0.0, max_value=24.0, step=0.5, key=f"hours_{member}")
    with col3:
        project = st.text_input("Project", key=f"project_{member}")
    with col4:
        job_code = st.text_input("Job Code", key=f"job_{member}")

    data_rows.append({
        "Date": work_date,
        "Team": selected_team,
        "Leader": team_leader,
        "Member": member,
        "Present": present,
        "Hours": hours,
        "Project": project,
        "Job Code": job_code
    })

# --- Confirm and Save ---
if st.button("Lưu dữ liệu"):
    df = pd.DataFrame(data_rows)
    error_msg = validate_record(df)
    if error_msg:
        st.error(error_msg)
    else:
        save_record(df)
        st.success("Đã lưu dữ liệu thành công!")

# --- View Existing Records ---
st.header("3. Xem dữ liệu đã ghi")
record_df = load_record()
st.dataframe(record_df.sort_values("Date", ascending=False), use_container_width=True)
