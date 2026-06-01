import subprocess
import os
#subrprocess to run it in command line
def run_marker(pdf_path,output_path):
    """
    Run the marker tool on the given PDF file and save the output to the specified path."""
    
    try:
        print(f"Running marker on : {pdf_path} ...")
        command=[
            "marker_single",
            pdf_path,
            output_path,
            "--batch_multiplier",2
        ]
        # equivalent to running the command in the terminal

        subprocess.run(command, check=True)
        #check if the command was successful, if not it will raise an error
        print(f"Successfully converted {pdf_path} to Markdown.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running marker: {e}")
        return False
if __name__ == "__main__":
    #used when directly running the script, it will execute the code inside this block
    input_pdf = "data/raw/statement.pdf" 
    output_folder = "data/interim"
    run_marker(input_pdf, output_folder)