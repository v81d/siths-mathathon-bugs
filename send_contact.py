import os
import re
import requests
from time import sleep


def clear():
    os.system("cls || clear")  # Simplified solution to clearing the console


def input_(type):
    data = input(f":: Input the {type}: ")
    if len(data) < 1:
        print(f"Please enter a {type}.")
        sleep(0.5)
        return input_(type)
    return data


while True:
    clear()

    name = input_("sender name")
    email = input_("sender email address")
    subject = input_("email subject")
    body = input_("email body")

    body = {
        "name": name,
        "email": email,
        "subject": subject,
        "body": body,
    }
    print("\n")
    print(body)
    if (
        input(
            "\n:: [Y/n] Above is the synthesized request body. Would you like to proceed with this? "
        ).lower()
        == "n"
    ):
        break

    resp = requests.post(
        "https://www.siths-mathathon.com/api/submitContactForm",
        json=body,
    ).json()

    print("\n")
    print(resp)
    if input(":: [Y/n] Would you like to rerun the program? ").lower() == "n":
        break
