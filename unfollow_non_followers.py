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
    raise ValueError("The Environment variable GITHUB_USERNAME is not defined.")
if not TOKEN:
    raise ValueError("The Environment variable GITHUB_TOKEN is not defined.")

def get_followers():
    """Get the GitHub API url for followers management."""
    url = f"https://api.github.com/users/{USERNAME}/followers?per_page=100"
    return fetch_all_pages(url)

def get_following():
    """Get the GitHub API url for following management."""
    url = f"https://api.github.com/users/{USERNAME}/following?per_page=100"
    return fetch_all_pages(url)

def fetch_all_pages(url):
    """Get all items from a GitHub pagination."""
    items = []
    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro on access: {url}: {response.status_code} - {response.text}")
            break

        items.extend([user['login'] for user in response.json()])

        url = response.links['next']['url'] if 'next' in response.links else None
        time.sleep(0.5) 
    return items

def unfollow_user(username):
    """Make the request to GitHub API to unfollow the user."""
    url = f"https://api.github.com/user/following/{username}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"You are now following any more: {username}")
    else:
        print(f"Error on remove from following {username}: {response.status_code}")

def read_exceptions(filename="usersfollow.txt"):
    """Read the exceptions file and return the list of usernames
    (ignoring empty lines and comments)."""
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
    """Main function that will get all followers and following,
    apply the exceptions from a file, unfollow any people that 
    is not following you that is not in the file."""
    if not USERNAME or not TOKEN:
        print("GITHUB_USERNAME or GITHUB_TOKEN not defined.")
        return

    print("Getting all followers...")
    followers = set(get_followers())
    print(f"You have {len(followers)} followers.")

    print("Getting people that you are following...")
    following = set(get_following())
    print(f"You are following {len(following)} peoples.")

    exceptions = read_exceptions()
    not_following_back = following - followers
    
    filtered_not_following_back = sorted(not_following_back - exceptions)
    print(f"{len(filtered_not_following_back)} people don't follow you back.")

    if filtered_not_following_back:
        print("\n Unfollowing...")
        for user in sorted(filtered_not_following_back):
            unfollow_user(user)
            time.sleep(1)
    else:
        print("All people that you are following, follow you back!")

if __name__ == "__main__":
    main()