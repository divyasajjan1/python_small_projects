# ADAS Pre-Crash Analysis

**Detect if ADAS (Autopilot or Cruise Control) was active before a vehicle crash.**

---

## Overview
This project processes vehicle telemetry data to identify whether ADAS systems were engaged **within 20 seconds before a collision**. It adds an `ADAS` column (`True`/`False`) to the dataset for analysis and reporting.  

---

## Features
- Detects all types of collisions using:
  - Collision Indicator columns (Frontal, Side, Rear, Rollover)  
  - Crash System Wakeup  
- Checks 20-second window prior to each crash  
- Flags rows where **Autopilot or Cruise Control** was active  

---

## Requirements
- Python 3.x  
- pandas  

Install dependencies:
```bash
pip install -r requirements.txt
