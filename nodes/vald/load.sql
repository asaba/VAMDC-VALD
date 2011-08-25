load data infile '/vald/vamdc/db_input_files/species.dat' into table species columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/species_components.dat' into table species_components columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/references.dat' ignore into table refs columns terminated by ';' enclosed by '"' ;
load data infile '/vald/vamdc/db_input_files/linelists.dat' ignore into table linelists columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/linelists_references.dat' ignore into table linelists_references columns terminated by ';' optionally enclosed by '"';

alter table states modify id varchar(255) NOT NULL;
load data infile '/vald/vamdc/db_input_files/upstates.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';
load data infile '/vald/vamdc/db_input_files/lowstates.dat' ignore into table states columns terminated by ';' optionally enclosed by '"';
create temporary table `sids` (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, charid VARCHAR(255) NOT NULL UNIQUE);
insert into sids (charid) select id from states;
update states,sids set states.id=sids.id where states.id=sids.charid;
alter table states modify id INT NOT NULL;

alter table transitions modify upstate varchar(255);
alter table transitions modify lostate varchar(255);
load data infile '/vald/vamdc/db_input_files/transitions.dat' ignore into table transitions columns terminated by ';' optionally enclosed by '"';
update transitions,sids set transitions.upstate=sids.id where transitions.upstate=sids.charid;
update transitions,sids set transitions.lostate=sids.id where transitions.lostate=sids.charid;
alter table transitions modify upstate INT;
alter table transitions modify lostate INT;

update transitions t, linelists ll set t.obstype=ll.obstype where t.wave_linelist_id=ll.id;
