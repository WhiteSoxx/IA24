# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Gabriel Bispo
# 106326 Guilherme Filipe

import sys
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

TOP_OPENING = ["FC", "BC", "BE", "BD", "VC", "VD", "LV"]
LEFT_OPENING = ["FE", "BC", "BB", "BE", "VC", "VE", "LH"]
RIGHT_OPENING = ["FD", "BC", "BB", "BD", "VB", "VD", "LH"]
BOT_OPENING = ["FB", "BB", "BE", "BD", "VB", "VE", "LV"]
#Indexs: 0 -> Peças de fecho; 1-3 -> biforcação; 4-5 - > curva, 6 -> linha

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
    possible_positions = []

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

    def transform(self, new_value):
        pass

    def __str__(self):
        return self.value
    
class F_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        self.possible_positions = ["FC", "FD", "FB", "FE"]
        
    def set_exits(self):
        self.exits = [self.value[1]]
        
    #mudar
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
        
    def transform(self, new_value):
        self.value = new_value
        self.set_exits()
    
class B_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        self.possible_positions = ["BC", "BD", "BB", "BE"]
        
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
        
    def transform(self, new_value):
        self.value = new_value
        self.set_exits()
        
class V_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        self.possible_positions = ["VC", "VD", "VB", "VE"]
        
    def set_exits(self):
        if self.value == "VC":
            self.exits = ["E", "C"]
        elif self.value == "VD":
            self.exits = ["C", "D"]
        elif self.value == "VB":
            self.exits = ["B", "D"]
        elif self.value == "VE":
            self.exits = ["E", "B"]

    
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
        
    def transform(self, new_value):
        #if len(self.possible_positions) > 0:
            #self.possible_positions.remove(new_value)
        self.value = new_value
        self.set_exits()

    
class L_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        self.rotations = 1
        self.possible_positions = ["LH", "LV"]
        
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
    
    def transform(self, new_value):
        self.value = new_value
        self.set_exits()

            
        
class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    board =  []

    def __init__(self):
        board = list()

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
    
        #action = (row, col)
        if value == None:
            return
        else:
            value.transform(action[2])
            
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
        dim = len(self.board)
        for i in range(dim):
            for j in range(dim):
                s += self.board[i][j].value
                if j <dim-1:
                    s+= '\t'
            if i<dim-1:
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
        
    def border_pieces(self, board: Board):
        limit = len(board.board)
        for i in range(limit):
            for j in range(limit):
                #canto
                border_piece = board.get_value(i, j)
                if i == 0 and j == 0:
                    if isinstance(border_piece, F_Piece): #FD or FB
                        border_piece.possible_positions = ["FB", "FD"]
                    elif isinstance(border_piece, V_Piece):
                        border_piece.transform("VB")
                        border_piece.possible_positions.clear()
                
                elif i == 0 and j == limit - 1:
                    if isinstance(border_piece, F_Piece):
                        border_piece.possible_positions = ["FE", "FB"]
                    elif isinstance(border_piece, V_Piece):
                        border_piece.transform("VE")
                        border_piece.possible_positions.clear()
                
                elif i == limit - 1 and j == 0:
                    if isinstance(border_piece, F_Piece):
                        border_piece.possible_positions = ["FD", "FC"]
                    elif isinstance(border_piece, V_Piece):
                        border_piece.transform("VD")
                        border_piece.possible_positions.clear()
                    
                elif i == limit - 1 and j == limit - 1:
                    if isinstance(border_piece, F_Piece):
                        border_piece.possible_positions = ["FE", "FC"]
                    elif isinstance(border_piece, V_Piece):
                        border_piece.transform("VC")
                        border_piece.possible_positions.clear()
                
                #bordas  
                elif i == 0: # borda superior
                    if isinstance(border_piece, L_Piece):
                        border_piece.possible_positions = ["LH"]
                        border_piece.transform("LH")
                        border_piece.possible_positions.clear()
                    elif isinstance(border_piece, B_Piece):
                        border_piece.possible_positions = ["BB"]
                        border_piece.transform("BB")
                        border_piece.possible_positions.clear()
                    
                    elif isinstance(border_piece, V_Piece):
                        border_piece.possible_positions = ["VB", "VE"]
                    elif isinstance(border_piece, F_Piece):
                        border_piece.possible_positions = ["FB", "FE", "FD"]

                
                elif j == 0: #borda esquerda
                    if isinstance(border_piece, L_Piece):
                        border_piece.transform("LV")
                        border_piece.possible_positions.clear()
                    elif isinstance(border_piece, B_Piece):
                        border_piece.transform("BD")
                        border_piece.possible_positions.clear()

                    elif isinstance(border_piece, V_Piece):
                        border_piece.possible_positions = ["VB", "VD"]
                    elif isinstance(border_piece, F_Piece):
                        border_piece.possible_positions = ["FC", "FB", "FD"]
                
                elif i == limit - 1: #borda inferior
                    if isinstance(border_piece, L_Piece):
                        border_piece.transform("LH")
                        border_piece.possible_positions.clear()
                    elif isinstance(border_piece, B_Piece):
                        border_piece.transform("BC")
                        border_piece.possible_positions.clear()
                
                    elif isinstance(border_piece, V_Piece):
                        border_piece.possible_positions = ["VC", "VD"]
                    elif isinstance(border_piece, F_Piece):
                        border_piece.possible_positions = ["FC", "FE", "FD"]
                        
                elif j == limit - 1: #borda direita
                    if isinstance(border_piece, L_Piece):
                        border_piece.transform("LV")
                        border_piece.possible_positions.clear()
                    elif isinstance(border_piece, B_Piece):
                        border_piece.transform("BE")
                        border_piece.possible_positions.clear()
                    elif isinstance(border_piece, V_Piece):
                        border_piece.possible_positions = ["VC", "VE"]
                    elif isinstance(border_piece, F_Piece):
                        border_piece.possible_positions = ["FC", "FB", "FE"]
                    

    def fools_errand(self, board: Board, row: int, col: int):
        """Verifica se existe alguma fuga entre as peças próximas e as posições
        possíveis da atual."""
        
        piece = board.get_value(row, col)
        top_piece = board.get_value(row - 1, col)
        left_piece = board.get_value(row, col - 1)
        
        leaking = False
        
        #criar uma peça hipotética para verificar exits mais depressa?
        #pode demorar mais tempo e memória, mesmo com garbage collecting

        for i in piece.possible_positions[:]:
            
            if top_piece != None:
                if "B" in top_piece.exits:
                    if i not in TOP_OPENING:
                        leaking = True
                else:
                    if i in TOP_OPENING:
                        leaking = True

            if left_piece != None:
                if "D" in left_piece.exits:
                    if i not in LEFT_OPENING:
                        leaking = True
                else:
                    if i in LEFT_OPENING:
                        leaking = True
                
            if leaking == True:
                piece.possible_positions.remove(i)
                leaking = False
        return
    
   

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        dim = len(board.board)
                
        actions = []
        for row in range(dim):
            for column in range(dim):
                piece = board.get_value(row,column)
                
                if len(piece.possible_positions) > 0:
                    self.fools_errand(board, row, column)
                    for i in piece.possible_positions:
                        actions.append((row, column, i))
                    piece.possible_positions.clear()
                    return actions
        return actions
                    

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        (row, column, value) = action
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
                
                new_possible_positions = []
                for l in state.board.board[i][j].possible_positions:
                    new_possible_positions.append(l)
                v.possible_positions = new_possible_positions
                new_line.append(v)
            board.append(new_line)

        new_board = Board()
        new_board.board = board
        new_state = PipeManiaState(new_board)
        new_state.board.action(action)
        new_state.board.get_value(row, column).possible_positions.clear()
        

        self.current = new_state
        return new_state
        

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        #print("Estado: ", state.id)

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
    problem.border_pieces(board)
    goal_node = depth_first_tree_search(problem)
    #print("Is goal?", problem.goal_test(goal_node.state))
    #print("State: ", goal_node.state.id)
    print(goal_node.state.board.print(), sep="")
    
    
    pass
