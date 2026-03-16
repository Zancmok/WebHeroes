import http.client
import ssl

# Target server
HOST = "localhost"
PORT = 443
PATH = "/ping"

# Create an SSL context (for self-signed certificates, we can skip verification)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # skip cert verification for local dev

# Create HTTPS connection
conn = http.client.HTTPSConnection(HOST, PORT, context=context)

try:
    conn.request("POST", PATH)
    response = conn.getresponse()
    print("Status:", response.status)
    print("Reason:", response.reason)
    print("Headers:", response.getheaders())
    body = response.read()
    print("Body:", body.decode('utf-8', errors='ignore'))
except Exception as e:
    print("Error:", e)
finally:
    conn.close()
