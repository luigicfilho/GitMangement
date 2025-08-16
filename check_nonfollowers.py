import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get("GITHUB_USERNAME")
TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

if not USERNAME:
    raise ValueError("Variável de ambiente GITHUB_USERNAME não está definida.")
if not TOKEN:
    raise ValueError("Variável de ambiente GITHUB_TOKEN não está definida.")

def get_list(type_):
    assert type_ in ["followers", "following"]
    users = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USERNAME}/{type_}?page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"GitHub API error while fetching {type_}: {response.status_code}")
        data = response.json()
        if not data:
            break
        users.extend([u["login"] for u in data])
        page += 1
    return set(users)

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

def save_followers_to_file(username, followers):
    date_str = datetime.now().strftime("%Y-%m-%d")
    base_filename = f"check_{username}_{date_str}"
    filename = f"{base_filename}.txt"   
    
    counter = 1
    while os.path.exists(filename):
        filename = f"{base_filename}_{counter}.txt"
        counter += 1
    
    with open(filename, "w", encoding="utf-8") as f:
        for follower in followers:
            f.write(f"{follower}\n")

    print(f"\nSaved {len(followers)} followers to: {filename}")

def main():
    if not USERNAME:
        raise EnvironmentError("GITHUB_USERNAME environment variable is not set.")
    
    followers = get_list("followers")
    following = get_list("following")

    exceptions = read_exceptions()
    not_following_back = following - followers
    
    filtered_not_following_back = sorted(not_following_back - exceptions)
    #save_followers_to_file(USERNAME, filtered_not_following_back)

    print(f"\nYou follow {len(following)} people.")
    print(f"You have {len(followers)} followers.")
    print(f"{len(filtered_not_following_back)} don't follow you back:\n")

    for user in filtered_not_following_back:
        print(f"- {user}")

if __name__ == "__main__":
    main()
