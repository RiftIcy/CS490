import requests

# API endpoint
url = "https://student-info-api.netlify.app/.netlify/functions/submit_student_info"

# Data to be sent in JSON format
data = {
    "UCID": "lb356",
    "first_name": "Lior",
    "last_name": "Biton",
    "github_username": "RiftIcy",
    "discord_username": "rift_icy",
    "favorite_cartoon": "Adventure Time",
    "favorite_language": "Python",
    "movie_or_game_or_book": "CS:GO"
}

headers = { "Content-Type": "application/json"}

def validate_data(data):
    # Checks to see if all the JSON parameters are valid
    required = ["UCID", "first_name", "last_name", "github_username", "discord_username", "favorite_cartoon", "favorite_language", "movie_or_game_or_book"]
    invalid = False

    for field in required:
        if field not in data:
            print(f"Missing required field: {field}")
            invalid = True
        
        elif not isinstance(data[field], str):
            print(f"Field '{field}' must be a string.")
            invalid = True

    if invalid:
        print("\nData validation failed.\n")
        return False
    
    print("\nAll data validated successfully.\n")
    return True

def submit_student_info(data):
    print("Submitting student info...\n")
    
    try:
        # Send POST to url to add JSON to database
        response = requests.post(url, headers=headers, json=data)
        return response
    
    except requests.exceptions.RequestException as e:
        print(f"Request Error during POST: {e}\n")
        return None


def delete_student_info(ucid):
    print("Deleting student info...\n")

    try:
        # Send DELETE to url to delete JSON from database
        response = requests.delete(f"{url}?UCID={ucid}") # Can also use this on the website to see uploaded data
        return response
    
    except requests.exceptions.RequestException as e:
        print(f"Request Error during DELETE: {e}\n")
        return None

def get_student_info(ucid):
    print("Fetching student info...\n")

    try:
        # Send GET to url to get JSON information from database
        response = requests.get(f"{url}?UCID={ucid}")
        if response.status_code == 200:
            print("Data fetched successfully:\n")
            print_response("GET", response)

        else:
            print("Failed to fetch data.\n")
            print_response("GET", response)

    except requests.exceptions.RequestException as e:
        print(f"Request Error during GET: {e}\n")

def print_response(label, response):
    if response is None:
        print(f"{label} failed: No response received\n")
        return
    
    print(f"{label} Status: {response.status_code}")

    if response.text:
        print(f"{label} Body: {response.text}\n")
    else:
        print("No response provided.\n")
        
def main():

    # Validate data
    print("Validating data...\n")
    
    if not validate_data(data):
        return
    
    # Attempt to submit student info
    response = submit_student_info(data)

    if response is None:
        return
    
    if response.status_code == 200:
        print("Student info submitted successfully.\n")

        # Print the status and response
        print_response("POST", response)
        
        get_student_info(data["UCID"])
    
    elif response.status_code == 409:
        print("Data already exists.\n")
        print_response("POST", response)

        print("Attempting to delete...\n")

        delete_response = delete_student_info(data["UCID"])


        if delete_response and delete_response.status_code == 200:
            print("Deleted existing record.\n")

            # Print the status and response
            print_response("DELETE", delete_response)

            print("Resubmitting...\n")

            response = submit_student_info(data)

            if response and response.status_code == 200:
                print("Resubmission successful.\n")
                print_response("POST", response)

                get_student_info(data["UCID"])

            else:
                print("Resubmission failed.\n")
                print_response("POST", response)
        else:
            print("Failed to delete existing record.\n")
            print_response("DELETE", delete_response)
    else:
        print("Failed to submit data.\n")
        print_response("POST", response)
        
if __name__ == "__main__":
    main()