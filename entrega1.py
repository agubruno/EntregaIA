from simpleai.search import SearchProblem, hill_climbing, hill_climbing_random_restarts, beam, simulated_annealing
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, \
    uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
import math
import random


tamañoMapa = 5
personas1 = ((2, 1), (3, 4), (4, 2))
posicionRobot = (0, 0)
hielosRotos = ()
state = (posicionRobot, hielosRotos, personas1)


class RescateSobreHielo(SearchProblem):

    def is_goal(self, state):
        posicionRobot, hielosRotos, personas = state
        if len(personas) == 0 and self.hay_orilla(posicionRobot):
            return True
        else:
            return False

    def hay_orilla (self, posicion):
        x, y = posicion
        if x == 0 or x == tamañoMapa or y == 0 or y == tamañoMapa:
            return True
        else:
            return False

    def actions(self, state):
        available_actions = []

        posicionRobot, hielosRotos, personas = state
        x, y = posicionRobot

        if x>0 and ((x-1,y) not in hielosRotos):
            available_actions.append((x-1,y))

        if x<tamañoMapa and ((x+1,y) not in hielosRotos):
            available_actions.append((x+1,y))

        if y > 0 and ((x, y-1) not in hielosRotos):
            available_actions.append((x, y-1))

        if y < tamañoMapa and ((x, y+1) not in hielosRotos):
            available_actions.append((x, y+1))

        return  available_actions

    def result(self, state, action):
        posicionRobot, hielosRotos, personas = state

        personas = list(personas)
        hielosRotos = list(hielosRotos)

        posicionRobot = action

        if posicionRobot in personas:
            personas.remove(posicionRobot)

        if not self.hay_orilla(posicionRobot):
            hielosRotos.append(posicionRobot)

        state = (tuple(posicionRobot), tuple(hielosRotos), tuple(personas))

        return state

    def cost(self, state1, action, state2):
        return 1


    def heuristic(self, state):
        posicionRobot, hielosRotos, personas = state
        sumaMasAlta = 0
        for p in personas:
            if p[0] < (tamañoMapa - p[0]):
                distanciaFila = p[0]
            else:
                distanciaFila = tamañoMapa - p[0]
            if p[1] < (tamañoMapa - p[1]):
                distanciaCol = p[1]
            else:
                distanciaCol = tamañoMapa - p[1]

            if distanciaFila < distanciaCol:
                distanciaMasCortaOrilla = distanciaFila
            else:
                distanciaMasCortaOrilla = distanciaCol

            DistanciaRobotPersonaOrilla = distanciaMasCortaOrilla + self.manhattanRobotPersona(p, state)

            if DistanciaRobotPersonaOrilla > sumaMasAlta:
                sumaMasAlta = DistanciaRobotPersonaOrilla

        return sumaMasAlta

           
    def manhattanRobotPersona(self,persona,state):
        posicionRobot, hielosRotos, personas = state
        manhattan = abs(persona[0]-posicionRobot[0])+abs(persona[1]-posicionRobot[1])
        return manhattan


def resolver(metodo_busqueda, posiciones_personas):

    state = (posicionRobot, hielosRotos, posiciones_personas)

    if metodo_busqueda == 'astar':
        visor=BaseViewer()
        result = astar(RescateSobreHielo(state),graph_search=True, viewer=visor)

    elif metodo_busqueda =='breadth_first':
        visor=BaseViewer()
        result = breadth_first(RescateSobreHielo(state),graph_search=True, viewer=visor)

    elif metodo_busqueda =='depth_first':
        visor=BaseViewer()
        result = depth_first(RescateSobreHielo(state),graph_search=True,viewer=visor)
        print(visor.stats)

    elif metodo_busqueda =='greedy':
        visor=BaseViewer()
        result = greedy(RescateSobreHielo(state),graph_search=True,viewer=visor)
        print(visor.stats)

    return result


"""
problem = RescateSobreHielo(state)
result = astar(problem)

posicionRobot, hielosRotos, personas = result.state


print("posicion Robot",posicionRobot)
print("hielos rotos",hielosRotos)
print("personas",personas)

print(result.state)
print(result.path())
"""
