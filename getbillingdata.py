import os
import re
from datetime import datetime, timedelta
import logging
from supabase import create_client, Client

# Define folder_path and hotel_id
folder_path = "smdr/copy"
hotel_id = "1"

# Configure logging to a file
log_filename = "logfile.log"
failed_filename = "failed.txt"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define Supabase URL and API Key
supabase_url = "End Point URL"
supabase_key = "API Key"

# Create a Supabase client
supabase = create_client(supabase_url, supabase_key)

def read_and_split_files(folder_path):
    if not os.path.exists(folder_path):
        logging.error(f"The folder '{folder_path}' does not exist.")
        print(f"The folder '{folder_path}' does not exist.")
        return

    all_file_data = []  # Initialize an empty list to store all data from files

    # Define the regular expression pattern
    pattern = re.compile(r'(\d{2}.\d{2}.\d{2})(\d{2}:\d{2}:\d{2})\s+(\d+)\s+(\d+)\s+(\d{2}:\d{2}:\d{2})(\d+)(\d)\s+(\d)\s+(\d)')

    # Get the current time
    current_time = datetime.now()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is a .txt file and within the last hour
        if filename.endswith(".txt") and os.path.isfile(file_path) and \
                current_time - datetime.fromtimestamp(os.path.getmtime(file_path)) <= timedelta(hours=720):
            with open(file_path, "r") as file:
                content = file.read().strip()  # Remove leading/trailing whitespace
                if content:  # Check if content is non-empty
                    # Use the regular expression to match and format the data
                    matches = [list(match.groups()) for line in content.splitlines() for match in re.finditer(pattern, line)]
                    all_file_data.extend(matches)

    # Insert data into Supabase
    try:
        failed_attempts = []  # Initialize a list to store failed attempts

        # Insert data into Supabase based on the provided mapping
        for data in all_file_data:
            logging.info(f"Inserting data: {data}")  # Log the data

            # Format the date as 'YYYY-MM-DD'
            date = datetime.strptime(data[0], "%d.%m.%y").strftime("%Y-%m-%d")

            # Use the time value directly
            time = data[1]

            extension = data[3]

            # Format the duration as 'HH:MI:SS'
            duration_parts = list(map(int, data[4].split(':')))
            duration_str = f"{duration_parts[0]:02d}:{duration_parts[1]:02d}:{duration_parts[2]:02d}"

            destination = data[5]

            # Check if the record exists
            existing_record = supabase.table('call_billing_list').select('*').eq('date', date).eq('start', time).execute()

            if 'data' in existing_record:
                # If record exists, update it
                response = supabase.table('call_billing_list').update({
                    "date": date,
                    "start": time,
                    "extension": extension,
                    "duration": duration_str,
                    "destination": destination,
                    "hotel_id": hotel_id
                }).eq('date', date).eq('start', time).execute()
            else:
                # If record doesn't exist, insert it
                response = supabase.table('call_billing_list').insert({
                    "date": date,
                    "start": time,
                    "extension": extension,
                    "duration": duration_str,
                    "destination": destination,
                    "hotel_id": hotel_id
                }).execute()

            if 'data' in response:
                logging.info("Data successfully inserted/updated in Supabase.")
            else:
                logging.info(f"Failed to insert/update data in Supabase. Response: {response}")
                failed_attempts.append(data)

        # Log failed attempts to a file
        with open(failed_filename, 'a') as failed_file:
            for failed_data in failed_attempts:
                failed_file.write(','.join(failed_data) + '\n')

    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")

# Example usage:
read_and_split_files(folder_path)
