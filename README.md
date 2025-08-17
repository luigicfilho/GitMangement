# Git Mangement

An automatic GitHub followers manager.

This repository contains a GitHub Action that runs daily at **03:00 UTC** and performs the following tasks:

- **Unfollows users who do not follow you back**.  
- **Skips users listed in an exceptions file**, so they are never unfollowed even if they don’t follow back.

## Main Features

1. **Daily follower check**
   - The GitHub Action runs automatically **every day at 03:00 UTC**.
   - It checks your followers and the users you are following.

2. **Smart unfollow**
   - If a user you follow **does not follow you back**, they will be unfollowed — **unless they are listed in the exceptions file**.

3. **Exceptions file**
   - Keep a file, in this case `usersfollow.txt` (you can change to: `exceptions.txt` or `whitelist.txt`) with usernames that **should never be unfollowed**, even if they don’t follow you back.

## How It Works

1. You maintain the repository with:
   - A script or action that queries the GitHub API.
   - An exceptions file containing usernames (one per line).

2. On execution:
   - The Action fetches your followers and following lists.
   - Compares them to identify differences.
   - Filters out exceptions.
   - Calls the API to **unfollow remaining users**.

3. The Action schedule is configured as:

```yaml
on:
 schedule:
   - cron: '0 3 * * *'
```

This ensures daily execution at **03:00 UTC**.

## Example of `whitelist.txt`

```
friend-user-1
friend-user-2
```

— each username should be placed on a separate line.

## Benefits

- **Full automation**: no need to manually check who unfollowed you.  
- **Exception control**: important users are never unfollowed.  
- **Reliable execution**: always runs at the scheduled time (03:00 UTC).  

## Getting Started

1. Clone or fork the repository.  
2. Create your exceptions file, or edit the `usersfollow.txt`.  
3. Customize the cleanup script according to your needs.  
5. Commit and push — the Action will run automatically every day at 03:00 UTC.  
