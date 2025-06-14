import random
import time
import pandas as pd

# Function to simulate patient IoT health data with unique device IDs
def generate_patient_iot_data(samples=50):
    """
    Generates simulated patient IoT health data matching smart contract format.
    
    Parameters:
    samples (int): Number of data points to generate.
    
    Returns:
    pd.DataFrame: A DataFrame containing simulated patient health IoT data.
    """
    data = []

    for i in range(samples):
        patient_id = f"PAT{str(i+1).zfill(3)}"
        device_id = f"Device_{str(i+1).zfill(3)}"  # ✅ Unique device ID per sample
        temperature = random.randint(350, 400)  # Tenths of °C (e.g., 375 = 37.5°C)
        heart_rate = random.randint(60, 100)    # Normal bpm
        bp_systolic = random.randint(110, 140)
        bp_diastolic = random.randint(70, 90)
        oxygen_saturation = random.randint(90, 100)
        respiratory_rate = random.randint(12, 20)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        data.append([
            patient_id,
            device_id,
            temperature,
            heart_rate,
            bp_systolic,
            bp_diastolic,
            oxygen_saturation,
            respiratory_rate,
            timestamp
        ])

        time.sleep(2)  # Simulate real-time data collection

    return pd.DataFrame(data, columns=[
        "Patient ID", "Device ID", "Temperature (tenths °C)", "Heart Rate (bpm)",
        "BP Systolic", "BP Diastolic", "Oxygen Saturation (%)",
        "Respiratory Rate", "Timestamp"
    ])

# Generate and save the data
iot_health_data = generate_patient_iot_data(50)
print(iot_health_data)

iot_health_data.to_csv("patient_iot_data.csv", index=False)