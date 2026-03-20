import streamlit as st
import pandas as pd
from datetime import datetime
import os

# App Setup
st.set_page_config(page_title="Work Timer", page_icon="⏱️", layout="centered")
st.title("👨‍🍳 Shift Tracker")

# File to save data
SAVE_FILE = "work_hours.csv"
STATUS_FILE = "current_status.txt"

# Load existing history
if os.path.exists(SAVE_FILE):
    df = pd.read_csv(SAVE_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Restaurant", "Start Time", "End Time", "Total Hours"])

# Check if there is an active shift saved on the server
active_start = None
active_restaurant = "Bath & Rose"

if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        data = f.read().split(",")
        if len(data) == 2:
            active_start = datetime.fromisoformat(data[0])
            active_restaurant = data[1]

# Restaurant Selection
restaurant_list = ["Bath & Rose", "Courtyard Hotel", "Butter and Rush"]
selected_restaurant = st.selectbox("Select Restaurant:", restaurant_list, disabled=(active_start is not None))

st.divider()

if active_start is None:
    # CLOCK IN MODE
    if st.button("🚀 Start Work", use_container_width=True, type="primary"):
        now = datetime.now()
        with open(STATUS_FILE, "w") as f:
            f.write(f"{now.isoformat()},{selected_restaurant}")
        st.rerun()
else:
    # CLOCK OUT MODE
    st.warning(f"Currently Working at: **{active_restaurant}**")
    st.info(f"Started at: {active_start.strftime('%I:%M %p')}")
    
    if st.button("🛑 End Work", use_container_width=True, type="secondary"):
        now = datetime.now()
        duration = now - active_start
        hours = round(duration.total_seconds() / 3600, 2)
        
        # Save to History
        new_entry = {
            "Date": now.strftime("%Y-%m-%d"),
            "Restaurant": active_restaurant,
            "Start Time": active_start.strftime("%H:%M:%S"),
            "End Time": now.strftime("%H:%M:%S"),
            "Total Hours": hours
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(SAVE_FILE, index=False)
        
        # Clear Active Status
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)
            
        st.balloons()
        st.success(f"Shift Saved! Total: {hours} hours")
        st.rerun()

# Display History Table
st.divider()
st.subheader("Last 5 Shifts")
st.dataframe(df.tail(5), use_container_width=True)

# Monthly Summary
if not df.empty:
    st.subheader("Total Hours Earned")
    summary = df.groupby("Restaurant")["Total Hours"].sum().reset_index()
    st.table(summary)
