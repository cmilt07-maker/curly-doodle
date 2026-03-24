import streamlit as st
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="72-Hour Deep Fast", page_icon="🌑")

# --- UI STYLING ---
st.title("🌑 72-Hour Metabolic Reset")
st.write("Targeting deep autophagy and peak fat oxidation.")

# --- SIDEBAR: STATS & SETTINGS ---
st.sidebar.header("User Profile")
weight = st.sidebar.number_input("Weight (lbs)", value=240)
height_ft = st.sidebar.number_input("Height (ft)", value=5)
height_in = st.sidebar.number_input("Height (in)", value=9)
age = st.sidebar.number_input("Age", value=30)

st.sidebar.divider()
is_keto_start = st.sidebar.toggle("Keto-Friendly Start?", value=True)
target_hrs = 72

# --- INPUT: START TIME ---
# Set this to when you finished your last meal
start_time = st.datetime_input("Fast Start Time:", datetime.now() - timedelta(minutes=1))

# --- CALCULATIONS ---
now = datetime.now()
elapsed = now - start_time
elapsed_hrs = max(0.0, elapsed.total_seconds() / 3600)
remaining_hrs = max(0.0, target_hrs - elapsed_hrs)

# BMR Math (Hourly Burn)
weight_kg = weight * 0.453592
height_cm = (height_ft * 30.48) + (height_in * 2.54)
bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
hourly_burn = bmr / 24
total_burned = hourly_burn * elapsed_hrs

# --- 72-HOUR PHYSIOLOGY LOGIC ---
offset = 4 if is_keto_start else 0
def get_72hr_status(hrs):
    h = hrs + offset
    if h < 12: return "Sugar Burning", "0.2 - 0.5", "Body is using up glucose and glycogen stores."
    elif h < 18: return "The Switch", "0.5 - 1.0", "Transitioning to fat as primary fuel. Hunger peaks here."
    elif h < 24: return "Ketosis", "1.1 - 2.0", "Fat oxidation is high. Insulin is at baseline."
    elif h < 48: return "Autophagy", "2.1 - 3.5", "Cellular repair begins. Growth hormone increases."
    elif h < 60: return "Peak GH", "3.6 - 5.0", "Growth hormone is up to 5x baseline to protect muscle."
    else: return "Immune Reset", "5.0+", "Old immune cells are being recycled. Deep metabolic healing."

zone, ketones, desc = get_72hr_status(elapsed_hrs)

# --- DISPLAY ---
if elapsed_hrs >= target_hrs:
    st.balloons()
    st.success(f"🏆 72-HOUR GOAL REACHED! You've burned approximately {int(total_burned)} calories.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Hours Fasted", f"{elapsed_hrs:.1f}")
    c2.metric("Hours Left", f"{remaining_hrs:.1f}")
    c3.metric("Est. Burn", f"{int(total_burned)} kcal")

    st.subheader(f"Current State: {zone}")
    st.markdown(f"**Ketones:** `{ketones} mmol/L` | **Status:** {desc}")
    
    # Progress Bar
    progress_pct = min(elapsed_hrs / target_hrs, 1.0)
    st.progress(progress_pct, text=f"Total Progress: {int(progress_pct*100)}%")

st.divider()
st.warning("⚠️ **72-Hour Protocol:** Ensure you are taking electrolytes (Sodium, Potassium, Magnesium). If you feel dizzy or unwell, listen to your body and break the fast safely.")

# Live Refresh every 2 minutes to save battery but keep it moving
time.sleep(120)
st.rerun()

