from classes import Team, Game
from webscraper import get_tournament
from textscraper import get_games, add_games_to_teams
from algorithm import get_rating_differential, get_score_weight

url = "https://play.usaultimate.org/events/USA-Ultimate-College-Championships-2021/schedule/Men/CollegeMen/d_i_men/"
#url = "https://play.usaultimate.org/events/USA-Ultimate-College-Championships-2021/schedule/Women/CollegeWomen/d_i_women/"
#url = "https://play.usaultimate.org/events/2017-US-Open-Club-Championships/schedule/Boys/youth-club-u-20-boys/"
#url = "https://play.usaultimate.org/events/2018-US-Open-Club-Championships/schedule/Boys/youth-club-u-20-boys/"
#url = "https://play.usaultimate.org/events/2019-US-Open-Club-Championship/schedule/Boys/youth-club-u-20-boys/"
#url = "https://play.usaultimate.org/events/Atlantic-Coast-D-I-College-Mens-Regionals-2021/schedule/Men/CollegeMen/"

#scrapes usau website
tournament = get_tournament(url)
name = tournament.name
teams = tournament.teams
games = tournament.games

#pulls from games.txt
more_games = get_games('mens_games.txt', teams)
#more_games = get_games('womens_games.txt', teams)
games += more_games
teams = add_games_to_teams(teams, more_games)

#runs usau algorithm n times
#usually converges within a few thousand
n = 2000
for i in range(0, n):
    for game in games:
        if game.teamA_score[0].isdigit():
            if (game.teamA.rating > game.teamB.rating + 600 and int(game.teamA_score) > int(game.teamB_score) * 2 + 1):
                #print("blowout " + game.teamA.name + " vs. " + game.teamB.name)
                continue
            elif (game.teamB.rating > game.teamA.rating + 600 and int(game.teamB_score) > int(game.teamA_score) * 2 + 1):
                #print("blowout " + game.teamA.name + " vs. " + game.teamB.name)
                continue
            if (int(game.teamA_score) > int(game.teamB_score)):
                rating_diff = get_rating_differential(int(game.teamA_score), int(game.teamB_score))
                game.teamA.game_ratings.append((game.teamB.rating + rating_diff) * get_score_weight(int(game.teamA_score), int(game.teamB_score)))
                game.teamB.game_ratings.append((game.teamA.rating - rating_diff) * get_score_weight(int(game.teamA_score), int(game.teamB_score)))
            else:
                rating_diff = get_rating_differential(int(game.teamB_score), int(game.teamA_score))
                game.teamA.game_ratings.append((game.teamB.rating - rating_diff) * get_score_weight(int(game.teamB_score), int(game.teamA_score)))
                game.teamB.game_ratings.append((game.teamA.rating + rating_diff) * get_score_weight(int(game.teamB_score), int(game.teamA_score)))

    for team in teams:
        if len(team.game_ratings) > 0:
            team.rating = sum(team.game_ratings)/len(team.game_ratings)
            team.game_ratings = []

teams.sort()
i = 1
for team in teams:
    print(str(i) + ". " + team.name + " " + str(round(team.rating)))
    i += 1
