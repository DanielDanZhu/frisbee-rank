class Tournament:
    def __init__(self, name, teams, games, datetime, division):
        self.name = name
        self.teams = teams
        self.games = games
        self.datetime = datetime
        self.division = division

    def __it__(self,other):
        return self.datetime < other.datetime

    def to_string(self):
        s = ""
        for game in self.games:
            s += game.to_string + "\n"