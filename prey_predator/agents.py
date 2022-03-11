from itertools import count
from tkinter import S
from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        
    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        self.eat_grass()
        self.model.breed(self)
        
        if self.model.grass:
            self.energy -= 1        
            if self.energy <= 0:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)

    def eat_grass(self):
        """the sheep_agent ask the model to eat grass"""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if isinstance(cellmate, GrassPatch):
                self.model.eat_grass(self, cellmate)

class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.eat_sheep()
        self.model.breed(self)
        self.energy -= 1
        if self.energy <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


    def eat_sheep(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for cellmate in cellmates:
            if isinstance(cellmate, Sheep):
                self.model.eat_sheep(self, cellmate)

class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
            growth_time
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.model.grid.place_agent(self, self.pos)
        self.fully_grown = fully_grown
        self.countdown = countdown
        
    def step(self):
        if self.countdown > 0:
            self.countdown -= 1
        if self.countdown == 0:
            self.fully_grown = True
