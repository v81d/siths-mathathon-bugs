import requests


def get_leaderboard():
    data = requests.get(
        "https://www.siths-mathathon.com/api/retreiveLeaderboard"
    ).json()

    leaderboard = data["leaderboard"]

    output = "# SITHS Math-a-Thon Leaderboard\n"

    for user in leaderboard:
        output += f"\n{leaderboard.index(user) + 1}. {user['user_name']} - {user['total_points']} points"

    return output


fetch = input(":: (y/N) Do you want to fetch the leaderboard? ")
if fetch.lower() == "y":
    with open("leaderboard.md", "w") as file:
        file.write(get_leaderboard())
        print("Leaderboard fetched and saved to leaderboard.md.")
else:
    print("The program will now terminate.")
