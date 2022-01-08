from bs4 import BeautifulSoup
import requests
from datetime import datetime
from classes import Team, Game
from classplus import Tournament

def get_tournament(url, teams=None):
    if teams == None:
        teams = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    tournament_name = str(soup.find("div", {"class": "breadcrumbs"}).find_all("a")[1].contents[0])

    num_pools = len(soup.find_all("div", {"class": "clearfix"})[1].find_all("div", {"class": "pool"}))

    pools = soup.find_all("div", {"class": "pool"})[0:num_pools]
    pools_games = soup.find_all("table", {"class": "global_table scores_table"})
    games = []

    #creates list of teams from pools
    for pool in pools:
        pool_letter = pool.find("h3").contents[0][5]
        for row in pool.find("table").find("tbody").find_all("a"):
            name = row.contents[0].rsplit(' ', 1)[0]
            seed = row.contents[0].split(" ")[-1][1:-1]
            doesTeamExist = False
            for team in teams:
                if team.name == name:
                    doesTeamExist = True
                    break
            if (not doesTeamExist):
                teams.append(Team(name, seed, pool_letter))

    t_year = int(soup.find("span", {"class": "date"}).contents[0].split(" ")[0].split("/")[2])
    t_month = 0
    t_day = 0

    #scrapes pools games
    for pool in pools_games:
        pool_letter = pool.find("th").contents[0][5]
        for row in pool.find("tbody").find_all("tr"):
            if row.has_attr("data-game"):
                teamA_name = row.find_all("td")[3].find("a").contents[0].rsplit(' ', 1)[0]
                teamB_name = row.find_all("td")[4].find("a").contents[0].rsplit(' ', 1)[0]
                teamA, teamB = None, None
                teamA_boolean = False
                teamB_boolean = False
                for team in teams:
                    if team.name == teamA_name:
                        teamA = team
                        teamA_boolean = True
                    elif team.name == teamB_name:
                        teamB = team
                        teamB_boolean = True
                if not teamA_boolean:
                    teamA = Team(teamA_name, row.find_all("td")[3].find("a").contents[0].split(' ')[-1][1:-1],None)
                    teams.append(teamA)
                if not teamB_boolean:
                    teamB = Team(teamB_name, row.find_all("td")[4].find("a").contents[0].split(' ')[-1][1:-1],None)
                    teams.append(teamB)
                teamA_score = row.find_all("td")[5].find_all("span", {"class": "isScore"})[0].find("span").contents[0]
                teamB_score = row.find_all("td")[5].find_all("span", {"class": "isScore"})[1].find("span").contents[0]

                date = row.find_all("td")[0].find("span").contents[0]
                time = row.find_all("td")[1].find("span").contents[0]
                month = int(date[4:date.find('/')])
                day = int(date[date.find('/')+1:len(date)])
                hour = int(time[0:time.find(":")])
                minute = int(time[time.find(":")+1:time.find(":")+3])
                if (time[len(time)-2:len(time)] == "PM" and hour != 12):
                    hour += 12
                game_datetime = datetime(t_year, month, day, hour, minute)

                game = Game(teamA, teamB, teamA_score, teamB_score, game_datetime, pool_letter)
                games.append(game)
                teamA.add_game(game)
                teamB.add_game(game)

    #scrapes bracket and consolation play
    columns = soup.find_all("div", {"class": "bracket_col"})
    for column in columns:
        column_name = column.find("h4", {"class":"col_title"}).contents[0]
        column_games = column.find_all("div", {"class": "bracket_game"})
        for game in column_games:
            game_teams = game.find_all("span", {"class": "team"})
            teamA_name = game_teams[0].contents[0].contents[0].rsplit(' ', 1)[0]
            teamB_name = game_teams[1].contents[0].contents[0].rsplit(' ', 1)[0]
            teamA_boolean = False
            teamB_boolean = False
            for team in teams:
                if team.name == teamA_name:
                    teamA = team
                    teamA_boolean = True
                elif team.name == teamB_name:
                    teamB = team
                    teamB_boolean = True
            if teamA_boolean == False:
                teamA = Team(teamA_name, game_teams[0].contents[0].contents[0].rsplit(' ')[-1][1:-1],None)
                teams.append(teamA)
            if teamB_boolean == False:
                teamB = Team(teamB_name, game_teams[1].contents[0].contents[0].rsplit(' ')[-1][1:-1],None)
                teams.append(teamB)
            team_scores = game.find_all("span", {"class": "score"})
            teamA_score = team_scores[0].contents[0]
            teamB_score = team_scores[1].contents[0]
            game_date = game.find("span", {"class": "date"}).contents[0].split(" ")
            year = int(game_date[0].split("/")[2])
            month = int(game_date[0].split("/")[0])
            day = int(game_date[0].split("/")[1])
            hour = int(game_date[1].split(":")[0])
            minute = int(game_date[1].split(":")[1])
            if (game_date[2] == "PM" and hour != 12):
                    hour += 12
            game_datetime = datetime(year, month, day, hour, minute)
            t_month = month
            t_day = day


            game = Game(teamA, teamB, teamA_score, teamB_score, game_datetime, column_name)
            games.append(game)
            teamA.add_game(game)
            teamB.add_game(game)

    teams.sort()
    games.sort()

    for game in games:
        if game.teamA_score == "W" or game.teamB_score == "W":
            game.teamA.games.remove(game)
            game.teamB.games.remove(game)
            games.remove(game)

    division = soup.find("h1", {"class": "title"}).contents[0]

    return Tournament(tournament_name,teams,games,datetime(t_year,t_month,t_day,0,0),division)
