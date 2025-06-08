import json
import os
import requests
from copy import deepcopy
from dotenv import find_dotenv, load_dotenv, set_key
from requests.structures import CaseInsensitiveDict

dotenv_file = find_dotenv()

data_template = """
{
    "changes": {
        "_rev": "__REV__",
        "_id": "__ID__",
        "content": "__CONTENT__",
        "date": "__DATE__",
        "_type": "activity"
    },
    "_id": "__ID__",
    "createdAt": "__CREATED__",
    "updateType": "create"
}
"""

load_dotenv()

headers = CaseInsensitiveDict()
headers["Authorization"] = os.environ.get("jwt")
headers["Content-Type"] = "application/json"

bold = "\033[1m"
faint = "\033[2m"
end = "\033[0m"
url = "https://www.siths-mathathon.com/api/activity"


def clear():
    os.system("cls || clear")  # Simplified solution to clearing the console


def has_valid_date(id):
    global sanity
    global sanity_

    if sanity[id] in sanity_:
        return True
    else:
        return False


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


def send_req():  # Funtion allows the action to be run recursively
    global headers

    resp = requests.put(url, headers=headers, data=data)
    response = json.loads(resp.text)["status"]

    # Create a new JWT
    if response == "error":
        headers["Authorization"] = load_jwt()
        os.environ["jwt"] = headers[
            "Authorization"
        ]  # Update the OS environment variable
        set_key(
            dotenv_file, "jwt", os.environ["jwt"]
        )  # Update the dotenv file with the new JWT

        restart = input(
            f":: [Y/n] Your JSON Web Token has regenerated since it might have been expired. Would you like to retry the request? "
        )
        if restart.lower() == "n":
            return False
        else:
            send_req()
    else:
        print("\n" + resp.text)
        restart = input(
            ":: [Y/n] Successfully edited activity; the updates will appear shortly. Would you like to restart the program? "
        )
        if restart.lower() == "n":
            return False
    return True


try:
    while True:
        sanity = json.loads(
            requests.get(
                "https://ferer2d9.apicdn.sanity.io/v1/data/query/production?query=*%5B_type+%3D%3D+%22activity%22%5D&returnQuery=false"
            ).text
        )[
            "result"
        ]  # Fetch all of the activity data
        sanity_ = sorted(
            [item for item in sanity if "date" in list(item.keys())],
            key=lambda x: x["date"],
            reverse=True,
        )  # Sort the data by date

        clear()

        for item in range(0, len(sanity)):
            if "date" in list(sanity[item].keys()):
                sanity[item]["date"] = (
                    sanity[item]["date"].replace("A ", "").replace("A", "")
                )  # Revise dates incorrectly containing the character "A"

            # List all the messages in order by their ID
            if "content" in list(sanity[item].keys()):
                print(f"{bold}[{item + 1}]{end} {sanity[item]["content"]}")
            else:
                print(f"{bold}[{item + 1}]{end} {faint}Invalid Message{end}")
        id_inp = input("\n:: Enter message ID to change: ")
        try:
            id = int(id_inp) - 1
        except ValueError:
            restart = input(
                ":: [Y/n] Your input is not a valid number. Would you like to restart the program? "
            )
            if restart == "n":
                break
            else:
                continue
        if id > len(sanity) - 1:
            restart = input(
                ":: [Y/n] Your selected message is out of range. Would you like to restart the program? "
            )
            if restart == "n":
                break
            else:
                continue

        clear()

        data = deepcopy(
            data_template
        )  # Make an actual copy of the dictionary instead of a reference to it

        # Edit the date
        print(f"=> Editing Message (ID={sanity[id]["_id"]})]\n")
        for item in range(0, len(sanity_)):
            print(
                f"{bold}[{item + 1} - {sanity_[item]["date"]}]{end} {sanity_[item]["content"][:20]}{" ..." if len(sanity_[item]["content"]) > 20 else ""}"
            )
        print(
            "\nAbove are the potential placements of your edited message along with their respective times. Edit accordingly.\n"
        )
        date = input(":: [SKIP/input] Enter the new date: ")
        if date == "":
            data = data.replace(
                "__DATE__",
                (
                    sanity[id]["_createdAt"]
                    if not has_valid_date(id)
                    else sanity[id]["date"]
                ),
            )
        else:
            data = data.replace("__DATE__", date)

        clear()

        # Edit the message content
        print(f"=> Editing Message (ID={sanity[id]["_id"]})\n")
        data = data.replace(
            "__CONTENT__",
            input(":: [EMPTY/input] Enter the new content of your message: "),
        )
        if has_valid_date(id):
            data = data.replace(
                "__CREATED__", sanity[id]["date"]
            )  # date if date != "" else
        else:
            data = data.replace(
                "__CREATED__", date if date != "" else sanity[id]["_createdAt"]
            )
        data = data.replace("__ID__", sanity[id]["_id"]).replace(
            "__REV__", sanity[id]["_rev"]
        )

        clear()

        confirm = input(
            f"Editing Message (ID={sanity[id]["_id"]})]\n{eval(json.dumps(data, indent=4))}\n:: [Y/n] Confirm update(s)? "
        )
        if confirm.lower() == "n":
            break

        option = send_req()
        if not option:
            break
except KeyboardInterrupt:
    print(
        "\nThe program has been interrupted by the user. It will now terminate peacefully."
    )
