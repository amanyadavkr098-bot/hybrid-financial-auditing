from src.extraction.marker_run import run_marker
from src.extraction.parser import extract_csv_from_markdown
from src.extraction.validator import validate_statement
import os


PDF_PATH = "data/raw/statement.pdf"
MD_FOLDER = "data/interim"
CSV_PATH = "data/processed/statement_cleaned.csv"

def main():
    if run_marker(PDF_PATH,MD_FOLDER):
        # 1  searching for .md file
        folder_name = os.listdir(MD_FOLDER)[0]
        statement_folder = os.path.join(MD_FOLDER, folder_name)

        md_file = [f for f in os.listdir(statement_folder) if f.endswith(".md")]

        full_md_path = os.path.join(statement_folder, md_file[0])

        #  2  extracting csv from markdown
        if extract_csv_from_markdown(full_md_path,CSV_PATH):
            #  3  validating the extracted CSV
            validate_statement(CSV_PATH)

if __name__=="__main__":
    main()
