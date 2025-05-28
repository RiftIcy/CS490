import requests

def delete_submission():
    ucid = "lb356"  # Replace with your actual UCID
    base_url = "https://student-info-api.netlify.app/.netlify/functions/submit_student_info"

    print(f"Attempting to delete record for UCID: {ucid}...")
    delete_response = requests.delete(f"{base_url}?UCID={ucid}")
    print("DELETE Status:", delete_response.status_code)
    print("DELETE Response:", delete_response.text)

if __name__ == "__main__":
    delete_submission()