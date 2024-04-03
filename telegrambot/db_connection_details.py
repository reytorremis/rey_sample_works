""""
Project File: db_connection_details
"""
# In case table report does not exist please run:
# CREATE TABLE report (
#     chat_id int NOT NULL,
#     name varchar(255) DEFAULT NULL,
#     email varchar(255) DEFAULT NULL,
#     report varchar(255) DEFAULT NULL,
#     PRIMARY KEY (chat_id)
# );

from mysql_connection_db import mysql_connection_db as db_con


# Database Configuration
db_config =  {
            'host':"ec2-50-17-131-52.compute-1.amazonaws.com",                 # database host
            'port': 3306,                       # port
            'user':"test",                      # username
            'passwd':"p@ssw0rD123",             # password
            'db':"is238_account_storage",       # database
            'charset':'utf8'                    # charset encoding
            }


#  ------------------ Defining DB Connection Details ------------------------------
# Establish Connection
dbcon = db_con(db_config)

# Define Curosr
dbcursor = dbcon.cursor


#  ------------------ DB Connection Functions ------------------------------
#Phone Login
def do_db_log_in(phone_num):
    if (dbcon):
        try:
            sql_procedure_query = "CALL is238_account_storage.update_status_log_in(%s)"
            data_tuple = (str(phone_num),)
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print(phone_num + ' successfully logged in')
        except:
            print('Error in Updating Log In for ' + phone_num)
    else:
        print("Unable to log in to database!")


#Phone Log out
def do_db_log_out(phone_num):
    if (dbcon):
        try:
            sql_procedure_query = "CALL is238_account_storage.update_status_log_out(%s)"
            data_tuple = (str(phone_num),)
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print(phone_num + ' successfully logged out')
        except:
            print('Error in Updating Log Out for ' + phone_num)
    else:
        print("Unable to log in to database!")


#Phone Update OTP
def do_update_otp(phone_num, otp):
    if (dbcon):
        try:
            sql_procedure_query = "CALL is238_account_storage.update_otp(%s,%s)"
            data_tuple = (str(phone_num), int(otp))
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print('OTP ' + otp + ' for ' + phone_num + ' successfully updated')
        except:
            print('Error in Updating OTP for ' + phone_num)
    else:
        print("Unable to log in to database!")


#Check Connection Status
def do_check_status(phone_num):
    if (dbcon):
        sql_procedure_query = "select is238_account_storage.check_status(%s)"
        data_tuple = (str(phone_num),)
        dbcursor.execute(sql_procedure_query, data_tuple)
        first_row = dbcursor.fetchone()
        return first_row[0]
    else:
        print("Unable to log in to database!")


# Convert Phone from
def convert_to_ph_mobile(phone_num):
    ph_mob = '0' + phone_num[3:]
    return ph_mob


def check_otp_phone_num_in_db(phone_num,otp):
    if (dbcon):
        sql_procedure_query = "select is238_account_storage.check_if_record_exists(%s,%s) as query_check"
        data_tuple = (str(phone_num),int(otp))
        dbcursor.execute(sql_procedure_query, data_tuple)
        #record = dbcursor.fetchall()
        first_row = dbcursor.fetchone()
        return first_row[0]
    else:
        print("Unable to log in to database!")


def get_last_activity(phone_num):
    if (dbcon):
        sql_procedure_query = "select is238_account_storage.get_last_activity(%s) as activity_check"
        data_tuple = (str(phone_num),)
        dbcursor.execute(sql_procedure_query, data_tuple)
        first_row = dbcursor.fetchone()
        return first_row[0]
    else:
        print("Unable to log in to database!")


def update_last_activity(phone_num):
    if (dbcon):
        try:
            sql_procedure_query = "call is238_account_storage.update_activity(%s)"
            data_tuple = (str(phone_num),)
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print(phone_num + ' activity updated')
        except:
            print('Error in Updating Last Activity for ' + phone_num)
    else:
        print("Unable to log in to database!")


def update_chat_id(phone_num, chat_id):
    if (dbcon):
        try:
            sql_procedure_query = "CALL is238_account_storage.update_chat_id(%s, %s)"
            data_tuple = (str(phone_num), int(chat_id))
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print(phone_num + ': chat_id updated')
        except:
            print('Error in Updating chat_id for ' + phone_num)
    else:
        print("Unable to log in to database!")

def get_phone_num(chat_id):
    if (dbcon):
        sql_procedure_query = "select is238_account_storage.get_phone_num (%s) as phone_num"
        data_tuple = (int(chat_id),)
        dbcursor.execute(sql_procedure_query, data_tuple)
        first_row = dbcursor.fetchone()
        return first_row[0]
    else:
        print("Unable to log in to database!")

# ===============================  WILLORD
def get_report_data(chat_idx):
    if dbcon:
        sql_procedure_query = "SELECT * FROM report WHERE chat_id = %s"
        data_tuple = (str(chat_idx),)
        dbcursor.execute(sql_procedure_query, data_tuple)
        first_row = dbcursor.fetchone()
        return first_row
    else:
        print("Unable to log in to database!")


def update_insert_report_name(chat_idx, name):
    if dbcon:
        try:
            sql_procedure_query = "INSERT INTO report(chat_id, name) VALUES(%s, %s) ON DUPLICATE KEY UPDATE name = %s"
            data_tuple = (chat_idx, str(name), str(name))
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print('report name activity updated')
        except:
            print('Error in Updating Last Acitivty for report name: ' + str(name))
    else:
        print("Unable to log in to database!")


def update_insert_report_email(chat_idx, email):
    if dbcon:
        try:
            sql_procedure_query = "INSERT INTO report(chat_id, email) VALUES(%s, %s) ON DUPLICATE KEY UPDATE email = %s"
            data_tuple = (chat_idx, str(email), str(email))
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print('report email activity updated')
        except:
            print('Error in Updating Last Acitivty for report email: ' + str(email))
    else:
        print("Unable to log in to database!")


def update_insert_report_report(chat_idx, report):
    if dbcon:
        try:
            sql_procedure_query = "INSERT INTO report(chat_id, report) VALUES(%s, %s) ON DUPLICATE KEY UPDATE" \
                                  " report = %s"
            data_tuple = (chat_idx, str(report), str(report))
            dbcursor.execute(sql_procedure_query, data_tuple)
            dbcon.commit()
            print('report.report activity updated')
        except:
            print('Error in Updating Last Acitivty for report.report: ' + str(report))
    else:
        print("Unable to log in to database!")
