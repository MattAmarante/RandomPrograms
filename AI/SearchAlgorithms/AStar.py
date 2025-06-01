from abc import ABC,abstractmethod
import logging

class AStar(ABC):

    # Macro(s)
    VALORE = 0
    F = 1
    G = 2
    PADRE = 3

    def __init__(self,StartState,GoalState):
        self.StartState = StartState
        self.GoalState = GoalState

    def Solve(self) -> tuple: # Algoritmo A*
        """
        Effettua una ricerca A* sulla posizione iniziale indicata

        Parametri d'uscita:
        - Una tupla contenente (Risultato finale,f(n),g(n),Nodo Padre)
        """

        queue = []
        visited = set()
        CurrentStep = 0

        queue.append((self.StartState,self.CalculateHeuristic(self.StartState),0,None))

        while len(queue) != 0:
            index = self.SearchLowest(queue)
            CurrentNode = queue.pop(index)
            hashablePosition = tuple(map(tuple, CurrentNode[self.VALORE]))
            
            if hashablePosition in visited: continue
            visited.add(hashablePosition)
            
            h = self.CalculateHeuristic(CurrentNode[self.VALORE])

            print(f"Step n.{CurrentStep}, posizione attuale:")
            print(f"Valutazione della posizione: {h}")
            print(f"f(n) = {CurrentNode[self.F]}")
            print(f"Depth: {CurrentNode[self.G]}\n")

            if CurrentNode[self.VALORE] == self.GoalState:
                return CurrentNode

            NewNodes = self.ExpandNode(CurrentNode[self.VALORE])
            for Node in NewNodes:
                g = self.CalculateG(CurrentNode,Node)
                f = g + h
                queue.append((Node,f,g,CurrentNode))

            CurrentStep += 1

        return ("failure",)

    @abstractmethod
    def CalculateHeuristic(self,CurrentPosition) -> int:
        pass

    @abstractmethod
    def CalculateG(self,PreviousNode:tuple,CurrentNode:tuple) -> int:
        pass

    @abstractmethod
    def ExpandNode(self,Node) -> list:
        pass

    def SearchLowest(self,StateList:list[tuple]) -> int:
        """
        Cerca all'interno di una lista di tuple, quella con valore f(n) minore.
        La tupla contiene (VALORE,f(n),depth,Padre)

        Parametri in ingresso:
        - StateList: La lista contenente tutte le tuple

        Parametri in uscita:
        - indice della tupla con valore di f(n) minore
        """

        lowest = float("inf")
        LowestNodeIndex = -1
        i = 0

        while i < len(StateList):

            if StateList[i][self.F] < lowest:
                lowest = StateList[i][self.F]
                LowestNodeIndex = i

            i+=1

        return LowestNodeIndex
