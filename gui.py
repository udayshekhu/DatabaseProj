import tkinter as tk
from tkinter import *
from tkinter import ttk
import pyodbc
import pandas as pd
import pandastable
import numpy as np
from pandastable import Table, TableModel, config

# ----------- Connection Parameters---------
server = 'uranium.cs.umanitoba.ca'
database = 'cs3380'
username = 'shekhawu'
password = '7932995'
root = tk.Tk()

def connect_to_db():
    cnx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                             'SERVER=' +server+
                             ';DATABASE='+database+
                             ';UID='+username+
                             ';PWD=' + password
                             ,autocommit=True)
    print('Connection Success')
    return cnx

def sanitize_input(inp):
    inp = str(inp)
    inp = inp.lower()
    inp = inp.replace(';','')
    inp = inp.replace('select','')
    inp = inp.replace('update','')
    inp = inp.replace('drop','')
    inp = inp.replace('delete','')
    return inp

def createdb(dbConnection):
    cursor = dbConnection.cursor()

    #Dropping
    dropQuery = """
    DROP TABLE IF EXISTS Play_Rebounds;
    DROP TABLE IF EXISTS Won;
    DROP TABLE IF EXISTS Draft_Records;
    DROP TABLE IF EXISTS Awards;
    DROP TABLE IF EXISTS CEO_Wealth;
    DROP TABLE IF EXISTS Player;
    DROP TABLE IF EXISTS Team;
    DROP TABLE IF EXISTS CEO;
    DROP TABLE IF EXISTS League;
    DROP TABLE IF EXISTS Home_Stadium;
    DROP TABLE IF EXISTS Head_Coach;
    DROP TABLE IF EXISTS College;
    """
    try:
        cursor.execute(dropQuery)
        print("Dropping Success")
    except:
        print("Dropping Failed")

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
    minutes_played decimal NOT NULL,
    games_played int NOT NULL,
    points float,
    assists float,
    fg_pct float,
    threepoint_pct float,
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
        cursor.execute(newTableQuery)
        print("Creation Success")
        cursor.close()
    except:
        print("Creation Failed")

def populatedb(dbConnection):
    dfTeams = pd.read_csv('teams.csv')
    dfColleges = pd.read_csv('colleges.csv')
    dfAwards = pd.read_csv('awards.csv')
    dfPlayers = pd.read_csv('players.csv')
    dfPlayers = dfPlayers.fillna(np.nan).replace([np.nan], [None])
    cursor = dbConnection.cursor()
    print('Please Wait for Data Insertion')

    try:
        #College Table
        for index,row in dfColleges.iterrows():
            cursor.execute("INSERT INTO College (college_name,country,us_state) values(?,?,?)",row.College, row.Country, row.State)
            dbConnection.commit()

        #Head Coach Table
        for index,row in dfTeams.iterrows():
            cursor.execute("INSERT INTO Head_Coach(hcid,fname,lname,age) values(?,?,?,?)",row.Hcid,row.Hcfname,row.Hclname,row.Hcage)
            dbConnection.commit()

        #Home Stadium Table
        for index,row in dfTeams.iterrows():
            cursor.execute("INSERT INTO Home_Stadium(stadium_id,stadium_name,us_state,city,capacity) values(?,?,?,?,?)",row.Sid,row.Stadium,row.State,row.City,row.Capacity)
            dbConnection.commit()

        #League Table
        cursor.execute("INSERT INTO League(league_name,commissionerFname,commissionerLname) values(?,?,?)",'NBA','Adam','Silver')
        dbConnection.commit()

        #CEO Table
        for index,row in dfTeams.iterrows():
            cursor.execute("INSERT INTO CEO(cid,fname,lname) values(?,?,?)",row.Cid,row.Cfname,row.Clname)
            dbConnection.commit()

        #Team Table
        for index,row in dfTeams.iterrows():
            cursor.execute("INSERT INTO Team(wins,losses,win_pct,teamname,abrv,conference,division,us_state,city,cid,stadium_id,league_name,hcid) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",row.Wins,row.Losses,row.Win_pct,row.Teamname,row.Abrv,row.Conference,row.Division,row.State,row.City,row.Cid,row.Sid,'NBA',row.Hcid)
            dbConnection.commit()

        print('Almost Done, Long Insertion Incoming')

        #Player Table
        for index,row in dfPlayers.iterrows():
            cursor.execute("INSERT INTO Player(pid,minutes_played,games_played,points,assists,fg_pct,threepoint_pct,fname,lname,age,country,salary,weight,height,hcid,teamname,college_name) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row.pid,row.MP,row.G,row.PTS,row.AST,row['FG%'],row['3P%'],row.fname,row.lname,row.Age,row.Country,row.Salary,row.Weight,row.Height,row.hcid,row.Tm,row.CollegeName)
            dbConnection.commit()

        #Net Worth Table
        for index,row in dfTeams.iterrows():
            cursor.execute("INSERT INTO CEO_Wealth(cid,net_worth) values(?,?)",row.Cid,row.networth)
            dbConnection.commit()

        #Award Table
        for index,row in dfAwards.iterrows():
            cursor.execute("INSERT INTO Awards(award_type,bonus) values(?,?)",row.Title,row.Bonus)
            dbConnection.commit()

        #Draft Records
        for index,row in dfPlayers.iterrows():
            cursor.execute("INSERT INTO Draft_Records(pid,draft_year,draft_round,draft_pick) values(?,?,?,?)",row.pid,row['draft_year'],row['draft_round'],row['draft_number'])
            dbConnection.commit()

        #Won
        for index,row in dfAwards.iterrows():
            cursor.execute("INSERT INTO Won(pid,award_type) values(?,?)",row.Pid,row.Title)
            dbConnection.commit()

        #Rebounds
        for index,row in dfPlayers.iterrows():
            cursor.execute("INSERT INTO Play_Rebounds(pid,off_rebounds,def_rebounds) values(?,?,?)",row.pid,row.ORB,row.DRB)
            dbConnection.commit()
        print('Data Insertion Success')
        cursor.close()
        dbConnection.close()
    except:
        print('Data Insertion Failed')

def main():
    #dbConnection = connect_to_db()
    #createdb(dbConnection)
    #populatedb(dbConnection)
    createGUI()

def createGUI():

    root.title("NBA Database")
    style = ttk.Style(root)
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")
    style.configure('lefttab.TNotebook', tabposition='ws')

    tab_control = ttk.Notebook(root, style='lefttab.TNotebook')

    # Define the tabs
    youngest_player_tab = ttk.Frame(tab_control)
    awards_bonuses_tab = ttk.Frame(tab_control)
    highest_salary_tab = ttk.Frame(tab_control)
    top_coaches_tab = ttk.Frame(tab_control)
    top_players_assists_tab = ttk.Frame(tab_control)
    top_players_points_tab = ttk.Frame(tab_control)
    richest_ceo_tab = ttk.Frame(tab_control)
    stadium_by_capacity_tab = ttk.Frame(tab_control)
    college_by_players_produced_tab = ttk.Frame(tab_control)

    #Tab Controls
    tab_control.add(youngest_player_tab, text='Best Young Players')
    tab_control.add(awards_bonuses_tab, text="Award Bonus Amount")
    tab_control.add(highest_salary_tab, text="Highest Salaries")
    tab_control.add(top_coaches_tab, text="Top Coaches by Wins")
    tab_control.add(top_players_assists_tab, text="Top Players by Assists")
    tab_control.add(top_players_points_tab, text="Top Players by Points")
    tab_control.add(richest_ceo_tab, text="Wealthiest CEO")
    tab_control.add(stadium_by_capacity_tab, text="Stadium by Capacity")
    tab_control.add(college_by_players_produced_tab, text="College by Players Produced")

    # youngest_player_tab
    labelText = """
    \t Search for best player under X age in terms of high points or high assists
    \n\t X input should be an integer within [0-50]
    \n\t Example: If age = 25, finds best players under 25 years old
    """
    youngest_player_title= ttk.Label(youngest_player_tab, text=labelText)
    youngest_player_title.pack()
    youngest_player_label = ttk.Label(youngest_player_tab, text='Enter Age:')
    youngest_player_label.pack()
    youngest_player_entry = ttk.Entry(youngest_player_tab)
    youngest_player_entry.pack()
    youngest_player_button = ttk.Button(youngest_player_tab, text='Search', command=lambda: youngest_player(youngest_player_entry.get(),youngest_player_tab))
    youngest_player_button.pack()

    # awards_bonuses_tab
    labelText = """
    \t Search for all award winners that won a bonus amount greater than or equal to X
    \n\t X input should be an integer within [0-1000000]
    \n\t Example: If bonus = 100000, finds all award winners rewarded with more than $100000
    """
    awards_bonuses_title= ttk.Label(awards_bonuses_tab, text=labelText)
    awards_bonuses_title.pack()
    awards_bonuses_label = ttk.Label(awards_bonuses_tab, text='Enter Bonus:')
    awards_bonuses_label.pack()
    awards_bonuses_entry = ttk.Entry(awards_bonuses_tab)
    awards_bonuses_entry.pack()
    awards_bonuses_button = ttk.Button(awards_bonuses_tab, text='Search', command=lambda: awards_bonuses(awards_bonuses_entry.get(),awards_bonuses_tab))
    awards_bonuses_button.pack()

    # highest_salary
    labelText = """
    \t Search for all players having a salary greater than or equal to X
    \n\t X input should be an integer within [0-45780966]
    \n\t Example: If salary = 30000000, finds players with salary above 30 million
    """
    highest_salary_title= ttk.Label(highest_salary_tab, text=labelText)
    highest_salary_title.pack()
    highest_salary_label = ttk.Label(highest_salary_tab, text='Enter Salary:')
    highest_salary_label.pack()
    highest_salary_entry = ttk.Entry(highest_salary_tab)
    highest_salary_entry.pack()
    highest_salary_button = ttk.Button(highest_salary_tab, text='Search', command=lambda: highest_salary(highest_salary_entry.get(),highest_salary_tab))
    highest_salary_button.pack()

    # top_coaches
    labelText = """
    \t Search for the top X coaches who have the most wins
    \n\t X input should be an integer within [0-30]
    \n\t Example: If amount = 10, finds top 10 coaches in the league in terms of wins
    """
    top_coaches_title= ttk.Label(top_coaches_tab, text=labelText)
    top_coaches_title.pack()
    top_coaches_label = ttk.Label(top_coaches_tab, text='Enter Amount:')
    top_coaches_label.pack()
    top_coaches_entry = ttk.Entry(top_coaches_tab)
    top_coaches_entry.pack()
    top_coaches_button = ttk.Button(top_coaches_tab, text='Search', command=lambda: top_coaches(top_coaches_entry.get(),top_coaches_tab))
    top_coaches_button.pack()

    # top_players_assists
    labelText = """
    \t Search for the top X players who have the most assists per game
    \n\t X input should be an integer within [0-605]
    \n\t Example: If amount = 20, finds top 20 players in the league in terms of assists per game
    """
    top_players_assists_title= ttk.Label(top_players_assists_tab, text=labelText)
    top_players_assists_title.pack()
    top_players_assists_label = ttk.Label(top_players_assists_tab, text='Enter Amount:')
    top_players_assists_label.pack()
    top_players_assists_entry = ttk.Entry(top_players_assists_tab)
    top_players_assists_entry.pack()
    top_players_assists_button = ttk.Button(top_players_assists_tab, text='Search', command=lambda: top_players_assists(top_players_assists_entry.get(),top_players_assists_tab))
    top_players_assists_button.pack()

    # top_players_points
    labelText = """
    \t Search for the top X players who have the most points per game
    \n\t X input should be an integer within [0-605]
    \n\t Example: If amount = 15, finds top 15 players in the league in terms of points per game
    """
    top_players_points_title= ttk.Label(top_players_points_tab, text=labelText)
    top_players_points_title.pack()
    top_players_points_label = ttk.Label(top_players_points_tab, text='Enter Amount:')
    top_players_points_label.pack()
    top_players_points_entry = ttk.Entry(top_players_points_tab)
    top_players_points_entry.pack()
    top_players_points_button = ttk.Button(top_players_points_tab, text='Search', command=lambda: top_players_points(top_players_points_entry.get(),top_players_points_tab))
    top_players_points_button.pack()

    # richest_ceo
    labelText = """
    \t Search for the CEOs who have a net worth greater than or equal to X (in billions)
    \n\t X input should be an decimal within [0-74.6]
    \n\t Example: If amount = 30, finds CEOs who have a net worth >=30 billion
    """
    richest_ceo_title= ttk.Label(richest_ceo_tab, text=labelText)
    richest_ceo_title.pack()
    richest_ceo_label = ttk.Label(richest_ceo_tab, text='Enter Net Worth(billions):')
    richest_ceo_label.pack()
    richest_ceo_entry = ttk.Entry(richest_ceo_tab)
    richest_ceo_entry.pack()
    richest_ceo_button = ttk.Button(richest_ceo_tab, text='Search', command=lambda: richest_ceo(richest_ceo_entry.get(),richest_ceo_tab))
    richest_ceo_button.pack()

    # stadium_by_capacity
    labelText = """
    \t Search for the Stadiums who have a capacity greater than or equal to X
    \n\t X input should be an integer within [0-20917]
    \n\t Example: If amount = 19700, finds Stadiums who have a capacity >= 19700
    """
    stadium_by_capacity_title= ttk.Label(stadium_by_capacity_tab, text=labelText)
    stadium_by_capacity_title.pack()
    stadium_by_capacity_label = ttk.Label(stadium_by_capacity_tab, text='Enter Minimum Capacity:')
    stadium_by_capacity_label.pack()
    stadium_by_capacity_entry = ttk.Entry(stadium_by_capacity_tab)
    stadium_by_capacity_entry.pack()
    stadium_by_capacity_button = ttk.Button(stadium_by_capacity_tab, text='Search', command=lambda: stadium_by_capacity(stadium_by_capacity_entry.get(),stadium_by_capacity_tab))
    stadium_by_capacity_button.pack()

    # college_by_players_produced
    labelText = """
    \t Search for colleges that have produced at least X players
    \n\t X input should be an integer within [0-26]
    \n\t Example: If amount = 5, finds colleges that have produced at least 5 NBA players
    """
    college_by_players_produced_title= ttk.Label(college_by_players_produced_tab, text=labelText)
    college_by_players_produced_title.pack()
    college_by_players_produced_label = ttk.Label(college_by_players_produced_tab, text='Enter Minimum Players Produced:')
    college_by_players_produced_label.pack()
    college_by_players_produced_entry = ttk.Entry(college_by_players_produced_tab)
    college_by_players_produced_entry.pack()
    college_by_players_produced_button = ttk.Button(college_by_players_produced_tab, text='Search', command=lambda: college_by_players_produced(college_by_players_produced_entry.get(),college_by_players_produced_tab))
    college_by_players_produced_button.pack()

    # Pack the tab control and start the GUI loop
    tab_control.pack(expand=1, fill='both')
    root.mainloop()

def youngest_player(age, youngest_player_tab):
    age = sanitize_input(age)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT fname, lname, teamname, age, points, assists FROM Player WHERE age<= ?
        GROUP BY fname, lname, teamname, age, points, assists HAVING points>20 OR assists>8
        ORDER BY  age ASC""", age)
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def awards_bonuses(bonusAmt, awards_bonuses_tab):
    bonusAmt = sanitize_input(bonusAmt)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT fname, lname, teamname, Awards.award_type, bonus FROM Player
        JOIN Won on Player.pid = Won.pid
        JOIN Awards on Awards.award_type = Won.award_type
        WHERE bonus>= ?
        GROUP BY fname, lname, teamname, Awards.award_type, bonus 
        ORDER BY bonus ASC""", bonusAmt)
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def highest_salary(salaryAmt, highest_salary_tab):
    salaryAmt = sanitize_input(salaryAmt)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT fname, lname, teamname, salary
        FROM Player WHERE salary >= ?
        GROUP BY fname, lname, teamname, salary
        ORDER BY salary""", salaryAmt)
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def top_coaches(topAmt, top_coaches_tab):
    topAmt = sanitize_input(topAmt)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT TOP (?) fname, lname, wins, losses, teamname FROM Head_Coach
        JOIN Team on Head_Coach.hcid = Team.hcid
        ORDER BY wins DESC""", int(topAmt))
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def top_players_assists(topAmt, top_players_assists_tab):
    topAmt = sanitize_input(topAmt)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT TOP(?) fname, lname, teamname, assists FROM Player
        ORDER BY assists DESC""", int(topAmt))
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def top_players_points(topAmt, top_players_points_tab):
    topAmt = sanitize_input(topAmt)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT TOP(?) fname,lname,teamname,points FROM Player
        ORDER BY points DESC """, int(topAmt))
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def richest_ceo(net_worth, richest_ceo_tab):
    net_worth = sanitize_input(net_worth)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT fname, lname, net_worth, teamname FROM CEO
        JOIN CEO_Wealth on CEO.cid= CEO_Wealth.cid
        JOIN Team on CEO.cid=Team.cid WHERE net_worth>= ?
        GROUP BY fname, lname, net_worth, teamname ORDER BY net_worth """, net_worth)
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def stadium_by_capacity(capacity, stadium_by_capacity_tab):
    capacity = sanitize_input(capacity)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT teamname, stadium_name, capacity, Team.city
        FROM Home_Stadium
        JOIN Team on Home_Stadium.stadium_id = Team.stadium_id
        WHERE capacity>= ?
        GROUP BY teamname, stadium_name, Team.city, capacity 
        ORDER BY capacity""", capacity)
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def college_by_players_produced(numProduced, college_by_players_produced_tab):
    numProduced = sanitize_input(numProduced)
    dbConnection = connect_to_db()
    cursor = dbConnection.cursor()
    try:
        cursor.execute(f"""SELECT College.college_name, College.country, us_state, COUNT (pid) AS 'num_players'
        FROM College
        JOIN Player on College.college_name = Player.college_name
        GROUP BY College.college_name, College.country, us_state
        HAVING COUNT('num_players') >= ?
        ORDER BY 'num_players'
        """, numProduced)
        result = [{cursor.description[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        openNewWindow(pd.DataFrame(result))
    except Exception as inst:
        print(inst)
        print('Failed Query')
    dbConnection.close()

def openNewWindow(df):
    extraWindow = Toplevel(root)
    extraWindow.title("Results of Query")
    extraWindow.geometry('600x400+200+400')
    frame = tk.Frame(extraWindow)
    frame.pack(fill='both', expand=True)
    pt = Table(frame, dataframe=df)
    pt.show()

if __name__ == "__main__":
    main()
