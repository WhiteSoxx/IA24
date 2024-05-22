# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 122:
# 105918 Gabriel Bispo
# 106326 Guilherme Filipe

import sys
import time
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

# ABERTURAS
OPENINGS = {
    "C": {"FC", "BC", "BE", "BD", "VC", "VD", "LV"}, #TOPO
    "E": {"FE", "BC", "BB", "BE", "VC", "VE", "LH"}, #ESQUERDA
    "D": {"FD", "BC", "BB", "BD", "VB", "VD", "LH"}, #DIREITA
    "B": {"FB", "BB", "BE", "BD", "VB", "VE", "LV"}, #BAIXO
}

#PECAS
PIECES = {
    "F": {"FC", "FD", "FB", "FE"},  #FURO
    "B": {"BC", "BD", "BB", "BE"},  #BIFURCACAO
    "V": {"VC", "VD", "VB", "VE"},  #CURVA
    "L": {"LH", "LV"},              #LINHA
}

class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    def get_board(self) -> 'Board':
        return self.board

class Piece:
    def __init__(self, value):
        self.val = value
        self.group = 0

    def value(self):
        return self.value
 
class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    def __init__(self, cells):
        self.cells = cells
        self.size = len(cells)
        self.row_pivot = 0
        self.column_pivot = 0
        self.group_counter = 0
        self.joined_groups = 0

    def get_value(self, row: int, col: int) -> Piece:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return None
        else:
            return self.cells[row][col]

    def action(self, row: int, col: int, value: str, state: PipeManiaState):
        """Realiza uma ação, mudando o valor na linha e coluna indicadas
        para o valor pretendido, devolvendo um novo tabuleiro."""

        merged_groups = set()
        new_piece = Piece(value)
        board = state.board
        new_piece.group = board.get_value(row, col).group
        new_row = self.cells[row][:col] + [new_piece] + self.cells[row][col+1:]
        new_cells = self.cells[:row] + [new_row] + self.cells[row + 1 :]
        new_board = Board(new_cells)
        new_board.group_counter = board.group_counter
        new_board.joined_groups = board.joined_groups
        top_piece = new_board.adjacent_vertical_values(row, col)[0]
        left_piece = new_board.adjacent_horizontal_values(row,col)[0]

        new_group = True 

        if top_piece is not None and top_piece.val in OPENINGS["B"]:
            new_piece.group = top_piece.group
            new_group = False

        if left_piece is not None and left_piece.val in OPENINGS["D"]:
            new_piece.group = left_piece.group

            # Antes de aumentar o counter do joined_groups verifica se se as pecas 
            # nao pertencem ao mesmo grupo
            if(new_group == False and not left_piece.group == top_piece.group):
                min_group = min(left_piece.group, top_piece.group)
                max_group = max(left_piece.group, top_piece.group)
                joined_groups = (min_group, max_group)
                # Caso a juncao nao tenha sido adicionada anteriormente
                if joined_groups not in merged_groups:
                    new_board.joined_groups += 1
                    merged_groups.add(joined_groups)
            new_group = False
        
        if(new_group == True):
            new_board.group_counter += 1
            new_piece.group = new_board.group_counter
                
        new_board.row_pivot = self.row_pivot
        new_board.column_pivot = self.column_pivot
        return new_board

    def adjacent_vertical_values(self, row: int, col: int) -> (Piece, Piece):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        v1 = self.get_value(row - 1, col)
        v2 = self.get_value(row + 1, col)
        return (v1, v2)
        

    def adjacent_horizontal_values(self, row: int, col: int) -> (Piece, Piece):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        v1 = self.get_value(row, col - 1)
        v2 = self.get_value(row, col + 1)
        return (v1, v2)

    def get_possible_actions(self, row: int, col: int):
        piece = self.get_value(row, col)

        left_piece, right_piece = self.adjacent_horizontal_values(row, col)
        top_piece, bot_piece = self.adjacent_vertical_values(row,col)
        
        possible_actions = set()

        if top_piece is not None  and top_piece.val in OPENINGS["B"]: 
            possible_actions = PIECES[piece.val[0]] & OPENINGS["C"] 
        else:
            possible_actions = PIECES[piece.val[0]] - OPENINGS["C"]
        
        if left_piece is not None and left_piece.val in OPENINGS["D"]: 
            possible_actions = possible_actions &  OPENINGS["E"]
        else:
            possible_actions = possible_actions -  OPENINGS["E"]
        
        if bot_piece is None:
            possible_actions = possible_actions - OPENINGS["B"]
        
        if right_piece is None:
            possible_actions = possible_actions - OPENINGS["D"]

        return possible_actions
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        board = list()
        line = stdin.readline().split()
        while(line != []):
            new_line = list()
            for i in range(len(line)):
                piece = Piece(line[i])
                new_line.append(piece)
            board.append(new_line)
            line = stdin.readline().split()
        new_board = Board(board)
        return new_board

    def print(self):
        s = ""
        size = self.size
        for i in range(size):
            for j in range(size):
                s += self.cells[i][j].val
                if j < size-1:
                    s+= '\t'
            if i< size-1:
                s += "\n"
        return s
    
    def print_groups(self): # for debugging
        s = ""
        size = self.size
        for i in range(size):
            for j in range(size):
                s += str(self.cells[i][j].group)
                if j < size-1:
                    s+= '\t'
            if i< size-1:
                s += "\n"
        return s

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = PipeManiaState(board)
        self.goal = None
        self.current = self.initial


    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        
        size = board.size
        actions = []

        if( not board.row_pivot == size):
            for row in range(board.row_pivot, size):
                for column in range(board.column_pivot, size):
                    board.column_pivot += 1
                    possible_actions = board.get_possible_actions(row,column)
                    for possible_action in possible_actions:
                        actions.append((row,column,possible_action))

                    if(board.column_pivot == size):
                        board.column_pivot = 0
                        board.row_pivot += 1
                    return actions
                
        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state). """
        (row, column, value) = action
        return PipeManiaState(state.board.action(row, column, value, state))

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = state.board
        size = board.size
        row_pivot = state.board.row_pivot
        col_pivot = state.board.column_pivot
        
        for row in range(row_pivot ,  size):
            for column in range(col_pivot , size):
                piece = board.cells[row][column]
                if piece.val in OPENINGS["C"]:
                    top_piece = board.get_value(row - 1, column)
                    if top_piece == None or top_piece.val not in OPENINGS["B"]: return False
                          
                if piece.val in OPENINGS["D"]:
                    right_piece = board.get_value(row, column +1)
                    if right_piece == None or right_piece.val not in OPENINGS["E"]: return False
                if piece.val in OPENINGS["B"]:
                    bot_piece = board.get_value(row+1, column)
                    if bot_piece==None or bot_piece.val not in OPENINGS["C"]: return False

                if piece.val in OPENINGS["E"]:
                    left_piece = board.get_value(row, column-1)
                    if left_piece==None or left_piece.val not in OPENINGS["D"]: return False
        if(board.joined_groups == board.group_counter - 1 or board.group_counter == 0): 
            return True
        else:
            return False

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance()
    problem = PipeMania(board)
    goal_node = depth_first_tree_search(problem)    
    print(goal_node.state.board.print(), sep="")
    pass