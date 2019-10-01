### client's version and update date ###
select oh.history_id hId, o.name, o.current_version, date_format(oh.updated_on, '%d  %M\'%y') as updated_on, oh.howManyUpdates
from organizations as o inner join
	(select max(start_date) updated_on, count(zendesk_id) howManyUpdates, history_id, zendesk_id
    from organizations_history
    group by org_id) oh
    on o.zendesk_id = oh.zendesk_id
    where o.status = 1
    order by o.name;


### client's history update list with dates ###
select oh.history_id hId, o.name, oh.current_version version, date_format(oh.start_date, '%d  %M\'%y') updated, o.org_id
from organizations o 
inner join organizations_history oh
on o.zendesk_id = oh.zendesk_id
where o.status = 1
order by o.name, oh.start_date;



## ADD foreign keys ##
alter table organizations_history
add constraint fk_organizations_history_org_id foreign key (org_id)
references organizations(org_id)
on update cascade on delete restrict;


### Dump query results into a file ###
select id, concat(name, ' - ', current_version)
from organizations 
where status = 1
group by name 
into outfile 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\clients.txt'
fields terminated by "  " optionally enclosed by '"'
lines terminated by '\n';