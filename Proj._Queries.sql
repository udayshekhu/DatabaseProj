-- To find the colleges that produced the most players.
SELECT college_name, country, us_state, city, COUNT (pid) AS Number_of_Players_Produced
FROM College JOIN Player on college_name.College=college_name.Player WHERE Number_of_Players_Produced>="%s"
GROUP BY college_name, country, us_state, city ORDER BY Number_of_Players_Produced


-- To find the stadiums with the highest capacity, with their respective teams.
SELECT teamname, stadium_name, capacity FROM Home_Stadium JOIN Team on stadium_name.Home_Stadium= stadium_name.Team WHERE capacity>="%s"
GROUP BY teamname, stadium_name, capacity ORDER BY capacity


-- To find the whealtheast CEOs, with their respective teams.
SELECT fname, lname, net_worth, teamname FROM CEO JOIN CEO_Wealth on cid.CEO=cid.CEO_Wealth JOIN Team on cid.CEO=cid.Team WHERE net_worth>="%s"
GROUP BY fname, lname, net_worth, teamname ORDER BY net_worth


-- To find top X players in term of achieved points.
SELECT TOP("%s") * FROM Player 
GROUP BY fname,lname,points ORDER BY points DESC 


-- To find top X players in term of assists.
SELECT TOP("%s") * FROM Player 
GROUP BY fname, lname, assists ORDER BY assists DESC


--To find top X Coaches in the NBA.
SELECT TOP("%") * FROM Head_Coach JOIN Team on hcid.Head_Coach=hcid.Team
GROUP BY fname, lname, teamname, wins ORDER BY wins DESC 


-- To find top players in term of the highest salary.
SELECT fname, lname, teamname, salary FROM Player WHERE salary>="%s"
GROUP BY fname, lname, teamname, salary ORDER BY salary


-- To find players who won Awards (Bonuses) and the amount of the bonus
SELECT fname, lname, teamname, award_type, bonus FROM Player JOIN Won on pid.Player=pid.Won JOIN Awards on award_type.Awards=award_type.Won WHERE bonus>="%s"
GROUP BY fname, lname, teamname, award_type, bonus ORDER BY bonus


-- To find the youngest, promising players.
SELECT fname, lname, teamname, age, points, assists FROM Player WHERE age<="%s"
GROUP BY fname, lname, teamname, age, points, assists HAVING points>50 OR assists>50


--