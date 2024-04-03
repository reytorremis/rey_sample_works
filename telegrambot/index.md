# Rey's Sample Works - Telegram Bot

<a href=""><img src="https://img.shields.io/badge/HOME%20GitHub-0068cb" /></a>

---

## Description
The Python code is hosted on an AWS EC2 instance, enabling interaction with a MySQL database. It also interfaces with a Telegram Bot and utilizes the Twilio and Mailgun APIs for sending text messages and emails, respectively. The server was disabled, but documentation and demonstration remain accessible.

---
## External Links:
[Video Presentation of Telegram Bot](https://youtu.be/oOTjHrp3N9Q?si=cSKsMoEcS6Ra8hM_)

---
## Download Python Files:
1. [main.py](main.py)
+ Contains the main interface between telegram and the database. All telegram functions and error handling are found in this file.

2. [constants.py](constants.py)
+ Contains constant variables referenced in main.py. (Twilio API account ID, Telegram Bot ID, Email Address and SMTP ID)

3. [db_connection_details](db_connection_details.py)
+ Interfaces between Python and MySQL. Contains RDBMS connection functions.

4. [mysql_connection_db](mysql_connection_db.py)
+ MySQL Interface class

5. [responses](responses.py)
+ Contains all responses used for telegram bot.

---

## Video Presentation

<iframe width="1080" height="640" src="https://www.youtube.com/embed/oOTjHrp3N9Q?si=QUy08Qm3Oh_w_7ZI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

---

