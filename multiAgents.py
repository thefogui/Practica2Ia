# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        penalty = 10.0
        score = successorGameState.getScore()

        min_distance_ghost = None
        min_distance_food = None
        infinito = -10000000
        if action == 'Stop':
            return infinito
        elif successorGameState.isWin():
            return 1000000

        """
            Search for the position of the  most near ghost in the ghosts list
            and do the manhattan Distance with the position of the pacman with
            the near ghost
        """
        for ghost in newGhostStates:
            if ghost.getPosition() == tuple(list(newPos)):
                if ghost.scaredTimer == 0:
                    return infinito
            distance_ghost = manhattanDistance(newPos, ghost.getPosition())
            if min_distance_ghost == None:
                min_distance_ghost = distance_ghost
            else:
                if min_distance_ghost < distance_ghost:
                    min_distance_ghost = distance_ghost
        """
            Search the nearest food in the list of food and do the manhattanDistance
            with the pacman position.
        """
        for food in newFood.asList():
            distance_food = manhattanDistance(newPos, food)
            if min_distance_food == None:
                min_distance_food = distance_food
            else:
                if min_distance_food < distance_food:
                    min_distance_food = distance_food

        if score:
            if min_distance_ghost:
                score -= penalty / min_distance_ghost
            if min_distance_food:
                score += penalty / min_distance_food

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        #util.raiseNotDefined()

        def maxValue(gameState, agentIndex, depth):
            move = 'Stop'
            moves = gameState.getLegalActions(self.index)
            if depth >= self.depth or gameState.isWin() or not moves:
                return self.evaluationFunction(gameState), Directions.STOP
            best_value = -1000000
            for action in moves:
                succesor = gameState.generateSuccessor(self.index, action)
                alpha, __ = minValue(succesor, agentIndex + 1, depth)

                if alpha > best_value:
                    best_value = alpha
                    move = action
            return best_value, move

        def minValue(gameState, agentIndex, depth):
            move = 'Stop'
            moves = gameState.getLegalActions(agentIndex)
            if depth >= self.depth or gameState.isLose() or not moves:
                return self.evaluationFunction(gameState), Directions.STOP
            best_value = 1000000
            for action in moves:
                succesor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() -1:
                    beta, __ = maxValue(succesor, self.index, depth +1)
                else:
                    beta, __ = minValue(succesor, agentIndex + 1, depth)

                if beta < best_value:
                    best_value = beta
                    move = action
            return best_value, move
        return maxValue(gameState, self.index, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, agentIndex, depth, alpha_pruning, beta_pruning):
            move = 'Stop'
            moves = gameState.getLegalActions(self.index)
            if depth >= self.depth or gameState.isWin() or not moves:
                return self.evaluationFunction(gameState), Directions.STOP
            best_value = -100000
            for action in moves:
                succesor = gameState.generateSuccessor(self.index, action)
                alpha, __ = minValue(succesor, agentIndex + 1, depth, alpha_pruning, beta_pruning)

                if alpha > best_value:
                    best_value = alpha
                    move = action

                if best_value > beta_pruning:
                    return best_value, move

                alpha_pruning = max(alpha_pruning, best_value)
            return best_value, move

        def minValue(gameState, agentIndex, depth, alpha_pruning, beta_pruning):
            move = 'Stop'
            moves = gameState.getLegalActions(agentIndex)
            if depth >= self.depth or gameState.isLose() or not moves:
                return self.evaluationFunction(gameState), Directions.STOP
            best_value = 100000
            for action in moves:
                succesor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() -1:
                    beta, __ = maxValue(succesor, self.index, depth +1, alpha_pruning, beta_pruning)
                else:
                    beta, __ = minValue(succesor, agentIndex + 1, depth,alpha_pruning, beta_pruning)

                if beta < best_value:
                    best_value = beta
                    move = action

                if best_value < alpha_pruning:
                    return best_value, move

                beta_pruning = min(beta_pruning, best_value)
            return best_value, move
        return maxValue(gameState, self.index, 0, -1000000, 1000000)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, agentIndex, depth):
            move = 'Stop'
            moves = gameState.getLegalActions(self.index)
            if depth >= self.depth or gameState.isWin() or not moves:
                return self.evaluationFunction(gameState), Directions.STOP
            best_value = -1000000
            for action in moves:
                succesor = gameState.generateSuccessor(self.index, action)
                alpha, __ = minValue(succesor, agentIndex + 1, depth)

                if alpha > best_value:
                    best_value = alpha
                    move = action
            return best_value, move

        def minValue(gameState, agentIndex, depth):
            move = 'Stop'
            moves = gameState.getLegalActions(agentIndex)
            if depth >= self.depth or gameState.isLose() or not moves:
                return self.evaluationFunction(gameState), Directions.STOP
            best_value = 1000000
            for action in moves:
                succesor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() -1:
                    beta, __ = maxValue(succesor, self.index, depth +1)
                else:
                    beta, __ = minValue(succesor, agentIndex + 1, depth)

                if beta < best_value:
                    best_value = beta
                    move = action
            return best_value, move
        return maxValue(gameState, self.index, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
