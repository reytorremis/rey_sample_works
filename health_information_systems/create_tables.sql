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
