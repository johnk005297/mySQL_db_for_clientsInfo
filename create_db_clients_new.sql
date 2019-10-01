create database clients;

create table organizations (
	org_id int unsigned not null auto_increment,
	name varchar(150),
	current_version varchar (50),
	status boolean,
	saas boolean,
	db_maintenance_plan boolean,
	ipad varchar(30),
	mdm varchar(30),
	rent_ipad boolean,
	custom_localization boolean,
	custom_skin_for_ipad boolean,
	custom_server_version boolean,
    zendesk_id varchar(20) unique,
	
	constraint pk_organizations primary key (org_id)
);


create table organizations_history (
	history_id int unsigned not null auto_increment,    
    name varchar(150),
    current_version varchar(50),
    org_id smallint unsigned,
    zendesk_id varchar(20),
    start_date date,
    end_date date,
    constraint pk_organizations_history primary key (history_id, org_id),
    constraint fk_organizations_org_id foreign key (org_id) references organizations(org_id)
    on update cascade on delete restrict
);


create table tickets (		
	id smallint unsigned not null unique,
    status enum('new', 'open', 'pending', 'hold', 'solved', 'closed'),
    subject text,
    type enum('problem', 'incident', 'question', 'task'),
    priority enum('low','normal','high','urgent'),	
    description text,  
    created_at date,
    updated_at date,
    tfs varchar(500),
    reason enum('дубль', 'консультация', 'обновление_системы', 'ошибка_клиента', 'ошибка_разработки', 'проблема_окружения', 'запрос_на_доработку'),  
    tags varchar(300),
	zendesk_org_id varchar(50),    
	requester_id varchar(50),  
    assignee_id varchar(50),
    group_id varchar(50),       
constraint fk_zdsk_org_id foreign key (zendesk_org_id)
	references organizations (zendesk_id)
    on update cascade on delete restrict 
);