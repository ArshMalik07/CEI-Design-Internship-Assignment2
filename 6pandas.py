import requests
import time

# Function to fetch ISS location data from API with exponential backoff
def fetch_iss_location():
    url = "http://api.open-notify.org/iss-now.json"
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=10)  # Set timeout to 10 seconds
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting before retrying...")
                time.sleep(60)  # Wait for 1 minute if rate limited
                retries += 1
                continue
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            if 'timestamp' in data and 'iss_position' in data and 'latitude' in data['iss_position'] and 'longitude' in data['iss_position']:
                return data['timestamp'], data['iss_position']['latitude'], data['iss_position']['longitude']
            else:
                print("Unexpected data format received.")
                return None, None, None
        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"Attempt {retries} failed: {e}")
            if retries < max_retries:
                delay = 2 ** retries  # Exponential backoff: wait 2^retries seconds
                print(f"Retrying after {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries exceeded. Exiting...")
                return None, None, None

# Function to write ISS location data to CSV file
def write_to_csv(records=100):
    with open('iss_location_data.csv', 'w') as file:  # Use 'a' for append mode if needed
        file.write("Timestamp,Latitude,Longitude\n")  # Write header if file is new
        for _ in range(records):
            timestamp, latitude, longitude = fetch_iss_location()
            if timestamp is not None:
                file.write(f"{timestamp},{latitude},{longitude}\n")
            else:
                print("Failed to fetch data. Exiting...")
                return
            time.sleep(1)  # Pause for 1 second between each request

    print(f'{records} records have been written to iss_location_data.csv')

# Execute the program
write_to_csv(records=100)
