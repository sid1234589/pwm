import pandas as pd
import random
import datetime

names = ["Ramesh Gupta", "Meena Shah", "John Doe", "Sara Ali", "David Kim", "Nina Singh", "Wei Zhang", "Ali Khan", "Priya Nair", "Carlos Gomez"]
countries = ["India", "USA", "UAE", "China", "UK", "Singapore", "Pakistan"]
account_types = ["Individual", "Joint", "Trust"]
checkmark = ["✅", "❌"]
approvers = ["", "", "", "Amit Patel", "Linda Wong"]

clients = []

for i in range(10):
    cid = f"C100{i+1}"
    name = names[i]
    country = random.choice(countries)
    acc_type = random.choice(account_types)
    kyc = random.choices(checkmark, weights=[0.8, 0.2])[0]
    id_proof = random.choices(checkmark, weights=[0.85, 0.15])[0]
    fatca = random.choices(checkmark, weights=[0.7, 0.3])[0]

    req_date = datetime.date.today() - datetime.timedelta(days=random.randint(5, 15))
    proc_date = req_date + datetime.timedelta(days=random.randint(1, 5))
    tat = (proc_date - req_date).days

    risk = "High" if kyc == "❌" or id_proof == "❌" else ("Medium" if fatca == "❌" else "Low")
    
    closure_status = random.choices(["-", "Closed", "Pending"], weights=[0.5, 0.3, 0.2])[0]
    closure_date = proc_date + datetime.timedelta(days=random.randint(5, 10)) if closure_status == "Closed" else ""
    approver = random.choice(approvers)

    clients.append({
        "Client ID": cid,
        "Client Name": name,
        "Country": country,
        "Account Type": acc_type,
        "KYC": kyc,
        "ID Proof": id_proof,
        "FATCA": fatca,
        "Risk Level": risk,
        "Request Date": req_date,
        "Processed Date": proc_date,
        "TAT": tat,
        "Maintenance": "-",
        "Closure Status": closure_status,
        "Closure Date": closure_date,
        "Approver": approver
    })

df = pd.DataFrame(clients)
df.to_csv("clients.csv", index=False)
print("✅ Dummy client data generated successfully.")
