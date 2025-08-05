import streamlit as st
from utils.data_handler import load_teams, save_record, load_record
from utils.validation import validate_record
from utils.report import generate_summary_chart, download_summary_excel
import pandas as pd

st.set_page_config(page_title="Time & Job Tracker", layout="wide")
st.title("📘 Time & Job Tracker App")

tabs = st.tabs(["Nhập dữ liệu", "Xem dữ liệu", "Báo cáo tổng hợp"])

with tabs[0]:
    st.header("📝 Nhập dữ liệu hàng ngày")
    teams_df = load_teams()

    if teams_df.empty:
        st.warning("⚠️ Không có dữ liệu team. Hãy kiểm tra file teams.xlsx trong thư mục config/")
    else:
        selected_date = st.date_input("Chọn ngày", pd.to_datetime("today"))
        team_list = sorted(teams_df['Team'].dropna().unique())
        selected_team = st.selectbox("Chọn Team", team_list)
        leader = st.text_input("Tên Team Leader", "")

        members = teams_df[teams_df['Team'] == selected_team]['Member'].unique()
        records = []
        st.markdown("### Thành viên trong team:")
        for member in members:
            cols = st.columns([3, 2, 2, 3])
            present = cols[0].selectbox(f"{member} có đi làm?", ["YES", "NO"], key=f"present_{member}")
            hours = cols[1].number_input("Giờ làm", min_value=0.0, max_value=24.0, step=0.5, key=f"hour_{member}")
            project = cols[2].text_input("Project", key=f"proj_{member}")
            job_code = cols[3].text_input("Job Code", key=f"job_{member}")
            records.append({
                "Date": selected_date,
                "Team": selected_team,
                "Leader": leader,
                "Member": member,
                "Present": present,
                "Hours": hours,
                "Project": project,
                "Job Code": job_code
            })

        if st.button("💾 Lưu dữ liệu"):
            df = pd.DataFrame(records)
            error = validate_record(df)
            if error:
                st.error(f"❌ {error}")
            else:
                save_record(df)
                st.success("✅ Dữ liệu đã được lưu thành công!")

with tabs[1]:
    st.header("📄 Xem dữ liệu đã ghi")
    df = load_record()
    if df.empty:
        st.info("Chưa có dữ liệu nào.")
    else:
        team_filter = st.selectbox("Lọc theo team", ["Tất cả"] + sorted(df['Team'].dropna().unique().tolist()))
        if team_filter != "Tất cả":
            df = df[df['Team'] == team_filter]
        st.dataframe(df, use_container_width=True)

with tabs[2]:
    st.header("📊 Báo cáo tổng hợp theo giờ làm việc")
    df = load_record()
    if df.empty:
        st.warning("Không có dữ liệu để tạo báo cáo.")
    else:
        st.plotly_chart(generate_summary_chart(df), use_container_width=True)
        st.download_button("📥 Tải Excel Báo Cáo", data=download_summary_excel(df), file_name="summary_report.xlsx")
