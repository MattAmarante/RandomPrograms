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

    def AStar(self):
        """
        Effettua una ricerca A* sulla posizione iniziale indicata
        
        Parametri d'uscita:
        - Una tupla contenente (Risultato finale,f(n),g(n),Nodo Padre)
        """

        queue = []
        visited = []
        CurrentStep = 0

        queue.append((self.StartState,self.CalculateHeuristic(self.StartState),0,None))

        while len(queue) != 0:
            index = self.SearchLowest(queue)
            CurrentNode = queue.pop(index)

            if CurrentNode[self.VALORE] in visited: continue
            visited.append(CurrentNode[self.VALORE])

            logging.debug(f"Step n.{CurrentStep}, posizione attuale:")
            logging.debug(f"Valutazione della posizione: {self.CalculateHeuristic(CurrentNode[self.VALORE])}")
            logging.debug(f"f(n) = {CurrentNode[self.F]}")
            logging.debug(f"Depth: {CurrentNode[self.G]}\n")

            if CurrentNode[self.VALORE] == self.GoalState:
                return CurrentNode
            
            NewNodes = self.ExpandNode(CurrentNode[self.VALORE])
            for Node in NewNodes:
                g = self.CalculateCostToPath(CurrentNode,Node)
                f = g + self.CalculateHeuristic(Node)
                queue.append((Node,f,g,CurrentNode))
            
            CurrentStep += 1

    @abstractmethod
    def CalculateHeuristic(self,CurrentPosition):
        pass

    @abstractmethod
    def CalculateCostToPath(self,PreviousNode,CurrentNode):
        pass

    @abstractmethod
    def ExpandNode(self,Node):
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