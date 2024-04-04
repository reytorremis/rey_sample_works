## ---------------------------------- Libraries --------------------------------------
import json
import pyodbc
import connection as ct

## All scripts are spearated by lamda function
## ---------------------------------- Connection.PY --------------------------------------
## Place this in a separate PY Script
conn_str = (
        "DRIVER=ODBC Driver 17 for SQL Server;"
        "DATABASE={database};"
        "UID={username};"
        "PWD={password};"
        "SERVER={server};"
        "PORT={port};".format(database='csmsc_209',
                              username='admin',
                              password='passkeys',
                              server='csmc209project.cnzbn9b5jtee.us-east-1.rds.amazonaws.com',
                              port='1433'))

## ---------------------------------- Create User --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries

def connect_to_db(_usr: str, _pas: str, _fir: str, _las: str, _rol: str):
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_sp = "exec [dbo].[sp_user_registration_simple] @username = ?, @password = ?, @firstname = ?, @lastname = ?, @role = ?"
        sp_param = (_usr, _pas, _fir, _las, _rol)
        row = crsr.execute(sql_sp, sp_param).fetchone()
        crsr.commit()
        x = str(row[0])
        if x[:3] == 'USR':
            return {"message": "SUCCESSFULLY ADDED RECORD", "body": {"user-id" : x}}
        else:
            return {"message": row[0], "body": {}}
    except Exception as e:
        return {"message": e, "body": {}}
    finally:
        crsr.close()
        con.close()


def lambda_handler(event, context):
    _usr = event['usr']
    _pas = event['pas']
    _fir = event['fir']
    _las = event['las']
    _rol = event['rol']
    return {'statusCode': 200, 'body': json.dumps(connect_to_db(_usr, _pas, _fir, _las, _rol))}

 ## ---------------------------------- Edit User --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries
def connect_to_db(_uid :str, _fir:str, _las:str, _usr:str, _mob:str, _bday: str, _gen:str, _add:str, _ht:str, _wt:str):
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_sp = "exec [dbo].[sp_edit_user] @userid = '{uid}', @new_firstname = '{fir}', @new_lastname = '{las}', @new_username = '{usr}', @new_mobile_number = '{mob}', @new_birthday = '{bday}', @new_gender = '{gen}', @new_complete_address = '{add}', @new_height = '{ht}', @new_weight = '{wt}'". format(
            uid= _uid,
            fir = _fir,
            las = _las,
            usr = _usr,
            mob = _mob,
            bday = _bday,
            gen = _gen,
            add = _add,
            ht = _ht,
            wt = _wt
        )
        crsr.execute(sql_sp)
        crsr.commit()
        sql_qry = "select message from dbo.vw_most_recent_user_logs where user_id =  '{uid}'".format(uid=_uid)
        crsr.execute(sql_qry)
        row = crsr.fetchone()
        return {"message" : row[0], "body" : {"user-id" : _uid}}
    except Exception as e:
        return {"message": e, "body": {"user-id": _uid}}
    finally:
        crsr.close()
        con.close()

def lambda_handler(event, context):
    uid = event['uid']
    fir = event['fir']
    las = event['las']
    usr = event['usr']
    mob = event['mob']
    bday = event['bday']
    gen = event['gen']
    add = event['add']
    ht = event['ht']
    wt = event['wt']
    return {'statusCode': 200, 'body': json.dumps(connect_to_db(uid, fir, las, usr, mob, bday, gen, add, ht, wt))}

## ---------------------------------- Log In --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries

def connect_to_db(_usr:str, _pas:str):
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_fx = "select [dbo].[fx_get_user_id] (?, ?)"
        fx_param = (_usr, _pas)
        row = crsr.execute(sql_fx, fx_param).fetchone()
        _uid = row[0]
        if _uid == 'ERROR':
            return 'INVALID USERID or PASSWORD'
        else:
            sql_sp = "exec [dbo].[sp_user_login] @userid = ?"
            sql_param = (_uid)
            crsr.execute(sql_sp, sql_param)
            crsr.commit()
            sql_qry = "select message from dbo.vw_most_recent_user_logs where user_id =  '{uid}'".format(uid = _uid)
            crsr.execute(sql_qry)
            out = crsr.fetchone()
            if out[0] == 'SUCCESSFULLY LOGGED IN':
                sql_qry2 = "select user_id, role, first_name, last_name, gender, mobile_number, birthday, complete_address, height, weight, user_name, password, created_at, updated_at  from dbo.users where user_id =  '{uid}'".format(uid=_uid)
                crsr.execute(sql_qry2)
                rows = crsr.fetchone()
                print(rows)
                return {"message" : out[0], "body" : {'user-id': rows[0], 'role': rows[1], 'first-name': rows[2], 'last-name': rows[3], 'gender': rows[4], 'mobile-number': rows[5], 'birthday':  rows[6], 'complete-address':  rows[7], 'height':  rows[8], 'weight':  rows[9], 'user-name': rows[10], 'password':  rows[11], 'created-at':  str(rows[12]), 'updated-at': str(rows[13])}}
            else:
                return {'message': out[0],'body': {}}
    except Exception as e:
        return (e)
    finally:
        crsr.close()
        con.close()

def lambda_handler(event, context):
   usr = event['usr']
   pas = event['pas']
   return {'statusCode': 200, 'body': json.dumps(connect_to_db(usr, pas))}
  
  
## ---------------------------------- Log out --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries

def connect_to_db(_uid:str):
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_sp = "exec [dbo].[sp_user_logout] ?"
        sp_param = (_uid)
        crsr.execute(sql_sp, sp_param)
        crsr.commit()
        sql_qry = "select message from dbo.vw_most_recent_user_logs where user_id =  '{uid}'".format(uid = _uid)
        crsr.execute(sql_qry)
        row = crsr.fetchone()
        return {"message" : row[0], "body" : {"user-id" : _uid}}
    except Exception as e:
        return {"message" : e, "body" : {"user-id" : _uid}}
    finally:
        crsr.close()
        con.close()


def lambda_handler(event, context):
   _uid = event['uid']
   return {'statusCode': 200, 'body': json.dumps(connect_to_db(_uid))}

## ---------------------------------- Add Diary --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries

def connect_to_db(_uid:str, _sys: int, _dia: int):
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_sp = "exec [dbo].[sp_add_diary_record] @userid = '{uid}',  @bp_systolic = {sys}, @bp_diastolic = {dia}". format(
            uid = _uid,
            sys = _sys,
            dia = _dia
        )
        crsr.execute(sql_sp)
        crsr.commit()
        sql_qry = "select message from dbo.vw_most_recent_user_logs where user_id =  '{uid}'".format(uid=_uid)
        crsr.execute(sql_qry)
        row = crsr.fetchone()
        x = row[0]
        if x.isdigit():
            return {"message" : "SUCCESSFULLY EXECUTED", "body" : {"diary-id" : x}}
        else:
            return {"message": x, "body" : {} }
    except Exception as e:
        return {"message": e, "body" : {} }
    finally:
        crsr.close()
        con.close()

def lambda_handler(event, context):
   uid = event['uid']
   sys = event['sys']
   dia = event['dia']
   return {'statusCode': 200, 'body': json.dumps(connect_to_db(uid, sys, dia))}


## ---------------------------------- Edit Diary --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries

def connect_to_db(_did :int, _uid:str, _sys: int, _dia: int):
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_sp = "exec [dbo].[sp_edit_diary_record] @diary_id = {did}, @userid = '{uid}',  @new_bp_systolic = {sys}, @new_bp_diastolic = {dia}". format(
            did = _did,
            uid = _uid,
            sys = _sys,
            dia = _dia
        )
        crsr.execute(sql_sp)
        crsr.commit()
        sql_qry = "select message from dbo.vw_most_recent_user_logs where user_id =  '{uid}'".format(uid=_uid)
        crsr.execute(sql_qry)
        row = crsr.fetchone()
        return {"message" : row[0], "body" : {"diary-id" : _did}}
    except Exception as e:
        return {"message": e, "body": {"diary-id": _did}}
    finally:
        crsr.close()
        con.close()

def lambda_handler(event, context):
    did = event['did']
    uid = event['uid']
    sys = event['sys']
    dia = event['dia']
    return {'statusCode': 200, 'body': json.dumps(connect_to_db(did, uid, sys, dia))}


## ---------------------------------- Delete Diary --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries
def connect_to_db(_did:str, _uid:str):
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_sp = "exec [dbo].[sp_delete_diary_record] @diary_id = {diary_id}, @userid = '{user_id}'".format(diary_id= _did, user_id= _uid)
        crsr.execute(sql_sp)
        crsr.commit()
        sql_qry = "select message from dbo.vw_most_recent_user_logs where user_id =  '{uid}'".format(uid=_uid)
        crsr.execute(sql_qry)
        out = crsr.fetchone()
        return {"message": out[0]}
    except Exception as e:
        return {"message": e }
    finally:
        crsr.close()
        con.close()

def lambda_handler(event, context):
   did = event['did']
   uid = event['uid']
   return {'statusCode': 200, 'body': json.dumps(connect_to_db(did, uid))}
  
## ---------------------------------- Get All Patients --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries
def connect_to_db():
    tuple = []
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_qry = "select user_id, first_name, last_name, gender, mobile_number, birthday, complete_address, height, weight, user_name from dbo.vw_get_all_patient"
        rows = crsr.execute(sql_qry).fetchall()
        row_cnt = len(rows)
        for i in range(row_cnt):
            tuple.append({'user-id': rows[i][0], 'first-name': rows[i][1], 'last-name': rows[i][2], 'gender': rows[i][3], 'mobile-number': rows[i][4], 'birthday': rows[i][5], 'complete-address': rows[i][6], 'height': rows[i][7], 'weight': rows[i][8], 'user-name': rows[i][9] } )
        return {"message" : "SUCCESSFULLY EXTRACTED", "row-count" : row_cnt ,"body": tuple}
    except Exception as e:
        return {"message": e , "row-count": 0 , "body": tuple}
    finally:
        crsr.close()
        con.close()

def lambda_handler(event, context):
    return {'statusCode': 200, 'body': json.dumps(connect_to_db())}

## ---------------------------------- Get All Diary Records --------------------------------------
## Place this in Main.Py and change lamda_hander.py name to main.py
## Import all Libraries

def connect_to_db(_uid:str):
    tuple = []
    try:
        con = pyodbc.connect(ct.conn_str)
        crsr = con.cursor()
        sql_qry = "select diary_id, user_id, bp_systolic, bp_diastolic, logged_date, comments from dbo.vw_get_diary where user_id =  '{userid}'".format(userid = _uid)
        rows = crsr.execute(sql_qry).fetchall()
        print(rows)
        row_cnt = len(rows)
        for i in range(row_cnt):
            tuple.append({'diary-id': rows[i][0], 'user-id': rows[i][1], 'bp-systolic': rows[i][2], 'bp-diastolic': rows[i][3], 'logged-date': rows[i][4], 'comments': rows[i][5]} )
        return {"message" : "SUCCESSFULLY EXTRACTED", "row-count" : row_cnt ,"body": tuple}
    except Exception as e:
        return {"message": e , "row-count": 0 , "body": tuple}
    finally:
        crsr.close()
        con.close()

def lambda_handler(event, context):
    uid = event['uid']
    return {'statusCode': 200, 'body': json.dumps(connect_to_db(uid))}
