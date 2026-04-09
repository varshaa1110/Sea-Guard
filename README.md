# SEA GUARD – Maritime Monitoring System

## Project Overview

SEA GUARD is a smart maritime surveillance system designed to monitor ship activities within India's Exclusive Economic Zone (EEZ). The system uses AIS (Automatic Identification System) data to detect suspicious vessel behavior such as illegal fishing, abnormal movement, and dark activity (ships turning off AIS).

This project simulates a real-time maritime monitoring system used by authorities like the Coast Guard, Navy, Port authorities, Coast guard and others to ensure ocean security.

---

## Understanding EEZ (Exclusive Economic Zone)

The Exclusive Economic Zone (EEZ) is the sea area extending up to 200 nautical miles from a country's coastline, where the country has rights over marine resources and activities.

In this project:
- We focus on **India’s EEZ**
- All ship monitoring and detection happens within this zone

---

## Key Technologies Used

- **AIS (Automatic Identification System):**
  Provides ship data such as location, speed, and identity

- **SAR (Synthetic Aperture Radar) [Simulated]:**
  Used to detect ships even when AIS is turned OFF

---

## Objectives

- Monitor ship movements in real-time (simulated)
- Detect suspicious maritime activities
- Provide instant alerts to authorities
- Enable historical data analysis using time filters

---

## Features Explained in Detail

### 1. Role-Based Login System

- Users must log in to access the system
- Roles include:
  - Coast Guard
  - Navy
  - Port Authorities
  - Fishery Department
  - Others

- Login validation ensures only authorized access
- Uses session-based authentication (Streamlit session_state)

---

### 2. Dashboard (Central Monitoring System)

- Displays all ship data in tabular format
- Shows:
  - Total ships
  - AIS ON ships
  - AIS OFF ships
  - Total records

- Includes **time-based filtering system**

---

### 3. Time-Based Filtering

Users can analyze ship data across different time intervals:

- Now (real-time simulation)
- 1 hour ago
- 1 day ago
- 1 week ago
- 1 month ago
- All records

Purpose:
- Helps in tracking historical patterns
- Useful for investigation and analysis

---

### 4. AIS Status Monitoring

Ships are categorized into:

- 🟢 AIS ON → Normal ships
- 🔴 AIS OFF → Dark ships (highly suspicious)

Dark ships are considered risky as they hide their identity

---

### 5. SAR Simulation

- SAR is simulated to detect all ships
- If a ship is detected but AIS is OFF:
  → Marked as **Dark Activity**

---

### 6. Suspicious Activity Detection

The system uses rule-based logic to detect anomalies:

| Condition | Reason |
|----------|--------|
| Speed < 1 | Possible illegal fishing |
| Speed > 30 | Abnormal movement |
| AIS OFF | Dark activity |

Each suspicious ship is flagged with a reason.

---

### 7. Instant Alert System

- Alerts are generated immediately when suspicious activity is detected
- Includes:
  - 🔴 Critical alert (dark ships)
  - 🟡 Warning alert (multiple suspicious ships)

- Alerts are visually enhanced for clarity

---

### 8. Ship Tracking & Map Visualization

- Displays ship locations using map interface
- Users can:
  - View ship positions
  - Identify suspicious ships visually

---

### 9. Ship Tracking (Detailed View)

- Users can select a specific ship
- View details such as:
  - Speed
  - Location
  - Timestamp

---

### 10. Suspicious Ships Dashboard

- Displays all flagged ships
- Includes:
  - Ship ID
  - Reason for suspicion
  - Location

- Severity levels:
  - 🔴 High → AIS OFF
  - 🟡 Medium → Abnormal speed
  - 🟢 Low → Minor issues

---

### 11. Notification Simulation

- Includes a “Notify Authorities” feature
- Simulates real-world alert systems (SMS/email integration possible)

---

## System Workflow

1. Collect ship data (AIS)
2. Process and analyze ship behavior
3. Detect anomalies using rules
4. Generate alerts instantly
5. Display results in dashboard and maps

---

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy

---

## ▶️ How to Run the Project

```bash
pip install -r requirements.txt
streamlit run app.py
