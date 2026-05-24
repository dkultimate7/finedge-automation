import requests
import json
import sys

def main():
    # Step 1: Generate Webhook
    generate_url = "https://api.finedge.ai/hiring/generateWebhook/PYTHON"
    payload = {
        "name": "Devansh Khandelwal",
        "regNo": "22BCE287",
        "email": "devansh@gmail.com"
    }
    
    print("Sending request to generate webhook...")
    try:
        response = requests.post(generate_url, json=payload)
        response.raise_for_status()
        data = response.json()
        webhook_url = data.get("webhook")
        access_token = data.get("accessToken")
        
        print(f"Received webhook: {webhook_url}")
        print(f"Received accessToken: {access_token[:10]}...")
    except requests.exceptions.RequestException as e:
        print(f"Error generating webhook: {e}")
        if e.response is not None:
            print("Response:", e.response.text)
        sys.exit(1)

    # Step 2: Final SQL Query
    sql_query = """
SELECT d.department_name, e.name AS employee_name, e.salary
FROM EMPLOYEE e
JOIN DEPARTMENT d ON e.department_id = d.id
JOIN (
    SELECT department_id, MAX(salary) AS max_salary
    FROM EMPLOYEE
    GROUP BY department_id
) m ON e.department_id = m.department_id AND e.salary = m.max_salary;
""".strip()

    # Step 3: Send Final Query
    submission_url = "https://api.finedge.ai/hiring/testWebhook/PYTHON"
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    submission_payload = {
        "finalQuery": sql_query
    }
    
    print("Sending final SQL query...")
    try:
        submit_response = requests.post(submission_url, headers=headers, json=submission_payload)
        submit_response.raise_for_status()
        print("Submission successful!")
        print("Response:", submit_response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error submitting query: {e}")
        if e.response is not None:
            print("Response details:", e.response.text)
        sys.exit(1)

if __name__ == "__main__":
    main()
