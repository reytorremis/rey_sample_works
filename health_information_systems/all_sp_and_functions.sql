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
