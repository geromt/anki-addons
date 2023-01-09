import random

from aqt import gui_hooks
from aqt.utils import askUserDialog, showInfo


class CamelGame:
    def __init__(self):
        self.distance = 0
        self.natives = -20
        self.canteen = 3
        self.tiredness = 0
        self.thirst = 0
        self.turns = 0
        self.alive = True

    def drink(self):
        if self.canteen > 0:
            self.canteen -= 1
            self.thirst = 0
            return True
        return False

    def walk(self, amount):
        self.distance += amount
        self.natives += random.randint(1, 4)
        self.thirst += random.randint(0, 2)

    def run(self, reviewer, card, ease):
        if not self.alive:
            return

        self.walk(ease)
        if self.turns % 10 == 0:
            bd = askUserDialog(f"Traveled Distance: {self.distance}\nDistance from natives: {self.distance-self.natives}\nDrinks in canteen: {self.canteen}\n",
                               ["Drink water", "Continue"], title="CamelGame")
            response = bd.run()
            if response == "Drink water":
                self.drink()

        if self.natives >= self.distance:
            showInfo("You've been captured by the natives. Game Over")
            self.alive = False
        if self.thirst >= 10:
            showInfo("You've died from dehydration: Game Over")
            self.alive = False

        self.turns += 1


camel_game = CamelGame()
gui_hooks.reviewer_did_answer_card.append(camel_game.run)
