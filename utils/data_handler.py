import pandas as pd
import os
from io import BytesIO

CONFIG_TEAMS_PATH = "config/teams.xlsx"
CONFIG_JOBS_PATH = "config/jobs.xlsx"
RECORD_PATH = "data/record.xlsx"

def load_teams():
    if os.path.exists(CONFIG_TEAMS_PATH):
        return pd.read_excel(CONFIG_TEAMS_PATH)
    else:
        return pd.DataFrame(columns=["Team", "Member"])

def load_jobs():
    if os.path.exists(CONFIG_JOBS_PATH):
        return pd.read_excel(CONFIG_JOBS_PATH)
    else:
        return pd.DataFrame(columns=["Job Code", "Name", "Level", "Category"])

def save_record(new_df):
    if os.path.exists(RECORD_PATH):
        existing = pd.read_excel(RECORD_PATH)
        df = pd.concat([existing, new_df], ignore_index=True)
    else:
        df = new_df
    df.to_excel(RECORD_PATH, index=False)

def load_record():
    if os.path.exists(RECORD_PATH):
        df = pd.read_excel(RECORD_PATH)
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    else:
        return pd.DataFrame(columns=["Date", "Team", "Leader", "Member", "Present", "Hours", "Project", "Job Code"])

def dataframe_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Summary')
        writer.save()
    output.seek(0)
    return output
