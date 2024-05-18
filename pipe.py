# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Gabriel Bispo
# 106326 Guilherme Filipe

import sys
import time
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
from sys import stdin


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Piece:

    """Representação interna de uma peça do PipeMania."""
    def __init__(self, value: str):
        self.value = value
        self.exits = []
        self.rotations = 3

    def rotate(self, clockwise: bool):
        """Roda a peça 90° no sentido dos ponteiros do relógio se
        'clockwise' for True, caso contrário, no sentido contrário."""
        # TODO
        pass
    
    def set_exits(self):
        pass

    def rotate180(self):
        pass

    def __str__(self):
        return self.value
    
class F_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        
    def set_exits(self):
        self.exits = [self.value[1]]
        
    def rotate(self, clockwise: bool):
        if clockwise:
            if self.value == "FC":
                self.value = "FD"
            elif self.value == "FD":
                self.value = "FB"
            elif self.value == "FB":
                self.value = "FE"
            elif self.value == "FE":
                self.value = "FC"
        else:
            if self.value == "FC":
                self.value = "FE"
            elif self.value == "FD":
                self.value = "FC"
            elif self.value == "FB":
                self.value = "FD"
            elif self.value == "FE":
                self.value = "FB"

        self.set_exits()

    def rotate180(self):
        if self.value == "FC":
                self.value = "FB"
        elif self.value == "FD":
                self.value = "FE"
        elif self.value == "FB":
                self.value = "FC"
        elif self.value == "FE":
                self.value = "FD"
        self.set_exits()
    
class B_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        
    def set_exits(self):
        if self.value[1] == "C":
            self.exits = ["E", "C", "D"]
        elif self.value[1] == "D":
            self.exits = ["C", "D", "B"]
        elif self.value[1] == "B":
            self.exits = ["E", "B", "D"]
        elif self.value[1] == "E":
            self.exits = ["C", "E", "B"]

    def rotate(self, clockwise: bool):
        if clockwise:
            if self.value == "BC":
                self.value = "BD"
            elif self.value == "BD":
                self.value = "BB"
            elif self.value == "BB":
                self.value = "BE"
            elif self.value == "BE":
                self.value = "BC"
        else:
            if self.value == "BC":
                self.value = "BE"
            elif self.value == "BD":
                self.value = "BC"
            elif self.value == "BB":
                self.value = "BD"
            elif self.value == "BE":
                self.value = "BB"
        
        self.set_exits()

    def rotate180(self):
        if self.value == "BC":
                self.value = "BB"
        elif self.value == "BD":
                self.value = "BE"
        elif self.value == "BB":
                self.value = "BC"
        elif self.value == "BE":
                self.value = "BD"
        self.set_exits()
        
class V_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        
    def set_exits(self):
        if self.value == "VC":
            self.exits = ["E", "C"]
        elif self.value == "VD":
            self.exits = ["C", "D"]
        elif self.value == "VB":
            self.exits = ["B", "D"]
        elif self.value == "VE":
            self.exits = ["E", "B"]

    def rotate(self, clockwise: bool):
        if clockwise:
            if self.value == "VC":
                self.value = "VD"
            elif self.value == "VD":
                self.value = "VB"
            elif self.value == "VB":
                self.value = "VE"
            elif self.value == "VE":
                self.value = "VC"
        else:
            if self.value == "VC":
                self.value = "VE"
            elif self.value == "VD":
                self.value = "VC"
            elif self.value == "VB":
                self.value = "VD"
            elif self.value == "VE":
                self.value = "VB"

        self.set_exits()

    def rotate180(self):
        if self.value == "VC":
                self.value = "VB"
        elif self.value == "VD":
                self.value = "VE"
        elif self.value == "VB":
                self.value = "VC"
        elif self.value == "VE":
                self.value = "VD"
        self.exits
    
class L_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        self.rotations = 1
        
    def set_exits(self):
        if self.value == "LH":
            self.exits = ["E", "D"]
        elif self.value == "LV":
            self.exits = ["C", "B"]
            
    def rotate(self):
        if self.value == "LH":
            self.value = "LV"
        elif self.value == "LV":
            self.value = "LH"
        self.set_exits()
    
    def rotate180(self):
        pass
            
        

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    board = []; # Game Board

    def get_value(self, row: int, col: int) -> Piece:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row >= len(self.board) or col < 0 or col >= len(self.board[0]):
            return None
        else:
            return self.board[row][col]
        
    #implementada por nós, podemos?
    def set_value(self, row: int, col: int, value: Piece):
        """Altera o valor na respetiva posição do tabuleiro."""
        self.board[row][col] = value
        
    def action(self, action: tuple) -> None:
        value = self.get_value(action[0], action[1])
        orientation = action[2]
        double = action[3]

        #action = (row, col, orientation, double)
        #orientation = True -> clockwise
        #orientation = False -> counter-clockwise
        
        #podemos usar match? (um switch para strings)
        if double == False:
            if value == "None":
                return
            elif isinstance(value, F_Piece):
                value.rotate(orientation)
                return
            elif(isinstance(value, B_Piece)):
                value.rotate(orientation)
                return
            elif(isinstance(value, V_Piece)):
                value.rotate(orientation)
                return
            elif(isinstance(value, L_Piece)):
                value.rotate()
                return
        
        if double ==True:
            value.rotate180()
            return
        return
        

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        v1 = self.get_value(row - 1, col)
        v2 = self.get_value(row + 1, col)
        return (v1, v2)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        v1 = self.get_value(row, col - 1)
        v2 = self.get_value(row, col + 1)
        return (v1, v2)

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        board = list()
        line = stdin.readline().split()
        while(line != []):
            new_line = list()
            for i in range(len(line)):
                if(line[i][0] == "F"):
                    v = F_Piece(line[i])
                elif(line[i][0] == "B"):
                    v = B_Piece(line[i])
                elif(line[i][0] == "V"):
                    v = V_Piece(line[i])
                elif(line[i][0] == "L"):
                    v = L_Piece(line[i])
                new_line.append(v)
            board.append(new_line)
            line = stdin.readline().split()
        
        new_board = Board()
        new_board.board = board
        return new_board
    
    def print(self):
        s = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                s += self.board[i][j].value + "\t"
            s += "\n"
        return s

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        
        self.initial = PipeManiaState(board)
        self.goal = None
        self.current = self.initial

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        dim = len(board.board)
        actions = []
        for row in range(dim):
            for column in range(dim):
                piece = board.get_value(row,column)
                if not piece.rotations <= 0:
                    print("Peça: ", row, column)
                    piece.rotations = piece.rotations - 3
                    print("Rotações restantes: ", piece.rotations)
                    actions.append((row, column, True, False))
                    actions.append((row, column, False, False))
                    actions.append((row, column, True, True)) #180º

                    return actions
        return actions
                    

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        
        board = list()
        
        for i in range(len(state.board.board)):
            new_line = list()
            for j in range(len(state.board.board[i])):
                k = state.board.get_value(i, j).value
                if(k[0] == "F"):
                    v = F_Piece(k)
                elif(k[0] == "B"):
                    v = B_Piece(k)
                elif(k[0] == "V"):
                    v = V_Piece(k)
                elif(k[0] == "L"):
                    v = L_Piece(k)
                v.rotations = state.board.board[i][j].rotations
                new_line.append(v)
            board.append(new_line)
        
        new_board = Board()
        new_board.board = board
        
        new_state = PipeManiaState(new_board)
        new_state.board.action(action)

        self.current = new_state
        return new_state
        

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        print("Estadoo: ", state.id)

        for i in range(len(state.board.board)):
            for j in range(len(state.board.board[i])):
                testing = state.board.get_value(i, j) #getvalue?
                for k in range(len(testing.exits)):
                    if(testing.exits[k] == "C"):
                        if(state.board.get_value(i - 1, j) == None):
                            return False
                        elif("B" not in state.board.get_value(i - 1, j).exits):
                            return False
                    elif(testing.exits[k] == "D"):
                        if(state.board.get_value(i, j + 1) == None):
                            return False
                        elif("E" not in state.board.get_value(i, j + 1).exits):
                            return False
                    elif(testing.exits[k] == "B"):
                        if(state.board.get_value(i + 1, j) == None):
                            return False
                        elif("C" not in state.board.get_value(i + 1, j).exits):
                            return False
                    elif(testing.exits[k] == "E"):
                        if(state.board.get_value(i, j - 1) == None):
                            return False
                        elif("D" not in state.board.get_value(i, j - 1).exits):
                            return False
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node =  depth_first_tree_search(problem)
    print("Is goal?", problem.goal_test(goal_node.state))
    print("State: ", goal_node.state.id)
    print("Solution:\n", goal_node.state.board.print(), sep="")
    
    
    pass
