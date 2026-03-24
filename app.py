import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Fasting Pro", page_icon="⚡")

st.title("⚡ Metabolic Tracker")

# --- User Inputs ---
is_keto_start = st.toggle("Keto-Friendly Last Meal?", value=True)
start_time = st.sidebar.datetime_input("When did you stop eating?", datetime.now())

# Calculate Elapsed Time
elapsed = datetime.now() - start_time
elapsed_hrs = elapsed.total_seconds() / 3600

# --- Adjusted Logic for Keto/BMR ---
# We shift the zones earlier if starting from Keto
offset = 4 if is_keto_start else 0

def get_status(hrs):
    h = hrs + offset
    if h < 4:
        return "Anabolic", "0.1 - 0.2", "Processing last nutrients."
    elif h < 10:
        return "Catabolic", "0.3 - 0.5", "Glycogen dropping fast."
    elif h < 16:
        return "Fat Burning", "0.6 - 1.5", "Nutritional Ketosis beginning."
    elif h < 24:
        return "Deep Ketosis", "1.6 - 3.0", "Primary fuel is now fat."
    else:
        return "Autophagy", "3.0+", "Cellular cleanup active."

zone, ketones, desc = get_status(elapsed_hrs)

# --- Mobile Display ---
st.metric("Hours Fasted", f"{elapsed_hrs:.1f}")

st.subheader(f"Zone: {zone}")
st.write(f"**Est. Ketones:** {ketones} mmol/L")
st.info(desc)

# Progress towards a standard 16-hour goal
progress = min(elapsed_hrs / 16, 1.0)
st.progress(progress, text=f"Goal: 16 Hours ({int(progress*100)}%)")
