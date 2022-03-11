from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "DarkGray",
                 "r": 0.5}
        # ... to be completed

    elif type(agent) is Wolf:
        portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "Red",
                 "r": 0.5}
        # ... to be completed

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "darkgreen",
                    "w": 1.0,
                    "h": 1.0}
        else:
            portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "lightgreen",
                    "w": 1.0,
                    "h": 1.0}
        # ... to be completed

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)
chart_energy_element = ChartModule(
    [{"Label": "Grass Energy", "Color":"darkGreen"}]
)


model_params = {
    "grass": UserSettableParameter("checkbox", "grass", value=True),
    "starting_grass_prob":UserSettableParameter("slider", "starting_grass_prob",value=0.3, min_value=0.1, max_value=1.0, step=0.05),
    "initial_sheep" :UserSettableParameter("slider", "initial_sheep", value=40,  min_value=1, max_value=100, step=1),
    "initial_wolves" :UserSettableParameter("slider", "initial_wolves", value=20,  min_value=1, max_value=100, step=1),
    "initial_sheep_energy" :UserSettableParameter("slider", "initial_sheep_energy", value=30,  min_value=1, max_value=100, step=1),
    "initial_wolves_energy" :UserSettableParameter("slider", "initial_wolves_energy", value=30,  min_value=1, max_value=100, step=1),
    "sheep_reproduce" :UserSettableParameter("slider", "sheep_reproduce",value=0.15, min_value=0.00, max_value=0.2, step=0.01),
    "wolf_reproduce" :UserSettableParameter("slider", "wolf_reproduce", value=0.05,  min_value=0.00, max_value=0.1, step=0.01),
    "wolf_gain_from_food" :UserSettableParameter("slider", "wolf_gain_from_food", value=10,  min_value=1, max_value=100, step=1),
    "grass_regrowth_time" :UserSettableParameter("slider", "grass_regrowth_time", value=40,  min_value=1, max_value=100, step=1),
    "sheep_gain_from_food" :UserSettableParameter("slider", "sheep_gain_from_food", value=12,  min_value=1, max_value=100, step=1),
}

server = ModularServer(
    WolfSheep, [canvas_element, chart_element, chart_energy_element], "Prey Predator Model", model_params
)
server.port = 8524
