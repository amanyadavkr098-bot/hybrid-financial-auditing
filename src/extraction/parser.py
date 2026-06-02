import csv
import re
import os

def extract_transactions(md_text, output_csv):
    rows = []
    current_txn = None
    lines = md_text.splitlines()

    for line in lines:
        line = line.strip()
        if not line.startswith("|"): continue
        if "Date" in line or "---" in line: continue

        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) != 4: continue

        col1, col2, col3, col4 = cols   

        # CASE 1: NEW TRANSACTION START
        if re.search(r'[A-Za-z]{3}\s+\d{2},\s+\d{4}', col1):
            if current_txn:
                rows.append([current_txn["date"], current_txn["time"], current_txn["merchant"], 
                             current_txn["amount"], current_txn["type"], current_txn["transaction_id"], current_txn["utr"]])

            current_txn = {"date": "", "time": "", "merchant": "", "amount": "", "type": "", "transaction_id": "", "utr": ""}

            if "<br>" in col1:
                dt_parts = col1.split("<br>")
                if len(dt_parts) >= 2:
                    current_txn["date"] = dt_parts[0].strip()
                    current_txn["time"] = dt_parts[1].strip()
            else:
                current_txn["date"] = col1.strip()

            merchant_match = re.search(r'(?:Paid to|Received from)\s+(.*?)(?:<br>|$)', col2, re.IGNORECASE)
            if merchant_match: current_txn["merchant"] = merchant_match.group(1).strip()

            txn_match = re.search(r'Transaction ID\s*(T\d+)', col2, re.IGNORECASE)
            if txn_match: current_txn["transaction_id"] = txn_match.group(1)

            utr_match = re.search(r'UTR No\.?\s*(\d+)', col2, re.IGNORECASE)
            if utr_match: current_txn["utr"] = utr_match.group(1)

            current_txn["type"] = col3.strip().upper()
            current_txn["amount"] = col4.replace("₹", "").replace(",", "").replace("â‚¹", "").strip()

        # CASE 2: CONTINUATION ROW
        elif current_txn:
            time_match = re.search(r'\d{1,2}:\d{2}\s*[ap]m', col1, re.IGNORECASE)
            if time_match: current_txn["time"] = time_match.group()

            txn_match = re.search(r'Transaction ID\s*(T\d+)', col2, re.IGNORECASE)
            if txn_match: current_txn["transaction_id"] = txn_match.group(1)

            utr_match = re.search(r'UTR No\.?\s*(\d+)', col2, re.IGNORECASE)
            if utr_match: current_txn["utr"] = utr_match.group(1)

    if current_txn:
        rows.append([current_txn["date"], current_txn["time"], current_txn["merchant"], 
                     current_txn["amount"], current_txn["type"], current_txn["transaction_id"], current_txn["utr"]])

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Time", "Merchant", "Amount", "Type", "TransactionID", "UTR"])
        writer.writerows(rows)

    print(f"Successfully extracted {len(rows)} transactions.")
    return True

# This allows main.py to call this function
if __name__ == "__main__":
    md_file_path = "data/interim/statement__1/statement.md"
    output_csv_path = "data/processed/statement_cleaned_v2.csv"
    with open(
        md_file_path,
        "r",
        encoding="utf-8"
    ) as f:
        md_text = f.read()

    extract_transactions(
        md_text,
        output_csv_path
    )