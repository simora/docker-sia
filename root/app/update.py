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

def get_releases(version = None):
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
        return json.loads(response.text)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if args.check:
    releases = get_releases()
    try:
        soup = BeautifulSoup(releases[0]["description_html"], 'html.parser')
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    for link in soup.find_all('a'):
        if 'linux-amd64' in link.get('href'):
            print(releases[0]["name"])
            sys.exit(0)
    print("Unable to find download")
    sys.exit(1)

if not args.output:
    print("Missing output directory")
    sys.exit(1)
if not os.path.isdir(args.output):
    print("Provided path is invalid or doesn't exist")
    sys.exit(1)

if not args.version or args.version.lower() == "latest":
    args.version = None

releases = get_releases(args.version)
if isinstance(releases, list):
    soup = BeautifulSoup(releases[0]["description_html"], 'html.parser')
else:
    soup = BeautifulSoup(releases["description_html"], 'html.parser')
for link in soup.find_all('a'):
    if 'linux-amd64' in link.get('href'):
        filename = link.get('href').split('/')[-1]
        if not args.dry_run:
            r = requests.get(link.get('href'), allow_redirects=True)
            open(os.path.join(args.output, filename), 'wb').write(r.content)
        print(os.path.join(args.output, filename))
        sys.exit(0)
print('Failed to find download')
sys.exit(1)
