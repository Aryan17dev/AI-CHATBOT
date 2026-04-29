import csv
import os

def log_to_csv(agreement_type, data_dict):
    """
    Logs the submitted form data into a local CSV file.
    """
    file_path = f"{agreement_type}_logs.csv"
    file_exists = os.path.exists(file_path)
    
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data_dict.keys())
        
        if not file_exists:
            writer.writeheader()  # Write column names directly from dictionary keys
            
        writer.writerow(data_dict)
