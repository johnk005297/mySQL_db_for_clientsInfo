
DELIMITER $$

create trigger organizations_history_insert after insert on organizations for each row 
begin
declare N DATE;
set N = now();

insert into organizations_history (name, current_version, org_id, zendesk_id, start_date, end_date)
values (new.name, new.current_version, new.org_id, new.zendesk_id, N, null);
end;


DELIMITER $$

create trigger organizations_history_delete after delete on organizations for each row 
begin
declare N DATE;
set N = now();

UPDATE organizations_history
SET end_date = N
WHERE org_id = OLD.org_id
AND end_date IS NULL;
end;


DELIMITER $$
create trigger organizations_history_update after update on organizations for each row 
begin

declare N DATE;
set N = now();

if old.current_version != new.current_version then

	UPDATE organizations_history
	SET end_date = N
	WHERE org_id = OLD.org_id
	AND end_date IS NULL;

	insert into organizations_history (name, current_version, org_id, zendesk_id, start_date, end_date)
	values (new.name, new.current_version, new.org_id, new.zendesk_id, N, NULL);

end if;
end;
