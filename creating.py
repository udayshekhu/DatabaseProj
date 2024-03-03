import pandas as pd
import numpy as np
import pyodbc

def main():
    #do things
    pass

def createTable(myConnection):
    newTableQuery = """
    CREATE TABLE College (
    college_name varchar(100) PRIMARY KEY NOT NULL,
    country varchar(100) NOT NULL,
    us_state varchar(100) NOT NULL
);

CREATE TABLE Head_Coach (
    hcid int NOT NULL PRIMARY KEY,
    fname varchar(100) NOT NULL,
    lname varchar(100) NOT NULL,
    age int NOT NULL
);

CREATE TABLE Home_Stadium (
    stadium_id int PRIMARY KEY,
    stadium_name varchar(100) NOT NULL,
    us_state varchar(100) NOT NULL,
    city varchar(100) NOT NULL,
    capacity int NOT NULL
);

CREATE TABLE League (
    league_name varchar(10) PRIMARY KEY NOT NULL,
    commissionerFname varchar(100) NOT NULL,
    commissionerLname varchar(100) NOT NULL
);

CREATE TABLE CEO (
    cid int NOT NULL PRIMARY KEY,
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
    stadium_id int REFERENCES Home_Stadium(stadium_id),
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
    salary money, 
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
    """
    try:
        myConnection.execute(newTableQuery)
        print("All Tables Created Successfully")
    except:
        print("Attempt to Create Table Unsuccessful") 
    myConnection.commit()

def addData(cursor,myConnection):
    dfTeams = pd.read_csv('teams.csv')
    dfColleges = pd.read_csv('colleges.csv')
    dfAwards = pd.read_csv('awards.csv')
    dfPlayers = pd.read_csv('players.csv')
    dfPlayers = dfPlayers.fillna(np.nan).replace([np.nan], [None])


    #College Table
    for index,row in dfColleges.iterrows():
        cursor.execute("INSERT INTO College (college_name,country,us_state) values(?,?,?)",row.College, row.Country, row.State)
        myConnection.commit()

    #Head Coach Table
    for index,row in dfTeams.iterrows():
        cursor.execute("INSERT INTO Head_Coach(hcid,fname,lname,age) values(?,?,?,?)",row.Hcid,row.Hcfname,row.Hclname,row.Hcage)
        myConnection.commit()

    #Home Stadium Table
    for index,row in dfTeams.iterrows():
        cursor.execute("INSERT INTO Home_Stadium(stadium_id,stadium_name,us_state,city,capacity) values(?,?,?,?,?)",row.Sid,row.Stadium,row.State,row.City,row.Capacity)
        myConnection.commit()

    #League Table
    cursor.execute("INSERT INTO League(league_name,commissionerFname,commissionerLname) values(?,?,?)",'NBA','Adam','Silver')
    myConnection.commit()

    #CEO Table
    for index,row in dfTeams.iterrows():
        cursor.execute("INSERT INTO CEO(cid,fname,lname) values(?,?,?)",row.Cid,row.Cfname,row.Clname)
        myConnection.commit()

    #Team Table
    for index,row in dfTeams.iterrows():
        cursor.execute("INSERT INTO Team(wins,losses,win_pct,teamname,abrv,conference,division,us_state,city,cid,stadium_id,league_name,hcid) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",row.Wins,row.Losses,row.Win_pct,row.Teamname,row.Abrv,row.Conference,row.Division,row.State,row.City,row.Cid,row.Sid,'NBA',row.Hcid)
        myConnection.commit()

    #Player Table
    for index,row in dfPlayers.iterrows():
        cursor.execute("INSERT INTO Player(pid,minutes_played,games_played,points,assists,fg_pct,threepoint_pct,fname,lname,age,country,salary,weight,height,hcid,teamname,college_name) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row.pid,row.MP,row.G,row.PTS,row.AST,row['FG%'],row['3P%'],row.fname,row.lname,row.Age,row.Country,row.Salary,row.Weight,row.Height,row.hcid,row.Tm,row.CollegeName)
        myConnection.commit()

    #Net Worth Table
    for index,row in dfTeams.iterrows():
        cursor.execute("INSERT INTO CEO_Wealth(cid,net_worth) values(?,?)",row.Cid,row.networth)
        myConnection.commit()

    #Award Table
    for index,row in dfAwards.iterrows():
        cursor.execute("INSERT INTO Awards(award_type,bonus) values(?,?)",row.Title,row.Bonus)
        myConnection.commit()

    #Draft Records
    for index,row in dfPlayers.iterrows():
        cursor.execute("INSERT INTO Draft_Records(pid,draft_year,draft_round,draft_pick) values(?,?,?,?)",row.pid,row['draft_year'],row['draft_round'],row['draft_number'])
        myConnection.commit()

    #Won
    for index,row in dfAwards.iterrows():
        cursor.execute("INSERT INTO Won(pid,award_type) values(?,?)",row.Pid,row.Title)
        myConnection.commit()

    #Rebounds
    for index,row in dfPlayers.iterrows():
        cursor.execute("INSERT INTO Play_Rebounds(pid,off_rebounds,def_rebounds) values(?,?,?)",row.pid,row.ORB,row.DRB)
        myConnection.commit()


if __name__ == '__main__':
    main()