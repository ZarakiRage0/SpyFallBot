import json
import time

from player import Player
import random
from datetime import datetime


class Game:
    def __init__(self, json_file_name):
        with open(json_file_name) as json_file:
            self.data = json.load(json_file)["locations"]
        self.maxPlayers = 8
        self.location = None
        self.players = []
        self.startTime = None
        self.gameTime = 600
        self.spy = None
        self.gameIsLive = False

    def set_players(self, members):
        self.players = []
        for member in members:
            player = Player(member)
            self.players.append(player)

    def assign_roles(self):
        n = len(self.players)
        locations_len = len(self.data)
        self.location = self.data[random.randint(0, locations_len - 1)]
        roles = self.location["roles"]
        roles_numbers = random.sample(range(0, self.maxPlayers - 1), n-1)
        spy = 0
        if n != 1:
            spy = random.randint(0, n - 1)
            roles_numbers.insert(spy-1, -1)
        for i in range(0, n):
            if i != spy:
                role = roles[roles_numbers[i]]
            else:
                role = "Spy"
                self.spy = self.players[i]
            self.players[i].set_role(role)

    def get_spy(self):
        return self.spy

    def set_startTime(self, startTime):
        self.startTime = startTime

    def set_gameTime(self, gameTime):
        self.gameTime = gameTime

    def play(self, members):
        self.set_players(members)
        self.assign_roles()
        self.set_startTime(datetime.now())
        self.gameIsLive = True

    def show(self):
        for player in self.players:
            print(player.role, player.user.name)
        print(self.startTime)

    def add_location(self, location):
        self.data.append(location)

    def display(self):
        for e in self.data:
            print(e["title"], e["roles"])

    def countdown(self):
        countdown = self.gameTime
        while countdown != 0:
            time.sleep(1)
            countdown -= 1

    def gameEnd(self):
        self.gameIsLive = False
