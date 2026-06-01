import ollama
import re


def clean_llm_response(text):
    """
    Cleans LLM output and keeps only CSV rows.
    """

    # Remove markdown code blocks
    text = re.sub(r"```(?:csv)?", "", text)
    text = text.replace("```", "").strip()

    lines = text.splitlines()
    cleaned_lines = []

    header = "Date,Time,Merchant,Amount,Type,TransactionID,UTR"

    found_header = False

    for line in lines:
        line = line.strip()

        # detect csv header
        if header.lower() in line.lower():
            found_header = True

            # avoid duplicate headers
            if header not in cleaned_lines:
                cleaned_lines.append(header)

            continue

        # Keep only lines that look like CSV rows
        if found_header:
            comma_count = line.count(",")

            # Expected 7 columns = 6 commas
            if comma_count == 6:
                cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def extract_csv_from_markdown(md_file_path, output_csv_path):
    """
    Extract transactions from markdown using chunked LLM parsing.
    """

    try:
        with open(md_file_path, "r", encoding="utf-8") as f:
            md_text = f.read()

        print("Chunking markdown...")

        # Smaller chunks = better instruction following
        chunk_size = 3000

        chunks = [
            md_text[i:i + chunk_size]
            for i in range(0, len(md_text), chunk_size)
        ]

        print(f"Total chunks: {len(chunks)}")

        all_csv_outputs = []

        for idx, chunk in enumerate(chunks):

            print(f"Processing chunk {idx+1}/{len(chunks)}...")

            prompt = f"""
SYSTEM:
You are a CSV extraction engine.

You are NOT a chatbot.
You are NOT an analyst.
You are NOT allowed to summarize.
You are NOT allowed to explain.

If you output anything except valid CSV, the task is FAILED.

TASK:
Extract ONLY financial transaction rows from the markdown.

REQUIRED CSV HEADER:
Date,Time,Merchant,Amount,Type,TransactionID,UTR

RULES:
- Output ONLY CSV
- No explanations
- No markdown
- No notes
- No bullet points
- No summaries
- No analysis
- No disclaimer
- Ignore non-transaction text
- Each row MUST contain exactly 7 columns
- If a field is missing, leave blank

BAD OUTPUT EXAMPLE:
"This statement contains multiple transactions..."

GOOD OUTPUT EXAMPLE:
Date,Time,Merchant,Amount,Type,TransactionID,UTR
2026-03-01,09:17 PM,EKART,110,DEBIT,T26051,7988
2026-03-01,10:22 AM,MEDPLUS,91,DEBIT,T26052,5707

MARKDOWN:
{chunk}
"""

            response = ollama.generate(
                model="llama3",
                prompt=prompt
            )

            raw_response = response["response"]

            cleaned_csv = clean_llm_response(raw_response)

            if cleaned_csv.strip():
                all_csv_outputs.append(cleaned_csv)

        # Merge chunks
        final_csv = []

        header_added = False

        for chunk_csv in all_csv_outputs:

            lines = chunk_csv.splitlines()

            for line in lines:

                if line.startswith("Date,Time"):

                    if not header_added:
                        final_csv.append(line)
                        header_added = True

                else:
                    final_csv.append(line)

        # Save final CSV
        with open(output_csv_path, "w", encoding="utf-8") as f:
            f.write("\n".join(final_csv))

        print(f"\nCSV saved to: {output_csv_path}")
        return True

    except Exception as e:
        print(f"Error extracting CSV: {e}")
        return False


if __name__ == "__main__":

    md_file_path = "data/interim/statement/statement.md"
    output_csv_path = "data/processed/statement_cleaned_v2.csv"

    extract_csv_from_markdown(
        md_file_path,
        output_csv_path
    )