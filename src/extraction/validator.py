import pandas as pd

def validate_statement(csv_path):
    """
    Performs a math check on the extracted CSV to ensure accuracy.
    """
    try:
        df = pd.read_csv(csv_path)
        
        # Clean Amount column: remove any non-numeric chars and convert to float
        df['Amount'] = pd.to_numeric(df['Amount'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        
        debits = df[df['Type'].str.contains('DEBIT', case=False, na=False)]['Amount'].sum()
        credits = df[df['Type'].str.contains('CREDIT', case=False, na=False)]['Amount'].sum()
        
        print("\n--- 🛡️ Validation Report ---")
        print(f"Total Transactions: {len(df)}")
        print(f"Total Money Spent (Debits):  ₹{debits:.2f}")
        print(f"Total Money Received (Credits): ₹{credits:.2f}")
        print(f"Net Change: ₹{(credits - debits):.2f}")
        print("---------------------------\n")
        
        return debits, credits
    except Exception as e:
        print(f"Validation error: {e}")
        return None, None

if __name__ == "__main__":
    # Test run
    validate_statement("data/processed/statement_cleaned.csv")
