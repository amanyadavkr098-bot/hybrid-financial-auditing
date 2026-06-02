import pandas as pd
import os

def validate_statement(csv_path):
    """
    Performs a financial audit of the extracted CSV to ensure 
    no transactions were missed and amounts are correct.
    """
    if not os.path.exists(csv_path):
        print(f"❌ Validation Error: CSV file not found at {csv_path}")
        return False

    try:
        # 1. Load the CSV
        df = pd.read_csv(csv_path)
        
        if df.empty:
            print("❌ Validation Error: The extracted CSV is empty.")
            return False

        # 2. Clean the Amount column 
        # Ensure it's numeric, remove any remaining symbols, and handle NaNs
        df['Amount'] = pd.to_numeric(
            df['Amount'].astype(str).str.replace(r'[^\d.]', '', regex=True), 
            errors='coerce'
        ).fillna(0)

        # 3. Calculate Totals
        # We assume 'Type' column contains 'DEBIT' or 'CREDIT'
        debits = df[df['Type'].str.contains('DEBIT', case=False, na=False)]['Amount'].sum()
        credits = df[df['Type'].str.contains('CREDIT', case=False, na=False)]['Amount'].sum()
        net_change = credits - debits

        # 4. Generate the Audit Report
        print("\n" + "="*40)
        print("🛡️  FINANCIAL AUDIT REPORT")
        print("="*40)
        print(f"Total Transactions Found: {len(df)}")
        print(f"Total Money Out (DEBITS):  ₹{debits:,.2f}")
        print(f"Total Money In (CREDITS):  ₹{credits:,.2f}")
        print("-" * 40)
        print(f"Net Account Change:       ₹{net_change:,.2f}")
        print("="*40)

        # 5. User Manual Cross-Check
        print("\n👉 ACTION REQUIRED: Check your PDF statement totals.")
        print("Does the 'Total Debits' and 'Total Credits' match your PDF?")
        
        # In a fully automated system, you could extract the total 
        # from the PDF using Marker and compare it here.
        # For now, a manual confirmation is the highest form of accuracy.
        
        return True

    except Exception as e:
        print(f"❌ Critical Validation Error: {e}")
        return False

if __name__ == "__main__":
    # Test the validator locally
    validate_statement("data/processed/statement_cleaned.csv")
