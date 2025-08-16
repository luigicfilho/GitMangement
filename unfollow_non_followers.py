import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get("GITHUB_USERNAME")
TOKEN = os.environ.get("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

if not USERNAME:
    USERNAME = github.repository_owner
    raise ValueError("Variável de ambiente GITHUB_USERNAME não está definida.")
if not TOKEN:
    TOKEN = secrets.GITHUB_TOKEN
    raise ValueError("Variável de ambiente GITHUB_TOKEN não está definida.")

def get_followers():
    url = f"https://api.github.com/users/{USERNAME}/followers?per_page=100"
    return fetch_all_pages(url)

def get_following():
    url = f"https://api.github.com/users/{USERNAME}/following?per_page=100"
    return fetch_all_pages(url)

def fetch_all_pages(url):
    items = []
    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro ao acessar {url}: {response.status_code} - {response.text}")
            break

        items.extend([user['login'] for user in response.json()])

        url = response.links['next']['url'] if 'next' in response.links else None
        time.sleep(0.5) 
    return items

def unfollow_user(username):
    url = f"https://api.github.com/user/following/{username}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Deixou de seguir: {username}")
    else:
        print(f"Falha ao deixar de seguir {username}: {response.status_code}")

def read_exceptions(filename="usersfollow.txt"):
    """Lê o arquivo de exceções e retorna um conjunto de usernames (ignorando linhas vazias e comentários)."""
    exceptions = set()
    if not os.path.exists(filename):
        print(f"⚠️ {filename} not found. No exceptions applied.")
        return exceptions
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"): 
                exceptions.add(stripped)
    print(f"Loaded {len(exceptions)} exception(s) from {filename}")
    return exceptions

def main():
    if not USERNAME or not TOKEN:
        print("GITHUB_USERNAME ou GITHUB_TOKEN não definidos.")
        return

    print("Buscando seguidores...")
    followers = set(get_followers())
    print(f"Você tem {len(followers)} seguidores.")

    print("Buscando pessoas que você segue...")
    following = set(get_following())
    print(f"Você está seguindo {len(following)} pessoas.")

    exceptions = read_exceptions()
    not_following_back = following - followers
    
    filtered_not_following_back = sorted(not_following_back - exceptions)
    print(f"{len(not_following_back)} pessoas não te seguem de volta.")

    if filtered_not_following_back:
        print("\n Começando a deixar de seguir...")
        for user in sorted(filtered_not_following_back):
            unfollow_user(user)
            time.sleep(1)
    else:
        print("Todos que você segue te seguem de volta!")

if __name__ == "__main__":
    main()