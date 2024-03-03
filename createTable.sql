CREATE TABLE College (
    college_name varchar(100) PRIMARY KEY NOT NULL,
    country varchar(100) NOT NULL,
    us_state varchar(100) NOT NULL,
    city varchar(100) NOT NULL
);

CREATE TABLE Head_Coach (
    hcid int NOT NULL PRIMARY KEY,
    fname varchar(100) NOT NULL,
    lname varchar(100) NOT NULL,
    age int NOT NULL
);

CREATE TABLE Home_Stadium (
    stadium_name varchar(100) PRIMARY KEY NOT NULL,
    us_state varchar(100) NOT NULL,
    city varchar(100) NOT NULL
);

CREATE TABLE League (
    league_name varchar(10) PRIMARY KEY NOT NULL,
    commissioner varchar(100) NOT NULL
);

CREATE TABLE CEO (
    cid int PRIMARY KEY NOT NULL,
    fname varchar(100) NOT NULL,
    lname varchar(100) NOT NULL
);

CREATE TABLE Team (
    wins int NOT NULL,
    losses int NOT NULL,
    win_pct decimal NOT NULL,
    teamname varchar(100) PRIMARY KEY NOT NULL,
    abrv varchar(10) NOT NULL,
    conference varchar(100) NOT NULL,
    division varchar(100) NOT NULL,
    us_state varchar(100) NOT NULL,
    city varchar(100) NOT NULL,
    cid int REFERENCES CEO(cid),
    stadium_name varchar(100) REFERENCES Home_Stadium(stadium_name),
    league_name varchar(10) REFERENCES League(league_name),
    hcid int REFERENCES Head_Coach(hcid)
);

CREATE TABLE Player (
    pid int NOT NULL PRIMARY KEY,
    minutes_played int NOT NULL,
    games_played int NOT NULL,
    points int, 
    assists int,
    fg_pct decimal,
    threepoint_pct decimal,
    fname varchar(100) NOT NULL, 
    lname varchar(100) NOT NULL,
    age int NOT NULL,
    country varchar(100) NOT NULL, 
    salary money NOT NULL, 
    weight decimal NOT NULL,
    height decimal NOT NULL,
    hcid int REFERENCES Head_Coach(hcid),
    teamname varchar(100) REFERENCES Team(teamname),
    college_name varchar(100) REFERENCES College(college_name)
);

CREATE TABLE CEO_Wealth (
   cid int REFERENCES CEO(cid),
   net_worth money NOT NULL 
);

CREATE TABLE Awards (
    award_type varchar(100) PRIMARY KEY NOT NULL,
    bonus money NOT NULL
);

CREATE TABLE Draft_Records(
    pid int REFERENCES Player(pid),
    draft_year int,
    draft_round int,
    draft_pick int
);

CREATE TABLE Won(
    pid int REFERENCES Player(pid),
    award_type varchar(100) REFERENCES Awards(award_type)
);

CREATE TABLE Play_Rebounds(
    pid int REFERENCES Player(pid),
    off_rebounds int,
    def_rebounds int
);