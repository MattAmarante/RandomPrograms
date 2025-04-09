from SearchAlgorithms.AStar import AStar
import random
from copy import deepcopy

class NPuzzle(AStar):

    def __init__(self,StartState:list[list[int]] = [],GoalState:list[list[int]] = [],MatrixDim:int = 3,BlankSpace = 0):
        """
        Inizializza i parametri per la dimensione della matrince,
        la posizione iniziale e finale.

        Il parametro StartState è opzionale, e se lasciato vuoto viene
        inizializzato ad un valore casuale.
        Il parametro GoalState è opzionale, e se lasciato vuoto viene
        inizializzato alla soluzione standard per quella dimensione.
        """

        self.MatrixDim = MatrixDim
        self.BlankSpace = BlankSpace
        super().__init__(self.GenerateInitialState(StartState),self.GenerateGoalMatrix(GoalState))

    def CalculateHeuristic(self,CurrentState:list[list[int]]) -> int:
        """
        Utilizza la posizione di Manhattan per calcolare l'euristica del
        problema
        """

        GridCharacter = list(range(1,self.MatrixDim**2))
        ManhattanDist = 0

        for num in GridCharacter:
            PosFinale_x,PosFinale_y = self.GetPositionFromState(self.GoalState,num)
            PosIniziale_x,PosIniziale_y = self.GetPositionFromState(CurrentState,num)
            
            ManhattanDist += abs(PosFinale_x-PosIniziale_x) + abs(PosFinale_y-PosIniziale_y)
        
        return ManhattanDist

    def CalculateCostToPath(self,PreviousNode:tuple,CurrentNode:tuple) -> int:
        """
        Il costo per un passo è sempre unitario
        """
        return PreviousNode[AStar.G]+1
    
    def ExpandNode(self,CurrentState:list[list[int]]) -> list:
        """
        Genera una lista contenente le posizioni raggiungibili dallo stato iniziale;
        quindi, la funzione capirà quali azioni sono legali e aggiungerà alla matrice la
        posizione che si ottiene dopo aver applicato quella determinata azione.
        
        Parametri in ingresso:
        - CurrentState: una matrice contenente uno stato iniziale.
        
        Parametri in uscita:
        - Una lista di matrici, contenenti le posizioni finali dopo aver applicato
        un azione
        """
        
        Queue = []
        IndexRow, IndexCol = self.GetPositionFromState(CurrentState,self.BlankSpace)

        if IndexCol+1 < self.MatrixDim:
            MoveRight = deepcopy(CurrentState)

            MoveRight[IndexRow][IndexCol] = MoveRight[IndexRow][IndexCol+1]
            MoveRight[IndexRow][IndexCol+1] = self.BlankSpace
            Queue.append(MoveRight)

        if IndexCol-1 >= 0:
            MoveLeft = deepcopy(CurrentState)

            MoveLeft[IndexRow][IndexCol] = MoveLeft[IndexRow][IndexCol-1]
            MoveLeft[IndexRow][IndexCol-1] = self.BlankSpace
            Queue.append(MoveLeft)

        if IndexRow+1 < self.MatrixDim:
            MoveUp = deepcopy(CurrentState)

            MoveUp[IndexRow][IndexCol] = MoveUp[IndexRow+1][IndexCol]
            MoveUp[IndexRow+1][IndexCol] = self.BlankSpace
            Queue.append(MoveUp)
        
        if IndexRow-1 >= 0:
            MoveDown = deepcopy(CurrentState)

            MoveDown[IndexRow][IndexCol] = MoveDown[IndexRow-1][IndexCol]
            MoveDown[IndexRow-1][IndexCol] = self.BlankSpace
            Queue.append(MoveDown)
        
        return Queue

    def GetPositionFromState(self,state:list[list[int]],num:int) -> tuple:
        """
        Cerca dalla matrice un valore numerico, ritornando l'indice di riga
        e colonna dove è stato trovato quel valore.
        
        Parametri in ingresso:
        - State: la matrice contenente lo stato corrente.
        - Num: il numero di cui voglio cercare la posizione
        
        Parametri in uscita:
        - Una tupla contenente l'indice di riga e colonna (riga,colonna)
        """

        IndexRow = IndexCol = -1
        i = j = 0
        FoundNum = False

        while i < self.MatrixDim and not FoundNum:
            while j < self.MatrixDim and not FoundNum:
                if state[i][j] == num:
                    IndexRow = i
                    IndexCol = j
                    FoundNum = True

                j+=1
            j=0
            i+=1
        
        return IndexRow,IndexCol

    def GenerateGoalMatrix(self,State:list[list[int]] = []) -> list[list[int]]:
        """
        Genera una posizione finale per il puzzle; la funzione permette
        di specificare una matrice specifica come posizione finale, e nel caso
        in cui non venga specificata la genera automaticamente seguendo la forma
        generica di una soluzione del 8Puzzle.
        
        Parametri in ingresso:
        - State (opzionale): la matrice che descrive la posizione finale del problema.
        """

        if State != []:
            return State
        
        OrderedPosition = list(range(1,self.MatrixDim**2)) + [self.BlankSpace]
        GoalMatrix = []

        for i in range(self.MatrixDim):
            NewRow = []

            for j in range(self.MatrixDim):
                NewRow.append(OrderedPosition[(i*self.MatrixDim)+j])
            
            GoalMatrix.append(NewRow)

        return GoalMatrix

    def RandomizeState(self) -> list[list[int]]:
        """Genera una matrice quadrata casuale"""
        PossibleValues = list(range(1,self.MatrixDim**2)) + [self.BlankSpace]
        RandomizedList = []

        for _ in range(self.MatrixDim):
            NewRow = []

            for _ in range(self.MatrixDim):
                RandomElementPosition = random.randint(0,len(PossibleValues)-1)
                NewRow.append(PossibleValues.pop(RandomElementPosition))
            
            RandomizedList.append(NewRow)
        
        return RandomizedList


    def IsSolvable(self,state:list[list[int]]) -> bool:
        flat = [cell for row in state for cell in row if cell != 0]
            
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] > flat[j]:
                    inversions += 1
        
        return inversions % 2 == 0

    def GenerateInitialState(self,State:list[list[int]] = []) -> list[list[int]]:
        """
        Genera lo stato iniziale per il problema;
        Se viene specificata la matrice, lo stato iniziale verrà impostato a quella matrice,
        altrimenti ne verrà generata una randomicamente.
        
        Parametri in ingresso:
        - State (opzionale): lo stato inizale del problema
        """

        if State != []:
            return State
        
        StartState = self.RandomizeState()
        while not self.IsSolvable(StartState):
            StartState = self.RandomizeState()

        return StartState

    def PrintPosition(self,state:list[list[int]]) -> None:
        """
        Stampa lo stato attuale
        
        Parametri in ingresso:
        - State: la matrice che rappresenta lo stato corrente
        """

        for i in range(self.MatrixDim): 
            for j in range(self.MatrixDim): 
                print(f" {state[i][j]} ",end="")
            print("")
    
    def PrintPath(self,Node:tuple) -> None:
        """
        Stampa tutti i valori a partire dal nodo iniziale, fino a quello finale.
        
        Parametri in ingresso:
        - Node: una tupla che contiene (Matrice,f(n),depth,Padre)
        """
        
        if Node[AStar.PADRE] == None:
            print(f"\nStep n.{Node[AStar.G]}:")
            self.PrintPosition(Node[AStar.VALORE])
            return 

        self.PrintPath(Node[AStar.PADRE])
        print(f"\nStep n.{Node[AStar.G]}:")
        self.PrintPosition(Node[AStar.VALORE])

if __name__ == "__main__":
    Game = NPuzzle()
    Solution = Game.AStar()
    Game.PrintPath(Solution)