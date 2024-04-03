""""
Project File: Constants
"""
import smtplib
#  ------------------ Constant Variables ------------------------------
# Bot Token
API_KEY = r'5062906885:AAFggvpwZ05aXnxEuAIEmxOdnglTK7UrrLM'

    #r'5098461916:AAGkraVA0TP8ujKSqqDz0ea5cyKxhcW-MMs'

# Current Chad ID -- to be updated for automation
chat_id = '1336351420'
user_id = '1336351420'

#  ------------------ Constant Variables ------------------------------
# Twilio Details

twilio_accnt_num = r'AC418746642909e2d03bb59a277524f2bc'    # Twilio Account Number AC90bf347bcf1f6467a9d3196b241ba336
twilio_auth_token = r'dc7772e3651e5c6bf8c292610de28f43'     # Twilio Authentication Token 382ec67fa29c28e614dafc58004199eb
twilio_phone_num = r'+13612214541'                           # Twilio Phone Number +17246342051


# -------------------------- MailGun -------------------------
mySMTP = smtplib.SMTP('smtp.mailgun.org', 587)
emailSender = 'willord@sandbox03e651e0a1ec4bb1b72a356511438fe1.mailgun.org'
emailRecipients = ['miguel.abriol+project@up.edu.ph']
mySMTP.login(emailSender, "cbd6fed5fe4b7fb48b26d476ccc89f13-1831c31e-f93747c7")  # mailgun-domain, domain password 59c3cbac17aef61e76717b993d68bcb3-cac494aa-ab26918c
