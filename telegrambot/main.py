""""
Project: TeleBot Project for IS238
Developed by
    Willord Jay Villanueva,
    Rey lawrence Torrecampo,
    Connie Baltazar,
    Herminio Liegen Jr.,
    Clark Joseph Ribunal

Version History:
1.0 on 12/25/2021
1.1 on 12/30/2021 - added log out and
Associated python files:
    1) Costants.py              --> Contains Bot Key and SMS Authentication
    2) mysql_connection_db.py   --> MySQL Class for easier connection
    3) db_connection_details.py --> defines MySQl Connection Details
    4) responses.py             --> Contains non-command responses
1.2 on 12/30/2021 - added QUOTES function
1.3 on 12/31/2021 - merged all functions
1.4 on 02/01/2021 - updated version to allow simultaneous users and create data table for REPORT function, fixed issues for multi user chats
1.5 on 03/01/2021 - updated timeout function and message handlers


This file contains the full program and sqeuences for login, logout and help.
"""

#  ------------------ Libraries ------------------------------
import constants as keys
import responses as r
from telegram.ext import *
import telegram as t
import db_connection_details as dbd
from twilio.rest import Client
import random
import telebot
import random

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

bot = telebot.TeleBot(keys.API_KEY)
# chat_id = keys.chat_id
EMAILAD, REPORT, CONFIRM = range(3)

#  ------------------ Variables ------------------------------
OTP_generated = 000000
login_status = 'N'
# phone = '+630000000000'


#  ------------------ Non-program Specific Functions ------------------------------
# Generate six digit OTP
def generate_otp():
    global OTP_generated
    OTP_generated = random.randint(100000, 999999)
    print(OTP_generated)
    return OTP_generated


# Generates log in status, A for active and I for Inactive
def check_log_in_status(chat_id):
    _phone_num = dbd.get_phone_num(chat_id)
    # print('get phone num: ' + str(_phone_num))
    phone_ph_converted = dbd.convert_to_ph_mobile(_phone_num)
    # print('phone_ph_converted : ' + str(phone_ph_converted))
    login_status = dbd.do_check_status(phone_ph_converted)
    if (login_status == 'Y'):
        return 'A'
    else:
        return 'I'

def timestamp_update(phone_num):
    dbd.update_last_activity(phone_num)

# Sends OTP to user; +63 + 10-digit number as input
def send_otp(phone_num):
    account_sid = keys.twilio_accnt_num
    auth_token = keys.twilio_auth_token
    client = Client(account_sid, auth_token)
    otp = generate_otp()
    message = client.messages \
        .create(body='Your OTP is - ' + str(otp), from_=keys.twilio_phone_num, to=phone_num)
    print("Message ID" + message.sid, " OTP" + str(otp))
    phone_num_ph = dbd.convert_to_ph_mobile(phone_num)
    dbd.do_update_otp(phone_num_ph, str(otp))


# Send email report
def send_email(chat_idx):
    myresult = dbd.get_report_data(chat_idx)
    newEmail = MIMEMultipart('alternative')
    newEmail['Subject'] = 'A report from ' + str(myresult[1])
    newEmail['From'] = 'Group 2 - IS238 <willord@sandbox03e651e0a1ec4bb1b72a356511438fe1.mailgun.org>'
    newEmail['To'] = 'Miguel Abriol <miguel.abriol+project@up.edu.ph>'
    newEmail['reply-to'] = str(myresult[2])
    newEmail.attach(MIMEText(str(myresult[3]), 'plain'))
    keys.mySMTP.sendmail(keys.emailSender, keys.emailRecipients, str(newEmail))


# Generate random quotes for the selected candidate
def msg(update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == '1':
        send_email(update.callback_query.message.chat_id)
        query.edit_message_text(text="The report has been sent successfully")
    elif query.data == '2':
        query.edit_message_text(text="Report Cancelled")
    elif query.data == '3':
        i = int(random.randint(0, 4))
        quote = r.ran_quotes[i]
        query.edit_message_text(text=quote)
    elif query.data == '4':
        i = int(random.randint(5, 9))
        quote = r.ran_quotes[i]
        query.edit_message_text(text=quote)
    elif query.data == '5':
        i = int(random.randint(10, 14))
        quote = r.ran_quotes[i]
        query.edit_message_text(text=quote)
    elif query.data == '6':
        i = int(random.randint(15, 19))
        quote = r.ran_quotes[i]
        query.edit_message_text(text=quote)
    elif query.data == '7':
        i = int(random.randint(20, 24))
        quote = r.ran_quotes[i]
        query.edit_message_text(text=quote)
    else:
        query.edit_message_text(text="Please select a valid option")

# Get chat ID
def get_chat_id(update):
    user = update.message.from_user
    return user['id']

# ---------- defining states ---------
ONE, TWO = range(2)


#  ------------------ Program Specific Functions ------------------------------
# /Start Command to start log in sequence
def start_command (update, context):
    user = update.message.from_user
    chat_id = get_chat_id(update)
    print(chat_id)
    #chat_id = update.message.chat_id
    print('You talk with user{} and his user ID:{} '.format(user['username'], user['id']))
    update.message.reply_text('Welcome to Telegrambot.\nTo start, you will need to share your contact information.') #introdductory Message
    contact_keyboard = t.KeyboardButton('Share contact', request_contact=True) # creating contact button object
    custom_keyboard = [[contact_keyboard]]  # creating keyboard object
    reply_markup = t.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True) #show keyboard
    update.message.reply_text("Would you mind sharing your contact with me?", reply_markup=reply_markup) # prompt Sharing of Contact
    return ONE

# Callback to get Contact; Automatically gets the Phone Number when Contact is shared
def contact_callback(update, context):
    # global phone
    contact = update.message.contact #Get contact information
    phone = contact.phone_number #get phone number
    chat_id = get_chat_id(update)
    dbd.update_chat_id(dbd.convert_to_ph_mobile(phone),chat_id)
    # print(chat_id)
    update.message.reply_text('Sent an OTP to your end. Kindly check if you receive it. \nOnce received, input the OTP in the Chat.')  # introdductory Message
    send_otp(phone)
    #update.message.reply_text() #reply with message
     #send OTP to Phone
    return TWO

# Start of login sequence once correct OTP is sent
def login_sequence(update, context):
    _otp_input = update.message.text
    chat_id = get_chat_id(update)
    print(chat_id)
    _phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(_phone_num) # change +63 to 0
    if (dbd.check_otp_phone_num_in_db(phone_ph_converted,_otp_input) == 'FND'): # search db if Number and OTP matches, if yes then log in is successful
        dbd.do_db_log_in(phone_ph_converted)
        print('Log in Successful')
        update.message.reply_text('Login Successful. \n\nInput QUOTES to generate random quote from a selected presidential candidate. \n\nInput REPORT to submit a report. \n\n/end to logout\n\n/help to view the available keywords.')  # Login message Message
        #bot.send_message(chat_id,'Log in Successful')  # introdductory Message
        #update.message.reply_text('Log in Successful')
    else: #if not log in fails
        print('Log in Failed')
        update.message.reply_text('Log in Failed. Kindly Input Correct OTP!')
        #bot.send_message(chat_id, 'Log in Failed. Kindly Input Correct OTP!')
        return TWO # If incorrect OTP, returns to OTP Start sequence.
    check_log_in_status(chat_id) #converts return of status: Y --> A and N --> I
    print(check_log_in_status(chat_id))
    return ConversationHandler.END

# Non-command handler
def handle_message(update,context):
    #global phone
    chat_id = get_chat_id(update) # Get contact information
    phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(phone_num)  # change +63 to 0
    if (check_log_in_status(chat_id) == 'A'): #Check if Active
        if (r.check_for_time_out(phone_ph_converted)): # Check Time Out
            text = str(update.message.text).lower()
            response = r.sample_responses(text)
            update.message.reply_text(response)
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(phone_ph_converted)
    else:
        update.message.reply_text('Kindly Log in by inputting /start')

# Cancel Log in Process
def cancel(update, context): #Cancels current log in process
    chat_id = get_chat_id(update)
    bot.send_message(chat_id, text="Log in Process Canceled.\nKindly input /start to trigger login sequence!")
    return ConversationHandler.END


# User log out
def logout_sequence(update, context): # Log out Process; triggered by /end
    chat_id = get_chat_id(update)
    phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(phone_num)  # change +63 to 0
    if (check_log_in_status(chat_id) == 'A'):
        dbd.do_db_log_out(phone_ph_converted)
        update.message.reply_text('Logout Successful')
    else:
        update.message.reply_text('Unable to Log Out. Kindly Log in by inputting /start')


# Ask name of the user for the report
def askname(update, context):
    chat_id = get_chat_id(update) # Get contact information
    phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(phone_num)  # change +63 to 0
    if (check_log_in_status(chat_id) == 'A'):
        if (r.check_for_time_out(phone_ph_converted)):
            update.message.reply_text("What is your name?")
            timestamp_update(phone_ph_converted)
            return EMAILAD
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone_ph_converted))
    else:
        update.message.reply_text('Kindly Log in by inputting /start')


# Ask email address of the user for the report "REPLY-TO"
def askemailadd(update, context):
    chat_id = get_chat_id(update)
    phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(phone_num)  # change +63 to 0
    if (check_log_in_status(chat_id) == 'A'):
        if (r.check_for_time_out(phone_ph_converted)):
            dbd.update_insert_report_name(update.message.chat_id, update.message.text)  # inserting name
            print("Record name inserted.", update.message.chat_id, update.message.text)
            update.message.reply_text("What is your email address?")
            dbd.update_last_activity(phone_ph_converted)
            return REPORT
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone_ph_converted))
    else:
        update.message.reply_text('Kindly Log in by inputting /start')




# Ask for details of the report
def askhelp(update, context):
    chat_id = get_chat_id(update)
    phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(phone_num)  # change +63 to 0
    if (check_log_in_status(chat_id) == 'A'):
        if (r.check_for_time_out(phone_ph_converted)):
            dbd.update_insert_report_email(update.message.chat_id, update.message.text)  # inserting email
            print("Record email inserted.", update.message.chat_id, update.message.text)
            update.message.reply_text("What is your report?")
            dbd.update_last_activity(phone_ph_converted)
            return CONFIRM
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone_ph_converted))
    else:
        update.message.reply_text('Kindly Log in by inputting /start')


# Confirmation to send the report -> None
def confirmreport(update, context: CallbackContext):
    chat_id = get_chat_id(update)
    phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(phone_num)  # change +63 to 0
    if (check_log_in_status(chat_id) == 'A'):
        if (r.check_for_time_out(phone_ph_converted)):
            dbd.update_insert_report_report(update.message.chat_id, update.message.text)  # inserting report
            print("Record report inserted.", update.message.chat_id, update.message.text)
            keyboard = [
                [
                    InlineKeyboardButton("Confirm", callback_data='1'),
                    InlineKeyboardButton("Cancel", callback_data='2'),
                ]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Please confirm:', reply_markup=reply_markup)
            dbd.update_last_activity(phone_ph_converted)
            return ConversationHandler.END
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone_ph_converted))
    else:
        update.message.reply_text('Kindly Log in by inputting /start')


# Display InlineKeyboardButton for the candidates
def display_candidate(update, context):
    chat_id = get_chat_id(update)
    phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(phone_num)  # change +63 to 0
    if (check_log_in_status(chat_id) == 'A'):
        if (r.check_for_time_out(phone_ph_converted)):
            keyboard = [
                [InlineKeyboardButton("Leni Robredo", callback_data='3')],
                [InlineKeyboardButton("Bongbong Marcos", callback_data='4')],
                [InlineKeyboardButton("Ping Lacson", callback_data='5')],
                [InlineKeyboardButton("Manny Pacquiao", callback_data='6')],
                [InlineKeyboardButton("Isko Moreno", callback_data='7')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Pick a Presidential Candidate', reply_markup=reply_markup)
            dbd.update_last_activity(phone_ph_converted)
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone_ph_converted))
    else:
        update.message.reply_text('Kindly Log in by inputting /start')



# Help Command
def help_command (update, context):  # help menu; triggered by /help
    chat_id = get_chat_id(update)
    phone_num = dbd.get_phone_num(chat_id)
    phone_ph_converted = dbd.convert_to_ph_mobile(phone_num)  # change +63 to 0
    if (check_log_in_status(chat_id) == 'A'):
        if (r.check_for_time_out(phone_ph_converted)):
            update.message.reply_text('Available keywords: \n\n/start to login\n\n/end to logout\n\n/help for the available menu\n\nQUOTES for insipiration quotes of a presidential candidate\n\nREPORT to send an email to support.')
            dbd.update_last_activity(phone_ph_converted)
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone_ph_converted))
    else:
        update.message.reply_text('Kindly Log in by inputting /start')


# Error Handler
def error(update, context):  # displays error in console
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    ch1 = ConversationHandler(entry_points=[CommandHandler("start", start_command)],
                              states={ONE: [MessageHandler(Filters.contact, contact_callback)],
                                      TWO: [MessageHandler(Filters.text, login_sequence)]},
                              fallbacks=[MessageHandler(Filters.regex('cancel'), cancel)], allow_reentry=True)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text('REPORT'), askname)],
        fallbacks=[],

        states={
            EMAILAD: [MessageHandler(Filters.text, askemailadd)],
            REPORT: [MessageHandler(Filters.text, askhelp)],
            CONFIRM: [MessageHandler(Filters.text, confirmreport)],
        },
    )
    updater.dispatcher.add_handler(ch1)  # input /start to trigger message sequence
    dp.add_handler(CommandHandler("help", help_command))  # input /help to prompt help commands
    dp.add_handler(CommandHandler("end", logout_sequence))  # input /end to trigger log out sequence
    dp.add_handler(MessageHandler(Filters.contact, contact_callback))  # gets contact message
    # dp.add_handler(MessageHandler(Filters.text, handle_message))  # gets contact message
    updater.dispatcher.add_handler(CallbackQueryHandler(msg))
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text('QUOTES'), display_candidate))
    dp.add_error_handler(error)

    updater.start_polling(15)

    updater.idle()


# ----------------------- Main Program --------------------------------------
if __name__ == '__main__':
    print("Bot started ....")
    main()
