from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)



class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):

        def alphaBetaPruning(gameState, depth, agentID, alpha, beta):
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            if agentID == 0:
                v = float('-inf')
                if len(gameState.getLegalActions()) == 0:
                    return self.evaluationFunction(gameState)
                ac = Directions.STOP
                for a in gameState.getLegalActions():
                    s = alphaBetaPruning(gameState.generateSuccessor(0, a), depth, 1, alpha, beta)
                    if s > v:
                        v = s
                        ac = a
                    if v > beta:
                        return v
                    alpha = max(alpha, v)
                if depth == 0:
                    return ac
                else:
                    return v
            else:
                v = float('inf')
                if len(gameState.getLegalActions()) == 0:
                    return self.evaluationFunction(gameState)
                nextAgent = agentID + 1
                if nextAgent == gameState.getNumAgents():
                    nextAgent = 0
                for a in gameState.getLegalActions(agentID):
                    if nextAgent == 0:
                        s = alphaBetaPruning(gameState.generateSuccessor(agentID, a), depth + 1, 0, alpha, beta)
                    else:
                        s = alphaBetaPruning(gameState.generateSuccessor(agentID, a), depth, nextAgent, alpha, beta)
                    v = min(s, v)
                    if v < alpha:
                        return v
                    beta = min(beta, v)
                return v

        return alphaBetaPruning(gameState, 0, 0, float('-inf'), float('inf'))



def betterEvaluationFunction(currentGameState):

    def distanceToNearestFood():
        dis = float('inf')
        for food in foods:
            manDis = manhattanDistance(pacmanPos, food)
            if manDis < dis:
                dis = manDis
        return dis

    def distanceToNearestGhost():
        dis1 = float('inf')
        dis2 = float('inf')
        timer = 0
        i = 0
        for ghostState in ghostStates:
            manDis = manhattanDistance(ghostState.getPosition(), pacmanPos)
            if scaredTimes[i] != 0:
                if manDis < dis2:
                    dis2 = manDis
                    timer = scaredTimes[i]
            else:
                if manDis < dis1:
                    dis1 = manDis
            i += 1

        if dis2 != float('inf'):
            return (1 / dis2) + timer

        return dis1

    if currentGameState.isWin():
        return 99999
    if currentGameState.isLose():
        return -99999

    ghostStates = currentGameState.getGhostStates()
    pacmanPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    numOfFoods = len(foods)
    numOfCapsules = len(currentGameState.getCapsules())
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score = currentGameState.getScore() + (-1.5) * distanceToNearestFood() + 2 * distanceToNearestGhost() + (
        -4) * numOfFoods + (-20) * numOfCapsules
    return score


better = betterEvaluationFunction
