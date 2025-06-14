import pandas as pd
from web3 import Web3
import time

# Step 1: Load data from Homework 1 CSV
df = pd.read_csv("patient_iot_data.csv")

# ✅ Ensure all columns are shown in the output
pd.set_option("display.max_columns", None)

print("✅ Loaded CSV data:")
print(df.head())

# Step 2: Connect to Ganache
ganache_url = "http://127.0.0.1:7545"  # Make sure Ganache is running on this port
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("✅ Connected to Ganache successfully!")
else:
    raise ConnectionError("❌ Connection failed. Ensure Ganache is running.")

# Step 3: Connect to your deployed contract
contract_address = web3.to_checksum_address("0xc6733449559a86e7504ebaa2eb94e3df262a34d5")


# ABI here (you can also import it from a .json file if preferred)
abi = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": False,
    "inputs": [
      {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"},
      {"indexed": False, "internalType": "string", "name": "patientID", "type": "string"},
      {"indexed": False, "internalType": "string", "name": "deviceId", "type": "string"},
      {"indexed": False, "internalType": "int256", "name": "temperature", "type": "int256"},
      {"indexed": False, "internalType": "uint256", "name": "heartBeat", "type": "uint256"},
      {"indexed": False, "internalType": "uint256", "name": "bpSystolic", "type": "uint256"},
      {"indexed": False, "internalType": "uint256", "name": "bpDiastolic", "type": "uint256"},
      {"indexed": False, "internalType": "uint256", "name": "oxygenSaturation", "type": "uint256"},
      {"indexed": False, "internalType": "uint256", "name": "respiratoryRate", "type": "uint256"}
    ],
    "name": "DataStored",
    "type": "event"
  },
  {
    "inputs": [
      {"internalType": "string", "name": "_patientID", "type": "string"},
      {"internalType": "string", "name": "_deviceId", "type": "string"},
      {"internalType": "int256", "name": "_temperature", "type": "int256"},
      {"internalType": "uint256", "name": "_heartBeat", "type": "uint256"},
      {"internalType": "uint256", "name": "_bpSystolic", "type": "uint256"},
      {"internalType": "uint256", "name": "_bpDiastolic", "type": "uint256"},
      {"internalType": "uint256", "name": "_oxygenSaturation", "type": "uint256"},
      {"internalType": "uint256", "name": "_respiratoryRate", "type": "uint256"}
    ],
    "name": "storeData",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalRecords",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
    "name": "getRecord",
    "outputs": [
      {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
      {"internalType": "string", "name": "patientID", "type": "string"},
      {"internalType": "string", "name": "deviceId", "type": "string"},
      {"internalType": "int256", "name": "temperature", "type": "int256"},
      {"internalType": "uint256", "name": "heartBeat", "type": "uint256"},
      {"internalType": "uint256", "name": "bpSystolic", "type": "uint256"},
      {"internalType": "uint256", "name": "bpDiastolic", "type": "uint256"},
      {"internalType": "uint256", "name": "oxygenSaturation", "type": "uint256"},
      {"internalType": "uint256", "name": "respiratoryRate", "type": "uint256"}
    ],
    "stateMutability": "view",
    "type": "function"
  }
]


contract = web3.eth.contract(address=contract_address, abi=abi)
web3.eth.default_account = web3.eth.accounts[0]
print(f"✅ Smart Contract loaded at {contract_address}")

# Step 4: Function to send data
def send_iot_data(row):
    txn = contract.functions.storeData(
        row["Patient ID"],
        row["Device ID"],
        int(row["Temperature (tenths °C)"]),
        int(row["Heart Rate (bpm)"]),
        int(row["BP Systolic"]),
        int(row["BP Diastolic"]),
        int(row["Oxygen Saturation (%)"]),
        int(row["Respiratory Rate"])
    ).transact({
        'from': web3.eth.default_account,
        'gas': 3000000
    })
    receipt = web3.eth.wait_for_transaction_receipt(txn)
    print(f"✅ Stored data for {row['Patient ID']} | Txn Hash: {receipt.transactionHash.hex()}")

# Step 5: Send each row to the blockchain
for _, row in df.iterrows():
    send_iot_data(row)
    time.sleep(1)

# Step 6: Verify blockchain storage
total_records = contract.functions.getTotalRecords().call()
print(f"\n📦 Total IoT records stored: {total_records}")

# Retrieve all data
all_data = []
for i in range(total_records):
    record = contract.functions.getRecord(i).call()
    all_data.append({
        "timestamp": record[0],
        "patient_id": record[1],
        "device_id": record[2],
        "temperature": record[3] / 10.0,  # Convert tenths to °C
        "heartBeat": record[4],
        "bpSystolic": record[5],
        "bpDiastolic": record[6],
        "oxygenSaturation": record[7],
        "respiratoryRate": record[8]
    })

df_clean = pd.DataFrame(all_data)
df_clean["timestamp"] = pd.to_datetime(df_clean["timestamp"], unit="s")
df_clean.fillna(0, inplace=True)

# Show and save cleaned data
print("\n📊 Cleaned Data Preview:")
print(df_clean.head())

df_clean.to_csv("cleaned_iot_data.csv", index=False)
print("✅ Cleaned data saved as cleaned_iot_data.csv")

first = contract.functions.getRecord(0).call()
print("\n🔍 First Stored Record:", first)

