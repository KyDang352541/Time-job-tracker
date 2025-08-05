# utils/report.py
import pandas as pd
import plotly.express as px
from io import BytesIO

# Biểu đồ tổng giờ theo Team
def generate_summary_chart(df):
    df_summary = (
        df[df["Present"] == "YES"]
        .groupby(["Team", "Member"])
        ["Hours"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        df_summary,
        x="Member",
        y="Hours",
        color="Team",
        title="Tổng số giờ theo thành viên & team",
        labels={"Hours": "Tổng giờ làm", "Member": "Thành viên"},
        height=500
    )
    fig.update_layout(xaxis_tickangle=-30)
    return fig

# Xuất dữ liệu tổng hợp thành file Excel
def download_summary_excel(df):
    df_summary = (
        df[df["Present"] == "YES"]
        .groupby(["Team", "Member"])
        ["Hours"]
        .sum()
        .reset_index()
        .sort_values(["Team", "Member"])
    )
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_summary.to_excel(writer, sheet_name="Summary", index=False)
    output.seek(0)
    return output
