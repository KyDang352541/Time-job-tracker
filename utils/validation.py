# utils/validation.py

def validate_record(df):
    for i, row in df.iterrows():
        member = row['Member']
        # Kiểm tra tên leader
        if row['Leader'] == "":
            return f"Thiếu tên Team Leader."

        # Nếu có đi làm thì cần kiểm tra thêm
        if row['Present'] == "YES":
            # Kiểm tra giờ làm
            if row['Hours'] <= 0:
                return f"{member} có đi làm nhưng chưa nhập số giờ."
            if row['Hours'] > 24:
                return f"{member} vượt quá số giờ hợp lệ (max 24h)."
            if row['Hours'] > 9:
                return f"{member} vượt giới hạn 9 giờ làm việc/ngày."

            # Kiểm tra project
            if row['Project'] == "" or row['Project'].strip().lower() in ["select project"]:
                return f"{member} thiếu thông tin Project."

            # Kiểm tra job code
            if row['Job Code'] == "" or row['Job Code'].strip().lower() in ["enter job code"]:
                return f"{member} thiếu thông tin Job Code."

        # Nếu không đi làm mà vẫn điền giờ
        if row['Present'] == "NO" and row['Hours'] > 0:
            return f"{member} chọn 'NO' nhưng vẫn có giờ làm."

    return ""  # Dữ liệu hợp lệ
