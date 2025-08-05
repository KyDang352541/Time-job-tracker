def validate_record(df):
    for i, row in df.iterrows():
        member = row['Member']
        if row['Leader'] == "":
            return "Thiếu tên Team Leader."
        if row['Present'] == "YES":
            if row['Hours'] <= 0:
                return f"{member} có đi làm nhưng chưa nhập số giờ."
            if row['Hours'] > 24:
                return f"{member} vượt quá số giờ hợp lệ (max 24h)."
            if row['Hours'] > 9:
                return f"{member} vượt giới hạn 9 giờ làm việc/ngày."
            if row['Project'] == "" or row['Project'].strip().lower() in ["select project"]:
                return f"{member} thiếu thông tin Project."
            if row['Job Code'] == "" or row['Job Code'].strip().lower() in ["enter job code"]:
                return f"{member} thiếu thông tin Job Code."
        if row['Present'] == "NO" and row['Hours'] > 0:
            return f"{member} chọn 'NO' nhưng vẫn có giờ làm."
    return ""  # valid
