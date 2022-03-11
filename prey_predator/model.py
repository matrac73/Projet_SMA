"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    grass = False
    grass_regrowth_time = 30
    sheep_gain_from_food = 4

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_sheep=100,
        initial_wolves=50,
        initial_sheep_energy=40,
        initial_wolves_energy=40,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        grass=False,
        starting_grass_prob=0.5,
        grass_regrowth_time=30,
        sheep_gain_from_food=4,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.initial_sheep_energy = initial_sheep_energy
        self.initial_wolves_energy = initial_wolves_energy
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.starting_grass_prob = starting_grass_prob
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
                "Grass Energy": lambda m:  m.schedule.get_fully_grown_grass()*self.sheep_gain_from_food,
            }
        )

        # Create sheep:
        # ... to be completed
        for i in range(self.initial_sheep):

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
                        
            a = Sheep(self.next_id(), (x, y), self,  moore=True, energy=self.initial_sheep_energy )
            self.schedule.add(a)

            
        # Create wolves
        # ... to be completed
        for i in range(self.initial_wolves):

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
                        
            a = Wolf(self.next_id(), (x, y), self,  moore=True, energy=self.initial_wolves_energy )
            self.schedule.add(a)

        # Create grass patches
        # ... to be completed
        if self.grass:
            for i in range(self.grid.width):
                for j in range(self.grid.height):
                    if self.random.random() < self.starting_grass_prob:
                        a = GrassPatch(self.next_id(), (i, j), self, fully_grown=True, countdown=0)
                    else:
                        a = GrassPatch(self.next_id(), (i, j), self, fully_grown=False, countdown=self.random.randint(0,self.grass_regrowth_time))
                    self.schedule.add(a)
                
        

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

        # ... to be completed

        # eat each other

        #for i in self.grid.width:
        #    for j in self.grid.height:
        #        cellmates = self.model.grid.get_cell_list_contents([(i,j)])
        #        for agent in cellmates:
        #            if isinstance(agent, Wolf):

        # eliminate the ones without energy
        for agent in self.schedule.agents:
            if isinstance(agent, Sheep) or isinstance(agent, Wolf):
                if agent.energy <= 0:
                    self.schedule.remove(agent)
                    self.grid.remove_agent(agent)
            

        # breed wolfs and sheeps

        for agent in self.schedule.agents:
            if isinstance(agent, Sheep):
                if self.random.random() < self.sheep_reproduce:
                    possible_pos = self.grid.get_neighborhood(agent.pos, agent.moore, True)
                    pos = self.random.choice(possible_pos)
                    energy_used = agent.energy // 2 
                    agent.energy -= energy_used        
                    a = Sheep(self.next_id(), pos, self,  moore=True, energy = energy_used )
                    
                    self.schedule.add(a)

            if isinstance(agent, Wolf):
                if self.random.random() < self.wolf_reproduce:
                    possible_pos = self.grid.get_neighborhood(agent.pos, agent.moore, True)
                    pos = self.random.choice(possible_pos)
                    energy_used = agent.energy // 2 
                    agent.energy -= energy_used
                    a = Wolf(self.next_id(), pos, self,  moore=True, energy=energy_used)
                    
                    self.schedule.add(a)
            if isinstance(agent, GrassPatch):
                if agent.countdown == 0:
                    agent.fully_grown = True

        for agent in self.schedule.agents:
            if isinstance(agent, Sheep):
                cellmates = self.grid.get_cell_list_contents([agent.pos])
                for cellmate in cellmates:
                    if isinstance(cellmate, GrassPatch):
                        if cellmate.fully_grown:
                            cellmate.fully_grown = False
                            cellmate.countdown = self.grass_regrowth_time
                            agent.energy += self.sheep_gain_from_food

        for agent in self.schedule.agents:
            if isinstance(agent, Wolf):
                cellmates = self.grid.get_cell_list_contents([agent.pos])
                for cellmate in cellmates:
                    if isinstance(cellmate, Sheep):    
                        agent.energy += cellmate.energy # we are not using wolf gain from food
                        self.schedule.remove(cellmate)
                        self.grid.remove_agent(cellmate)

        
                
            if isinstance(agent, Wolf):
                if self.random.random() < self.wolf_reproduce:
                    possible_pos = self.grid.get_neighborhood(agent.pos, agent.moore, True)
                    pos = self.random.choice(possible_pos)
                    energy_used = agent.energy // 2 
                    agent.energy -= energy_used
                    a = Wolf(self.next_id(), pos, self,  moore=True, energy=energy_used)
                    
                    self.schedule.add(a)
                    
    def run_model(self, step_count=200):

        # ... to be completed
        for _ in range(step_count):
            self.step()
