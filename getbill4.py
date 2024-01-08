import os
import re
import logging
from datetime import datetime, timedelta
import requests

# Define folder_path and hotel_id
folder_path = "smdr/copy"
hotel_id = "1"

# Configure logging to a file
log_filename = "logfile.log"
failed_filename = "failed.txt"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define API URL and Headers
api_url = "https://qeuhwbauvxyevuvjnrcw.supabase.co/rest/v1/call_billing_list"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFldWh3YmF1dnh5ZXZ1dmpucmN3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMzY0NDI5NiwiZXhwIjoyMDE5MjIwMjk2fQ.YrobOni-rdd5MB8OXqHcfLptEEGtaLILgFHCeFM0FSE",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFldWh3YmF1dnh5ZXZ1dmpucmN3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMzY0NDI5NiwiZXhwIjoyMDE5MjIwMjk2fQ.YrobOni-rdd5MB8OXqHcfLptEEGtaLILgFHCeFM0FSE",
    "Content-Type": "application/json"
}

def read_and_split_files(folder_path):
    if not os.path.exists(folder_path):
        logging.error("The folder '{}' does not exist.".format(folder_path))
        print("The folder '{}' does not exist.".format(folder_path))
        return

    all_file_data = []

    pattern = re.compile(r'(\d{2}.\d{2}.\d{2})(\d{2}:\d{2}:\d{2})\s+(\d+)\s+(\d+)\s+(\d{2}:\d{2}:\d{2})(\d+)(\d)\s+(\d)\s+(\d)')

    current_time = datetime.now()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".txt") and os.path.isfile(file_path) and \
                current_time - datetime.fromtimestamp(os.path.getmtime(file_path)) <= timedelta(hours=720):
            with open(file_path, "r") as file:
                content = file.read().strip()
                if content:
                    matches = [list(match.groups()) for line in content.splitlines() for match in re.finditer(pattern, line)]
                    all_file_data.extend(matches)

    try:
        failed_attempts = []

        for data in all_file_data:
            logging.info("Processing data: {}".format(data))

            # [existing code to format the data]

            record = {
                "date": date,
                "start": time,
                "extension": extension,
                "duration": duration_str,
                "destination": destination,
                "hotel_id": hotel_id
            }

            response = requests.post(api_url, json=record, headers=headers)

            if response.status_code in [200, 201]:
                logging.info("Data successfully inserted/updated in Supabase.")
            else:
                logging.error("Failed to insert/update data in Supabase. Response: {}".format(response.text))
                failed_attempts.append(data)

        with open(failed_filename, 'a') as failed_file:
            for failed_data in failed_attempts:
                failed_file.write(','.join(failed_data) + '\n')

    except Exception as e:
        logging.error("Error: {}".format(e))
        print("Error: {}".format(e))

# Example usage
read_and_split_files(folder_path)
