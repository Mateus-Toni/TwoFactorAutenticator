
create table users(
id_user serial primary key not null,
name_user varchar(255) not null,
last_name varchar(255) not null,
birth_day date not null,
cpf char(14) not null,
password_user varchar(255) not null,
email varchar(255) not null,
nick_name varchar(255) not null
);

create table two_auth(
id_token serial primary key not null,
id_user int not null,
user_token varchar(300),
create_date date,
flag varchar(50),
FOREIGN KEY(id_user) REFERENCES users(id_user)
);

create table revoked_token(
id_token int,
id_user int,
user_token varchar(300),
flag varchar(50),
FOREIGN KEY(id_user) REFERENCES users(id_user),
FOREIGN KEY(id_token) REFERENCES two_auth(id_token)
);

create table code_user(
id_code serial primary key not null,
id_user int not null,
user_code char(6), 
create_date date,
FOREIGN KEY(id_user) REFERENCES users(id_user)
);