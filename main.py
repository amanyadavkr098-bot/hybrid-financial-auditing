from pathlib import Path
from src.extraction.marker_run import run_marker
from src.extraction.parser import extract_transactions
from src.extraction.validator import validate_statement

# Paths
PDF_PATH = "data/raw/PhonePe_Statement_May2026_May2026.pdf"
MD_FOLDER = "data/interim"
CSV_PATH = "data/processed/statement_cleaned.csv"


def main():

    # Step 1: PDF -> Markdown
    if run_marker(PDF_PATH, MD_FOLDER):

        # Search recursively for markdown files
        md_files = list(Path(MD_FOLDER).rglob("*.md"))

        if not md_files:
            print("Error: Marker did not produce a markdown file.")
            return

        # Take first markdown file found
        full_md_path = md_files[0]
        print(f"Markdown found: {full_md_path}")

        # Read markdown text
        with open(full_md_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        # Step 2: Markdown -> CSV
        if extract_transactions(md_text, CSV_PATH):

            # Step 3: Validate math
            validate_statement(CSV_PATH)


if __name__ == "__main__":
    main()