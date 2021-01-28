# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import collections
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    visited = set()

    stack = util.Stack()
    stack.push((problem.getStartState(), []))

    while not stack.isEmpty():
        top = stack.pop()

        if problem.isGoalState(top[0]):
            return top[1]

        if top[0] not in visited:
            visited.add(top[0])
            for s in problem.getSuccessors(top[0]):
                if s[0] not in visited:
                    stack.push((s[0], top[1] + [s[1]]))

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visited = set()

    queue = util.Queue()
    queue.push((problem.getStartState(), []))

    while not queue.isEmpty():
        front = queue.pop()

        if problem.isGoalState(front[0]):
            return front[1]

        if front[0] not in visited:
            visited.add(front[0])
            for s in problem.getSuccessors(front[0]):
                if s[0] not in visited:
                    queue.push((s[0], front[1] + [s[1]]))

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    visited = set()

    pqueue = util.PriorityQueue()
    pqueue.push(((problem.getStartState(), [], 0)), 0)

    while not pqueue.isEmpty():
        top = pqueue.pop()

        if problem.isGoalState(top[0]):
            return top[1]

        if top[0] not in visited:
            visited.add(top[0])
            for s in problem.getSuccessors(top[0]):
                if s[0] not in visited:
                    distance = top[2] + s[2]
                    pqueue.update((s[0], top[1] + [s[1]], distance), distance)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    predecessor = dict()
    distance = collections.defaultdict(lambda: float('inf'))

    start = (problem.getStartState(), None, 0)
    goal = None
    distance[start[0]] = 0

    pqueue = util.PriorityQueue()
    pqueue.push(start, distance[start])
    predecessor[start] = None

    while not pqueue.isEmpty():
        top = pqueue.pop()

        if problem.isGoalState(top[0]):
            goal = top
            break

        successors = problem.getSuccessors(top[0])
        for s in successors:
            g = distance[top[0]] + top[2]
            h = heuristic(top[0], problem)
            if distance[s[0]] > g + h:
                distance[s[0]] = g + h
                predecessor[s] = top
                pqueue.push(s, distance[s[0]])

    path = []
    while goal is not start:
        path.append(goal[1])
        goal = predecessor[goal]

    return path[::-1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
