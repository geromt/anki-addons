import json
import os.path
import random

from aqt import gui_hooks, mw
from aqt.utils import askUserDialog, showInfo


class CamelGame:
    def __init__(self, savefile):
        self.savefile = savefile
        self.config = mw.addonManager.getConfig(__name__)
        self.traveled_distance: int
        self.natives: int
        self.canteen: int
        self.thirst: int

        if os.path.exists(self.savefile):
            self._load_save()
        else:
            self.load_init()

        self.turns = 0
        self.alive = True

    def _load_save(self):
        with open(self.savefile, "r") as save:
            data = json.load(save)
            self._load(data)

    def load_init(self):
        self._load(self.config["init_vals"])

    def _load(self, data):
        self.traveled_distance = data["traveled_distance"]
        self.natives = data["natives"]
        self.canteen = data["canteen"]
        self.thirst = data["thirst"]

    def drink(self):
        if self.canteen > 0:
            self.canteen -= 1
            self.thirst = 0
            return True
        return False

    def walk(self, amount):
        self.traveled_distance += amount
        self.natives += random.randint(1, 3)
        self.thirst += random.randint(0, 1)

    def run(self, reviewer, card, ease):
        if not self.alive:
            return

        self.walk(ease)
        if self.turns % self.config["status_check"] == 0:
            bd = askUserDialog((f"Traveled Distance: {self.traveled_distance}\n"
                                f"Distance from natives: {self.traveled_distance-self.natives}\n"
                                f"Drinks in canteen: {self.canteen}\n"),
                               ["Drink water", "Continue"], title="CamelGame")

            response = bd.run()
            if response == "Drink water":
                self.drink()

        if self.natives >= self.traveled_distance:
            showInfo("You've been captured by the natives. Game Over")
            self.alive = False
        if self.thirst >= self.config["thirst_to_die"]:
            showInfo("You've died from dehydration: Game Over")
            self.alive = False

        self.turns += 1


camel_game = CamelGame("savefile.json")
gui_hooks.reviewer_did_answer_card.append(camel_game.run)
