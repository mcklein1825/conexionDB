import requests

BASE_URL = "https://ep-old-morning-ae89tbp3.apirest.c-2.us-east-2.aws.neon.tech/neondb/rest/v1"

email = "mcklein1825@gmail.com"
password = "Mcklein141123"

session = requests.Session()

# 1. Iniciar sesión y obtener cookie de sesión
login_resp = session.post(
    f"{BASE_URL}/signIn/emailPassword",
    json={"email": email, "password": password},
)

if login_resp.status_code != 200:
    raise Exception("Error al iniciar sesión:", login_resp.text)

print("✅ Sesión iniciada. Cookies recibidas:", session.cookies.get_dict())

# 2. Llamar al endpoint interno que devuelve el JWT
#    Este endpoint es el que usa internamente authClient.token()
token_resp = session.get(f"{BASE_URL}/token")

if token_resp.status_code != 200:
    raise Exception("Error al obtener token:", token_resp.text)

jwt = token_resp.json().get("token")
print(f"✅ JWT obtenido: {jwt}")
