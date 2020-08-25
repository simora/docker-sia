import requests, json, sys, argparse, os
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="Update Sia from NebulousLabs Gitlab releases")
parser.add_argument("-v", "--version", help="version to download")
parser.add_argument("-d", "--dry-run",
    help="don't download just return the filename that would have been the downloaded file",
    action="store_true")
parser.add_argument("-c", "--check",
    help="don't download just return the latest version",
    action="store_true")
parser.add_argument("-o", "--output", help="output directory to write downloaded file to")
args = parser.parse_args()

def get_release(version = None):
    if not version:
        url = "https://gitlab.com/api/v4/projects/7508674/releases/"
    else:
        url = f"https://gitlab.com/api/v4/projects/7508674/releases/{version}"
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Failed to properly retrieve releases")
        sys.exit(1)
    if response.status_code != 200:
        print("Failed to properly retrieve releases")
        sys.exit(1)
    try:
        return json.loads(response.text)['name']
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def get_download_url(version):
    try:
        response = requests.get(f"https://gitlab.com/api/v4/projects/7508674/releases/{version}")
    except requests.exceptions.RequestException as e:
        print("Failed to properly retrieve releases")
        sys.exit(1)
    if response.status_code != 200:
        print("Failed to properly retrieve releases")
        sys.exit(1)

    soup = BeautifulSoup(json.loads(response.text)["description_html"], 'html.parser')
    for link in soup.find_all('a'):
        if 'linux-amd64' in link.get('href'):
            return link.get('href')
    return f"https://sia.tech/releases/Sia-v{version}-linux-amd64.zip"


if args.check:
    print(get_release())
    sys.exit(0)

if not args.output:
    print("Missing output directory")
    sys.exit(1)
if not os.path.isdir(args.output):
    print("Provided path is invalid or doesn't exist")
    sys.exit(1)

if not args.version or args.version.lower() == "latest":
    args.version = None

release = get_release(args.version)
download_url = get_download_url(release)
try:
    r = requests.get(download_url, allow_redirects=True)
    open(os.path.join(args.output, filename), 'wb').write(r.content)
    print(os.path.join(args.output, filename))
    sys.exit(0)
except Exception as e:
    print('Failed to find download')
    sys.exit(1)
