import ollama
import pandas as pd
import os
def extract_csv_from_markdown(md_file_path,output_csv_path):
    """
    Extract table from markdown file and save it as a csv file.
    """

    with open(md_file_path,"r",encoding="utf-8") as f:
        md_text=f.read()


    prompt=f"""You are a financial data expert. Convert the following Markdown bank statement into a strict CSV.
    
    COLUMNS: Date, Time, Merchant, Amount, Type, TransactionID, UTR
    
    RULES:
    1. Output ONLY the CSV raw text. No introduction or explanation.
    2. Amount must be a number only (no currency symbols).
    3. One transaction per line.
    4. If a field is missing, leave it empty.
    
    MARKDOWN TEXT:
    {md_text}
    """

    try:
        print("Sending the data to llama for parsing ...")
        response=ollama.generate(model="llama3",prompt=prompt)
        csv_content=response['response']
        clean_csv=csv_content.replace("```csv","").replace("```","").strip()
        with open(output_csv_path,"w",encoding="utf-8") as f:
            f.write(clean_csv)

        print(f"Successfully extracted CSV and saved to {output_csv_path}")
        return True
    except Exception as e:
        print(f"Error extracting CSV: {e}")
        return False
if __name__=="__main__":
    md_file_path="data/interim/statement.md"
    output_csv_path="data/processed/statement.csv"
    extract_csv_from_markdown(md_file_path,output_csv_path)