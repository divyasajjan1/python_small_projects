"""
ADAS Pre-Crash Analysis

Objective:
Determine whether ADAS (Autopilot or Cruise Control) was active
at any point during the 20 seconds leading up to a crash event.

Input:
CSV file containing vehicle telemetry and ADAS states

Output:
Boolean ADAS flag indicating system activity before crash
"""

import pandas as pd

# Step 1: Read the CSV
df = pd.read_csv("vehicle_data_input.csv", parse_dates=['DATE (UTC)'])

# Step 2: Sort by Vehicle and Time (just in case)
df = df.sort_values(['Vehicle Identification Number', 'DATE (UTC)'])

# Step 3: Define active states
autopilot_active = ['Autopilot', 'Full Self-Driving', 'Autopilot nav']
cruise_active = ['Cruise Control Active']

# Step 4: Initialize ADAS column
df['ADAS'] = False

# Step 5: Identify crash/collision rows
# Find all collision indicator columns
collision_cols = [col for col in df.columns if 'Collision Indicator' in col]

# Create a single boolean column: True if any collision indicator or Crash System Wakeup is True
df['collision'] = df[collision_cols].any(axis=1) | df['Crash System Wakeup']

# Step 6: Loop per vehicle and check 20-second window
for vehicle_id, group in df.groupby('Vehicle Identification Number'):
    # Get times when collision happened
    collision_times = group.loc[group['collision'], 'DATE (UTC)']
    
    for collision_time in collision_times:
        # 20-second window before collision
        mask = (group['DATE (UTC)'] >= collision_time - pd.Timedelta(seconds=20)) & \
               (group['DATE (UTC)'] <= collision_time)
        
        # Check if Autopilot or Cruise Control was active in this window
        active = group.loc[mask].apply(
            lambda row: row['Autopilot System State'] in autopilot_active or 
                        row['Cruise Control State'] in cruise_active, axis=1)
        
        # If any row in the window was active, mark ADAS True
        if active.any():
            df.loc[mask, 'ADAS'] = True


# Step 7: Drop helper column if you want
df.drop(columns=['collision'], inplace=True)

#Number of crashes with ADAS active
print(df['ADAS'].value_counts())

# Optional: save the result
df.to_csv("adas_flagged_output.csv", index=False)

# Calculating the autopilot active time leading to the crash time. 

crash_time = pd.Timestamp("2024-10-24 00:19:03.578")

pre_crash_df = df[df["DATE (UTC)"] <= crash_time]

pre_crash_df["autopilot_active"] = (
    pre_crash_df["Autopilot System State"].isin(autopilot_active)
)

last_active_idx = pre_crash_df[pre_crash_df["autopilot_active"]].index.max()
autopilot_segment = pre_crash_df.loc[:last_active_idx]

# Find where Autopilot switches from inactive → active
transition_rows = autopilot_segment[
    (autopilot_segment["autopilot_active"]) &
    (~autopilot_segment["autopilot_active"].shift(1, fill_value=False))
]
autopilot_start_time = transition_rows["DATE (UTC)"].iloc[-1]

duration_seconds = (crash_time - autopilot_start_time).total_seconds()

print("Crash time:", crash_time)
print("Autopilot started at:", autopilot_start_time)
print("Autopilot active duration (seconds):", duration_seconds)

