class Team:
    def __init__(self, name, id, seed, pool=None):
        self.name = name
        self.id = id
        self.seed = seed
        self.pool = pool
        self.games = []
        self.rating = 1000
        self.game_ratings = []

    #allows sorting by seed or rating
    def __lt__(self, other):
        #return int(self.seed) < int(other.seed)
        return int(self.rating) > int(other.rating)

    def to_string(self):
        return ("Team: " + self.name + " (" + self.seed + ")")

    def add_game(self, game):
        self.games.append(game)

    def print_games(self):
        self.games.sort()
        print(self.to_string())
        for game in self.games:
            print(game.to_string())

    def isSameTeam(self,other):
        return self.id == other.id

class Game:
    def __init__(self, teamA, teamB, teamA_score, teamB_score, datetime, pool=None):
        self.teamA = teamA
        self.teamB = teamB
        self.teamA_score = teamA_score
        self.teamB_score = teamB_score
        self.datetime = datetime
        self.pool = pool

    #allows sorting by datetime
    def __lt__(self, other):
        return self.datetime < other.datetime

    def to_string(self):
        return ("Game: " + str(self.datetime.strftime("%b %d %H:%M")) + " | " + self.teamA.name + " vs. " + self.teamB.name + ", " + self.teamA_score + " - " + self.teamB_score)
