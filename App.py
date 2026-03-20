import streamlit as st
import pandas as pd
from datetime import datetime
import os

# App Setup
st.set_page_config(page_title="Work Timer", page_icon="⏱️")
st.title("👨‍🍳 Shift Tracker")

# File to save data
SAVE_FILE = "work_hours.csv"

# Load existing data
if os.path.exists(SAVE_FILE):
    df = pd.read_csv(SAVE_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Restaurant", "Start Time", "End Time", "Total Hours"])

# Tracking Logic
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# Restaurant Selection
restaurant_list = ["Bath & Rose", "Courtyard Hotel", "Butter and Rush"]
selected_restaurant = st.selectbox("Select Restaurant:", restaurant_list)

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Start Work", use_container_width=True):
        st.session_state.start_time = datetime.now()
        st.session_state.current_restaurant = selected_restaurant
        st.success(f"Started at {selected_restaurant}: {st.session_state.start_time.strftime('%H:%M:%S')}")

with col2:
    if st.button("🛑 End Work", use_container_width=True):
        if st.session_state.start_time:
            end_time = datetime.now()
            duration = end_time - st.session_state.start_time
            hours = round(duration.total_seconds() / 3600, 2)
            
            # Save to Dataframe
            new_entry = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Restaurant": st.session_state.current_restaurant,
                "Start Time": st.session_state.start_time.strftime("%H:%M:%S"),
                "End Time": end_time.strftime("%H:%M:%S"),
                "Total Hours": hours
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(SAVE_FILE, index=False)
            
            st.session_state.start_time = None
            st.balloons()
            st.info(f"Shift Ended at {st.session_state.current_restaurant}! Total: {hours} hours")
        else:
            st.error("Please press Start first!")

# Display History
st.divider()
st.subheader("Previous Shifts")
st.dataframe(df.tail(10), use_container_width=True)

# Calculate Totals per Restaurant
if not df.empty:
    st.subheader("Summary by Restaurant")
    summary = df.groupby("Restaurant")["Total Hours"].sum().reset_index()
    st.table(summary)
