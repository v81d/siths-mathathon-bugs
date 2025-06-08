import os
import requests
from uuid import UUID
from math import inf
from dotenv import find_dotenv, load_dotenv, set_key

dotenv_file = find_dotenv()
load_dotenv()


def clear():
    os.system("cls || clear")  # Simplified solution to clearing the console


def validate_uuid(uuid):
    try:
        UUID(uuid)
    except:
        return False
    return True


def get_leaderboard():
    data = requests.get(
        "https://www.siths-mathathon.com/api/retreiveLeaderboard"
    ).json()
    return data["leaderboard"]


def search():  # Search through the users
    clear()

    leaderboard = get_leaderboard()
    list = ""
    for item in leaderboard:  # Iterate through the list and create a user list
        list += f"\n[{leaderboard.index(item) + 1}] {item['user_name']} - {item['uid']}"
    print(f"Below is the list of discovered users in the database:\n{list}")
    user = input("\n:: Select a user number from the list: ")
    if user.isnumeric():  # Is the input a valid number?
        if int(user) > len(leaderboard):  # Is the selected user in the list?
            print(
                "The provided input is not in the range of the list. The task been terminated."
            )
        return leaderboard[int(user) - 1]  # Return the user data
    else:
        print("The provided input is not a valid number. The task has been terminated.")
        os._exit(1)


def load_jwt():
    headers = {
        "Content-Type": "application/json",
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVpcm1xemJqbHVhbW54enp3ZWllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjIzNTE1NzMsImV4cCI6MjAzNzkyNzU3M30.bd2LyUSNKoYB0zB6ZEhSGto639y_Zk011H5Wn-Ts428",
    }

    data = {
        "email": os.environ.get("usr_e"),
        "password": os.environ.get("usr_p"),
        "gotrue_meta_security": {},
    }

    # Login with the test user account
    resp = requests.post(
        "https://uirmqzbjluamnxzzweie.supabase.co/auth/v1/token?grant_type=password",
        json=data,
        headers=headers,
    ).json()

    if "error_code" in list(resp.keys()):
        print(
            "\n"
            + str(resp)
            + "\nThe JWT failed to load. Please check if your credentials are correct. The program will now terminate."
        )
        os._exit(6)  # Status code 6 => incorrect credentials
    else:
        # resp.json()["access_token"] => JSON Web Token
        return "Bearer " + resp["access_token"]


def send_req(uid, balance):
    # Make the request
    headers = {"Authorization": os.environ["jwt"]}
    body = {
        "userId": uid,
        "balance": balance,
        "gameState": {},
    }
    resp = requests.post(
        "https://www.siths-mathathon.com/api/updateBalance",
        headers=headers,
        data=body,
    ).json()
    if "error" in resp.keys():
        headers["Authorization"] = load_jwt()
        os.environ["jwt"] = headers[
            "Authorization"
        ]  # Update the OS environment variable
        set_key(
            dotenv_file, "jwt", os.environ["jwt"]
        )  # Update the dotenv file with the new JWT

        if (
            input(
                f":: [Y/n] Your JSON Web Token has regenerated since it might have been expired. Would you like to retry the request? "
            )
        ) == "n":
            return False
        else:
            send_req(uid, balance)
    else:
        print("\n" + str(resp))
        if (
            input(
                ":: [Y/n] Successfully updated the user's balance; the changes will appear shortly. Would you like to restart the program? "
            )
        ) == "n":
            return False
    return True


while True:
    clear()

    if (
        input(":: [Y/n] Would you like to select a user from the leaderboard? ").lower()
        != "n"
    ):
        user = search()
        uid = user["uid"]
    else:  # Allow the user to enter a user ID directly
        clear()
        if (
            input(
                ":: [a/B] Would you like to input a user ID or retrieve it from .env? "
            ).lower()
            == "a"
        ):
            uid = input(":: What is the user ID of the target? ")
        else:
            uid = os.environ[
                "uid"
            ]  # Retrieve the user ID directly as an environment variable

    if not validate_uuid(uid):  # Check if the user ID is a valid UUID
        print(f"The user ID ({uid}) is invalid. The task has been terminated.")
        os._exit(1)

    # Set a new balance
    try:
        name = user["user_name"]
    except (NameError, KeyError, TypeError):
        name = uid
    balance = input(f":: Enter the new balance for {name}: ")
    if balance.isnumeric():
        balance = int(balance)
    elif balance.lower() == "infinity":
        balance = inf
    else:
        print("The provided input is not a valid number. The task has been terminated.")
        os._exit(1)

    # Update the balance
    if not send_req(uid, balance):
        break
