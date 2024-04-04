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
