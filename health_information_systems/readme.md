# Rey's Sample Works - Health Information Management System

<a href=""><img src="https://img.shields.io/badge/HOME%20GitHub-0068cb" /></a>

## Description
AWS Lambda programmed using python uses multiple API points. It connects with MS SQL Server and triggers stored procedures. Front-end for this project is a mobile app that accesses API end points. Server was shut down due to incurring costs.

---
## Links:
[Documentation](https://drive.google.com/file/d/17rDCuWskhmumeTC5LrPi2npBAy99ulI4/view)

---

## Steps in Deployment

### 1. Provisioning a MS SQL Server

Deployed a MS SQL Server RDBMS in AWS and created a database named csmsc_209. Afterwards, tables were created using the SQL Script below:

#### 2. Create Tables

```
USE [csmsc_209]

GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

drop table if exists dbo.diary;
drop table if exists dbo.groups;
drop table if exists dbo.user_logs;
drop table if exists dbo.users;
drop table if exists dbo.roles;
drop table if exists dbo.sp_logs;

create table [dbo].[users](
	[user_id] [varchar](40) PRIMARY KEY,
	[role] [varchar](10) NOT NULL,
	[first_name] [varchar](100) NOT NULL,
	[last_name] [varchar](100) NOT NULL,
	[gender] varchar(255),
	[mobile_number] varchar(255),
	[birthday] varchar(255),
	[complete_address] varchar(1000), 
	[height] varchar(255), 
	[weight] varchar(255),
	[user_name] [varchar](50) NOT NULL  UNIQUE,
	[password] [varchar](50),
	[created_at] datetime,
	[updated_at] datetime
)


CREATE TABLE [dbo].[diary](
	[diary_id] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
	[user_id] [varchar](40) NULL,
	[bp_systolic] int NULL,
	[bp_diastolic] int NULL,
	last_update_by varchar(40),
	[created_at] datetime,
	[updated_at] datetime,
	FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE)

CREATE TABLE [dbo].[user_logs](
	[log_id] [int] IDENTITY(1,1) PRIMARY KEY,
	[user_id] [varchar](40) NULL,
	[status] [varchar](1) NULL,
	[log_in_time] [datetime] NULL,
	[log_out_time] [datetime] NULL,
	[updated_at] datetime,
	FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE)

create table [dbo].[sp_logs](
		[sp_log_id] [bigint] IDENTITY(1,1) PRIMARY KEY,
		[sp_name] [varchar](100) null,
		[status] [varchar](10) not null,
		[info_message] [varchar](255),
		[error_no] varchar(100),
		[error_msg] varchar(1000),
		[updated_at] datetime
	)
	
create table [dbo].[system_logs](
		[sys_log_id] [bigint] IDENTITY(1,1) PRIMARY KEY,
		[user_id] [varchar](40) not null,
		[message] [varchar](255),
		[log_at] datetime,
		FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE)
		

drop table  if exists defeault_timestamp
CREATE TABLE defeault_timestamp (get_date DATETIME DEFAULT  dateadd(hh,+10,GETDATE()))
```

#### 3. Stored Procedures and Functions

Created functions and stored procedures for database interaction between Python Code and writing data in RDBMS. This adds a layer of security.

```
CREATE FUNCTION dbo.fx_generate_user_id ()
returns varchar(40) as
	begin
	declare @fourdigit int = (select count(1) from csmsc_209.dbo.users) + 1;
	declare @output varchar(40)
	set @output = (SELECT 'USR' + replicate('0',4 - len(@fourdigit)) + cast( @fourdigit as varchar(4)) + replace(CONVERT(varchar, getdate(), 8),':',''))
	return @output
	end


CREATE FUNCTION dbo.fx_generate_role_id ()
returns varchar(10) as
	begin
	declare @fourdigit int = (select count(1) from csmsc_209.dbo.roles) + 1;
	declare @output varchar(40)
	set @output = (SELECT 'ROLEID' + replicate('0',4 - len(@fourdigit)) + cast( @fourdigit as varchar(4)))
	return @output
	end
	
CREATE procedure [dbo].[sp_user_registration](
	@username varchar(50),
	@firstname varchar(100),
	@lastname varchar(100),
	@gender varchar(255),
	@mobile_no varchar(255),
	@birthday varchar(255),
	@complete_address varchar(1000),
	@height varchar(255),
	@weight varchar(255),
	@password varchar(100),
	@role varchar(10),
	@new_user_id varchar(100) output)
as
	SET NOCOUNT ON;
	declare @chk_role int  = (select case when UPPER(@role) in ('ADMIN', 'PATIENT', 'NURSE', 'DOCTOR') then 1 else 0 end);
	declare @var_id varchar(100) = (select dbo.fx_generate_user_id ());
	BEGIN TRY 

		if (@chk_role = 1)
			Insert into csmsc_209.dbo.users(user_id, role, first_name, last_name, gender, mobile_number, birthday, complete_address, height, weight, user_name, password, created_at)
			select
				@var_id,
				@role,
				@firstname,
				@lastname,
				@gender,
				@mobile_no,
				@birthday,
				@complete_address,
				@height,
				@weight,
				@username,
				@password,
				getdate();
		else
			RAISERROR ('ROLE SHOULD BE ADMIN, PATIENT, DOCTOR or NURSE', 16,  1 ); 
	
		set @new_user_id = @var_id;
	END TRY 
	BEGIN CATCH
		Insert  into csmsc_209.dbo.sp_logs (status, error_no, error_msg)
		select 'ERROR', ERROR_NUMBER(), ERROR_MESSAGE();
		set @new_user_id = 'ERROR';
	END CATCH



ALTER procedure [dbo].[sp_user_registration_simple](
	@username varchar(50),
	@password varchar(100),
	@firstname varchar(100),
	@lastname varchar(100),
	@role varchar(10))
as
	SET NOCOUNT ON;
	declare @chk_role int  = (select case when UPPER(@role) in ('ADMIN', 'PATIENT', 'NURSE', 'DOCTOR') then 1 else 0 end);
	declare @var_id varchar(100) = (select dbo.fx_generate_user_id ());
	declare @current_date datetime = dateadd(hh,+8,GETDATE())
	BEGIN TRY 

		if (@chk_role = 1)
		begin
			Insert into csmsc_209.dbo.users(user_id, role, first_name, last_name, user_name, password, created_at, updated_at)
			select
				@var_id,
				@role,
				@firstname,
				@lastname,
				@username,
				@password,
				@current_date,
				@current_date;
		end
		else
		begin
			RAISERROR ('ROLE SHOULD BE ADMIN, PATIENT, DOCTOR or NURSE', 16,  1 );
		end
		exec dbo.sp_user_login_record @user_id = @var_id;
		select @var_id;
	END TRY 
	BEGIN CATCH
		Insert  into csmsc_209.dbo.sp_logs (status, error_no, error_msg, updated_at)
		select 'ERROR', ERROR_NUMBER(), ERROR_MESSAGE(), @current_date;
		SELECT 'ERROR';
	END CATCH
	
ALTER procedure [dbo].[sp_user_login_record](
	@user_id varchar(50)
)
as
	declare @current_date datetime = dateadd(hh,+8,GETDATE())

	insert into dbo.user_logs (user_id, log_in_time, status, updated_at)
	values(@user_id,@current_date, 'A', @current_date);
	
ALTER procedure [dbo].[sp_user_login](
	@userid varchar(40)
	)
as
	declare @chk_status varchar(1) = (SELECT ul.status from dbo.user_logs ul where user_id = @userid);
	declare @current_date datetime = dateadd(hh,+8,GETDATE())

	if (@chk_status = 'A' or @chk_status = 'I')
	begin
		exec [dbo].[sys_log_insert] @userid, 'USER MUST BE LOGGED OUT FIRST';
	end
	else if (@chk_status = 'X')
	begin
		update dbo.user_logs
		set  log_in_time = @current_date, status = 'A',  updated_at = @current_date
		where user_id = @userid;

		exec [dbo].[sys_log_insert] @userid, 'SUCCESSFULLY LOGGED IN';
	end

		
ALTER procedure [dbo].[sp_user_logout](
	@userid varchar(50)
	)
as
	declare @chk_status varchar(1) = (SELECT status from dbo.user_logs where user_id = @userid);
	declare @current_date datetime = dateadd(hh,+8,GETDATE())

	set @chk_status = (select coalesce(@chk_status, 'E'));

	if (@chk_status = 'E')
	begin
		exec [dbo].[sys_log_insert] @userid,'USERID NOT FOUND'
	end
	else if (@chk_status = 'A' or @chk_status = 'I')
	begin
		UPDATE dbo.user_logs set status = 'X', log_out_time = @current_date, updated_at = @current_date where user_id = @userid ;
		exec [dbo].[sys_log_insert] @userid,'SUCCESSFULLY LOGGED OUT';
	end
	else if (@chk_status = 'X')
	begin
		exec [dbo].[sys_log_insert] @userid, 'ALREADY LOGGED OUT';
	end
	
alter procedure dbo.sp_add_diary_record (@userid varchar(50), @bp_systolic int, @bp_diastolic int)
as
	declare @current_date datetime = dateadd(hh,+8,GETDATE())
	begin try 
		insert into dbo.diary(user_id, bp_systolic, bp_diastolic, created_at, updated_at)
		select @userid, @bp_systolic, @bp_diastolic, @current_date, @current_date;
		exec [dbo].[sys_log_insert] @userid, 'SUCCESSFULLY ADDED RECORD';
	end try
	BEGIN CATCH
		Insert  into csmsc_209.dbo.sp_logs (sp_name, status, error_no, error_msg, updated_at)
		select 'sp_add_diary_record', 'ERROR', ERROR_NUMBER(), ERROR_MESSAGE(), @current_date;
		exec [dbo].[sys_log_insert] @userid, 'ERROR IN ADDING RECORD';
	END CATCH

alter procedure dbo.sp_edit_diary_record ( @diary_id int, @userid varchar(40), @new_bp_systolic int, @new_bp_diastolic int)
as
	declare @current_date datetime = dateadd(hh,+8,GETDATE())
	declare @role varchar(10) = (select top 1 role from csmsc_209.dbo.users where user_id = @userid);
	declare @chk_editor int = (select case when user_id = @userid and @role = 'PATIENT' then 1 else
							case when  @role in ('ADMIN', 'DOCTOR', 'NURSE') then 1 else 0 end
						end from  csmsc_209.dbo.diary where diary_id = @diary_id);

	begin try

		if  (@chk_editor = 1)
		begin
			update csmsc_209.dbo.diary set bp_systolic = @new_bp_systolic, bp_diastolic = @new_bp_diastolic, last_update_by = @userid,
			updated_at = @current_date where diary_id = @diary_id;
			exec [dbo].[sys_log_insert] @userid, 'SUCCESSFULLY UPDATED RECORD';
		end
		else
		begin
			RAISERROR ('ONLY EDITABLE FOR PATIENT, ASSIGNED NURSE, DOCTOR or ADMIN', 16,  1 );
		end
	END TRY
	BEGIN CATCH
		Insert  into csmsc_209.dbo.sp_logs (sp_name, status, error_no, error_msg, updated_at)
		select 'sp_edit_diary_record', 'ERROR', ERROR_NUMBER(), ERROR_MESSAGE(), @current_date;
		exec [dbo].[sys_log_insert] @userid, 'FAILED TO UPDATE RECORD';
	END CATCH

ALTER procedure [dbo].[sys_log_insert](
	@userid varchar(50),
	@message varchar(255)
	)
as
	declare @current_date datetime = dateadd(hh,+8,GETDATE())
	insert into [csmsc_209].[dbo].[system_logs] (user_id, message, log_at)
	select @userid, @message,  @current_date
	

CREATE function [dbo].[fx_get_user_id](
	@username varchar(50),
	@password varchar(100)
)
returns varchar(40) as
begin
	declare @chk_status varchar(40) = (select coalesce((select user_id from dbo.users where user_name = @username and password = @password),'ERROR'));
	
	return @chk_status
end



alter procedure dbo.sp_delete_diary_record (@diary_id int, @userid varchar(50))
as
	declare @current_date datetime = dateadd(hh,+8,GETDATE())
	declare @message varchar(255);
	declare @chk_val varchar(10) = (select 
										case
										when u.role = 'ADMIN' then 1
										when u.role = 'PATIENT' and d.user_id = @userid then 1
										else 0 end
										from dbo.users u left join dbo.diary d on u.user_id = d.user_id where diary_id = @diary_id )

	begin try
		if @chk_val = 1
			begin
				delete from  dbo.diary where diary_id = @diary_id;
				set @message = 'DELETE DIARY ID ' + cast(@diary_id as varchar(100)) +  ' at ' + convert(varchar(100), @current_date, 100)
				exec [dbo].[sys_log_insert] @userid, @message;
			end
		else
			begin
				set @message = 'UNABLE TO DELETE DIARY RECORD ' + cast(@diary_id as varchar(100)) +  ' DUE TO ROLE BEING NOT AN ADMIN';
				exec [dbo].[sys_log_insert] @userid, @message;
			end
	end try
	BEGIN CATCH
		set @message = 'UNABLE TO DELETE DIARY RECORD ' + cast(@diary_id as varchar(100)) +  ' DUE TO ROLE BEING NOT AN ADMIN';
		Insert  into csmsc_209.dbo.sp_logs (sp_name, status, error_no, error_msg, updated_at)
		select 'sp_delete_diary_record', 'ERROR', ERROR_NUMBER(), ERROR_MESSAGE(), @current_date;
		exec [dbo].[sys_log_insert] @userid, @message;
	END CATCH



create procedure dbo.sp_edit_user ( @userid varchar(40),
@new_firstname varchar(100),  
@new_lastname varchar(100), 
@new_username varchar(100),
@new_mobile_number varchar(100), 
@new_birthday varchar(100),  
@new_gender varchar(100), 
@new_complete_address varchar(1000),  
@new_height varchar(100),  
@new_weight varchar(100))
as
	declare @current_date datetime = dateadd(hh,+8,GETDATE())
	declare @role varchar(10) = (select top 1 role from csmsc_209.dbo.users where user_id = @userid);
	declare @chk_editor int = (select case when user_id = @userid and @role = 'PATIENT' then 1 else
							case when  @role in ('ADMIN', 'DOCTOR', 'NURSE') then 1 else 0 end
						end from  csmsc_209.dbo.users where user_id = @userid);

	begin try
		if  (@chk_editor = 1)
		begin
			update csmsc_209.dbo.users 
			set
			first_name = @new_firstname,
			last_name = @new_lastname,
			user_name = @new_username,
			mobile_number = @new_mobile_number,
			birthday = @new_birthday,
			gender = @new_gender,
			complete_address = @new_complete_address,
			height = @new_height,
			weight = @new_weight
			where user_id = @userid;
			exec [dbo].[sys_log_insert] @userid, 'SUCCESSFULLY UPDATED RECORD';
		end
		else
		begin
			RAISERROR ('ONLY EDITABLE FOR PATIENT, ASSIGNED NURSE, DOCTOR or ADMIN', 16,  1 );
		end
	END TRY
	BEGIN CATCH
		Insert  into csmsc_209.dbo.sp_logs (sp_name, status, error_no, error_msg, updated_at)
		select 'sp_edit_user', 'ERROR', ERROR_NUMBER(), ERROR_MESSAGE(), @current_date;
		exec [dbo].[sys_log_insert] @userid, 'FAILED TO UPDATE RECORD';
	END CATCH
```

#### 4. Views

Another layer of security for data extraction. Linked account for database will only access views and stored procedures.

```
create view dbo.vw_most_recent_user_logs as
with max_cte (sys_log_id, user_id, message)  as (
	select
	a.sys_log_id,
	a.user_id,
	a.message
	from dbo.system_logs a join ( 
	select max(sys_log_id) as sys_log_id, user_id  from dbo.system_logs group by user_id) b on a.sys_log_id = b.sys_log_id and a.user_id = b.user_id
)

select
ul.user_id,
coalesce(m.message, 'NO MESSAGE') as message
from dbo.user_logs ul left join max_cte m on ul.user_id = m.user_id


create view dbo.vw_get_diary as
select
d.diary_id,
d.user_id,
bp_systolic, 
bp_diastolic, 
convert(varchar, d.created_at, 120) [logged_date],
comments = concat( coalesce('UPDATED BY ' + u2.first_name + ' ' + u2.last_name, 'ADDED BY USER '), ' at ', convert(varchar, d.updated_at, 100))
from dbo.diary d join dbo.users u1 on d.user_id = u1.user_id
left join dbo.users u2 on d.last_update_by = u2.user_id


create view dbo.vw_get_all_patient as

select user_id, first_name, last_name, gender, mobile_number, birthday, complete_address, height, weight, user_name from users
where role = 'PATIENT'
```

#### 5. Python Interface in AWS Lambda

main.py python file containing all interactions with RDBMS. This is deployed on AWS Lambda.

```

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

```
