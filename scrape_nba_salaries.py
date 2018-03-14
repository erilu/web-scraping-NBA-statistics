import re
import urllib
from urllib import urlopen

# This method finds the urls for each of the rosters in the NBA using regexes.
def build_team_url():
    # Open the webpage containing links to each roster,
    # and extract the names of each roster available.
    f = urllib.urlopen('http://www.espn.com/nba/teams')
    words = f.read().decode('utf-8')
    teams = re.findall("www\.espn\.com/nba/team/_/name/(\w+)/(.+?)\"\sclass", words)

    #Using the names of the rosters, this creates the urls of each roster in the NBA.
    roster_urls = []
    for team in teams:
        #each roster webpage follows this general pattern.
        roster_urls.append('http://www.espn.com/nba/team/roster/_/name/' + team[0] + '/' + team[1])

# This is a method that finds the key of a dictionary, given the value.
# This is used in the calculate_statistics method.
def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dic.items() if v == val][0]

# Using the url of each roster, extract the salary data using regexes and
# perform calculations based on what we have extracted.
def calculate_statistic(rosters,specific_teams):
    # Create empty lists that will contain the statistics.
    average_team_salaries = []
    highest_salary_per_team = []

    # Open each roster, one by one.
    for url in rosters:
        f = urllib.urlopen (url)
        stats = f.read().decode('utf-8')

        # The salaries were embedded in the source code in this format:
        '''
        <a href="http://www.espn.com/nba/player/_/id/3975/stephen-curry">Stephen Curry</a>
        </td><td>PG</td><td >29</td><td >6-3</td><td >190</td><td>Davidson</td><td>$34,382,550</td>
        </tr><tr class="evenrow player-46-3202"><td >35</td><td class="sortcell">
        '''
        # This is the regex pattern to return players and their corresponding salary.
        player_salaries = dict(re.findall('http\://www\.espn\.com/nba/player/_/id/\d*?/.*?\">(\w+\s\w+)</a></td><td>\w*?</td><td >\d*?</td><td >.*?</td><td >\d*?</td><td>.*?</td><td>\$(.*?)</td>', stats))

        # in the dictionary, each player corresponds to a salary. change the salaries from strings to integers.
        for key in player_salaries.keys():
            player_salaries[key] = int(re.sub(',',"", player_salaries[key]))

        # Sort the salaries and append them to the list,
        # Also returns the person with the highest salary
        salaries = list(player_salaries.values())
        highest_salary_per_team.append((find_key(player_salaries,sorted(salaries)[-1]),sorted(salaries)[-1]))
        average_team_salaries.append(sum(salaries)/len(salaries))

    # Prints the average salary out, with the team and salary side by side.
    print ("\n\nAverage Team Salaries in the NBA\n(Average amount spent on each player)\n\n")
    team_with_salary = dict(zip(average_team_salaries, specific_teams ))
    average_team_salaries.sort()
    for key in average_team_salaries:
        print (team_with_salary[key].ljust(30), round(key,2))

    # Prints the highest salaries out, with the team and salary side by side.
    team_with_highest = dict(zip(highest_salary_per_team, specific_teams ))
    highest_salary_per_team.sort(key=lambda highest_salary_per_team: highest_salary_per_team[1])
    print ("\n\nPlayer with the highest salary per team in the NBA\n\n")
    for key in highest_salary_per_team:
        print (team_with_highest[key].ljust(30), key)

# Run the program.
rosters = build_team_url()
f = urllib.urlopen('http://espn.go.com/nba/teams')
words = f.read().decode('utf-8')
teams = re.findall("http\://espn\.go\.com/nba/team/_/name/\w+?/.+?\"\sclass\=\"bi\">(.+?)</a>", words)
calculate_statistic(rosters,teams)