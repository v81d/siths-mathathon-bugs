# SITHS Math-a-Thon Bugs & Exploits
The [SITHS Math-a-Thon website](https://siths-mathathon.com) has several security vulnerabilities which should be addressed immediately.

---

## DISCLAIMER
These vulnerabilities have been exploited with no intent of malice or destruction. **Did we exploit them? Yes—to some extent. Was it necessary? Probably—to uncover and report them.** *We do sincerely apologize if these have caused any major issues for the site; we promise that was not our intention.*

The goal of this repository is to demonstrate the major security vulnerabilities we have discovered in the SITHS Math-a-Thon website. The scripts provided are merely for educational purposes only, not to be used to cause irreversible damage to the server.

> Many of these API vulnerabilities can be addressed by implementing a role verification process using the JWT user ID, which prevents unauthorized users from attacking the APIs.

---

## BUGS
The bugs below have been discovered by [Aaron Wijesinghe](https://github.com/introvertednoob) by and [me](https://github.com/v81d). We are not affiliated with the SITHS Math-a-Thon website development team. [Link to Aaron's version of this repository, which contains additional information.](https://github.com/introvertednoob/mathathon-exploits)

### ~~1. Change Mines Balance~~ [FEATURE REMOVED]
Through the endpoint `/api/updateBalance`, you can set your balance to Infinity.

You can also set your balance to NaN or a negative number.

The `mines_balance_editor.py` tool in this repository allows you to edit anyone's balance, albeit it doesn't seem to work when targeting other users.

> Update (Wed Jun 11, 2025): Minigames have been removed. This bug is now obsolete.

### ~~2. Bet a Negative Amount~~ [FEATURE REMOVED]
If you remove `disabled=""` property from the Bet button in the Mines minigame, you can bet a negative amount on the game, thus increasing your balance.

> Update (Wed Jun 11, 2025): Minigames have been removed. This bug is now obsolete.

### ~~3. Unable to Update Avatar~~ [FEATURE REMOVED]
When choosing an image on the profile screen for my avatar and saving afterwards, you get an error:

```
mime type text/plain;charset=UTF-8 is not supported
```

> Update (Wed Jun 11, 2025): Custom avatars have been removed. This bug is now obsolete.

### ~~4. Change Anyone's Password~~ [RESOLVED]
The endpoint `/api/changePassword` allows you to change anyone's password using just their UID, which can be retrieved through the endpoint `/api/retreiveLeaderboard`.

> This exploit is no longer possible since this API endpoint now requires a valid, unexpired JSON Web Token (JWT).

### ~~5. Make New Questions~~ [RESOLVED]
The endpoint `/api/questions` can be used to create/modify questions.

This endpoint is usable with a valid and unexpired JWT, granted you know the correct parameters.

> Update (Sat Jun 07, 2025): Although this has now been semi-resolved, users can still freely view the questions through [this link](https://ferer2d9.apicdn.sanity.io/v1/data/query/production?query=*%5B_type+%3D%3D+%22questions%22%5D&returnQuery=false).

> Update (Wed Jun 11, 2025): Users can still view the full questions list through the new endpoint `/api/retreiveQuestions`. However, this is mostly be a minor vulnerability. I will mark it as resolved anyway since the severity of this "bug" is unknown.

### ~~6. Post Activities~~ [RESOLVED]
The endpoint `/api/activity` can also be used to create/modify activities (announcements).

This endpoint is usable with a valid and unexpired JWT, granted you know the correct parameters.

The `activity_editor.py` script in this repository allows you to edit any activity.

> Update (Sat Jun 07, 2025): Although this has now been semi-resolved, users can still freely view the activities through [this link](https://ferer2d9.apicdn.sanity.io/v1/data/query/production?query=*%5B_type+%3D%3D+%22activity%22%5D&returnQuery=false). The `activity_editor.py` script, however, is now obsolete.

> Update (Wed Jun 11, 2025): This feature has been revamped and this bug has been officially resolved.

### ~~7. Invalid User Accounts~~ [RESOLVED]
The registration page can be exploited to create a user account with invalid form data (i.e., a non-NYCDOE email, a fake OSIS number, etc.).

Like the Mines minigame balance exploit, this bug is powered by a simple removal of the `disabled=""` on the form buttons.

> Update (Wed Jun 11, 2025): This bug has been officially resolved.

### ~~8. View the Entire Leaderboard~~ [RESOLVED]
The endpoint `/api/retreiveLeaderboard` is unprotected and can easily be viewed by anyone without any credentials.

The `retrieve_leaderboard.py` script fetches the entire leaderboard and outputs it into a file.

> Update (Wed Jun 11, 2025): This bug has been resolved. Only the top ten users are returned through the endpoint now.

### ~~9. Spoof Contact Form~~ [RESOLVED]
You can send a contact form on someone else's behalf by, again, removing the `disabled=""` tag from the form elements.

This can be exploited to spam the email service and essentially spoof your identity (as someone else) while doing so.

You can also send a request to the unprotected endpoint `/api/submitContactForm`, as demonstrated in the script `send_contact.py`, which emulates the contact form directly in the terminal.

> Update (Wed Jun 11, 2025): This bug has been resolved. The contact form now matches the token to a user from the database and retrieves the name and email from the user metadata.

### 10. Mispelled API Endpoints
The endpoints `/api/retreiveAnnouncements`, `/api/retreiveLeaderboard`, and `/api/retreiveQuestions` are mispelled. It should be "retrieve," not "retreive."

This is not a bug, but it's a minor error to consider.

