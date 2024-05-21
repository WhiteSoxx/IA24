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
    locked = False

    """Representação interna de uma peça do PipeMania."""
    def __init__(self, value: str):
        self.value = value

    def rotate(self, clockwise: bool):
        """Roda a peça 90° no sentido dos ponteiros do relógio se
        'clockwise' for True, caso contrário, no sentido contrário."""
        # TODO
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
        
    #mudar
    def possible_positions(self, board, row: int, col: int):
        possible_positions = []
        top_piece = board.get_value(row - 1, col)
        left_piece = board.get_value(row, col - 1)
        
        if top_piece != None and left_piece != None:
            top_value = top_piece.value
            left_value = left_piece.value
            
            if top_value in BOT_OPENING and left_value in RIGHT_OPENING:
                possible_positions.clear()
                return possible_positions
            elif top_value in BOT_OPENING:
                possible_positions.append("FC")
                return possible_positions
            elif left_value in RIGHT_OPENING:
                possible_positions.append("FE")
                return possible_positions
            else:
                possible_positions.append("FB")
                possible_positions.append("FD")
                return possible_positions
            
        if top_piece != None:
            top_value = top_piece.value
            if top_value in BOT_OPENING:
                possible_positions.append("FC")
            else: #top não tem abertura nem a esquerda
                possible_positions.append("FB")
                possible_positions.append("FD")
            return possible_positions
        
        elif left_piece != None:
            left_value = left_piece.value
            if left_value in RIGHT_OPENING:
                possible_positions.append("FE")
            else: #top não tem abertura nem a esquerda
                possible_positions.append("FB")
                possible_positions.append("FD")
            return possible_positions
        
        elif top_piece == None and left_piece == None: #FIXME ELSE?? EM VEZ DE ELIF?
            possible_positions.append("FB")
            possible_positions.append("FD")
        
        return possible_positions

    def transform(self, new_value):
        self.value = new_value
    
class B_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)

    def possible_positions(self, board, row: int, col: int):
        possible_positions = []
        top_piece = board.get_value(row - 1, col)
        left_piece = board.get_value(row, col - 1)
        
        if top_piece != None and left_piece != None:
            top_value = top_piece.value
            left_value = left_piece.value
            
            if top_value in BOT_OPENING and left_value in RIGHT_OPENING:
                possible_positions.append("BC")
                possible_positions.append("BE")
                return possible_positions
            elif top_value in BOT_OPENING:
                possible_positions.append("BD")
                return possible_positions
            elif left_value in RIGHT_OPENING:
                possible_positions.append("BB")
                return possible_positions
            return possible_positions #FIXME
            
        if top_piece != None:
            top_value = top_piece.value
            if top_value in BOT_OPENING:
                possible_positions.append("BD")
            return possible_positions
        
        elif left_piece != None:
            left_value = left_piece.value
            if left_value in RIGHT_OPENING:
                possible_positions.append("BB")
            return possible_positions
        
        return possible_positions
        
    def transform(self, new_value):
        self.value = new_value
        
class V_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        
    def possible_positions(self, board, row: int, col: int):
        possible_positions = []
        top_piece = board.get_value(row - 1, col)
        left_piece = board.get_value(row, col - 1)
        
        if top_piece != None and left_piece != None:
            top_value = top_piece.value
            left_value = left_piece.value
            
            if top_value in BOT_OPENING and left_value in RIGHT_OPENING:
                possible_positions.append("VC")
                return possible_positions
            elif top_value in BOT_OPENING:
                possible_positions.append("VD")
                return possible_positions
            elif left_value in RIGHT_OPENING:
                possible_positions.append("VE")
                return possible_positions
            else:
                possible_positions.append("VB")
                return possible_positions
            
        if top_piece != None:
            top_value = top_piece.value
            if top_value in BOT_OPENING:
                possible_positions.append("VD")
            else: #top não tem abertura nem a esquerda
                possible_positions.append("VB")
            return possible_positions
        
        elif left_piece != None:
            left_value = left_piece.value
            if left_value in RIGHT_OPENING:
                possible_positions.append("VE")
            else: #top não tem abertura nem a esquerda
                possible_positions.append("VB")
            return possible_positions
        
        elif top_piece == None and left_piece == None:
            possible_positions.append("VB")
        
        return possible_positions
        
    def transform(self, new_value):
        #if len(possible_positions) > 0:
            #possible_positions.remove(new_value)
        self.value = new_value


class L_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        
    def possible_positions(self, board, row: int, col: int):
        possible_positions = []
        top_piece = board.get_value(row - 1, col)
        left_piece = board.get_value(row, col - 1)
        
        if top_piece != None and left_piece != None:
            top_value = top_piece.value
            left_value = left_piece.value
            
            if top_value in BOT_OPENING and left_value in RIGHT_OPENING:
                return possible_positions
            elif top_value in BOT_OPENING:
                possible_positions.append("LV")
                return possible_positions
            elif left_value in RIGHT_OPENING:
                possible_positions.append("LH")
                return possible_positions
            return possible_positions
            
        if top_piece != None:
            top_value = top_piece.value
            if top_value in BOT_OPENING:
                possible_positions.append("LV")
            return possible_positions
        
        elif left_piece != None:
            left_value = left_piece.value
            if left_value in RIGHT_OPENING:
                possible_positions.append("LH")
            return possible_positions
        
        return possible_positions
    
    def transform(self, new_value):
        self.value = new_value         
        
class Board:
    """Representação interna de um tabuleiro de PipeMania."""

    board =  []
    dim = 0

    def __init__(self):
        board = list()
        dim = 0

    def get_value(self, row: int, col: int) -> Piece:
        """Devolve o valor na respetiva posição do tabuleiro."""
        dim = self.dim
        if row < 0 or row >= dim or col < 0 or col >= dim:
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

    # def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
    #     """Devolve os valores imediatamente acima e abaixo,
    #     respectivamente."""
    #     v1 = self.get_value(row - 1, col)
    #     v2 = self.get_value(row + 1, col)
    #     return (v1, v2)

    # def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
    #     """Devolve os valores imediatamente à esquerda e à direita,
    #     respectivamente."""
    #     v1 = self.get_value(row, col - 1)
    #     v2 = self.get_value(row, col + 1)
    #     return (v1, v2)

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
        dim = len(line)
        while(line != []):
            new_line = list()
            for i in range(dim):
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
        new_board.dim = dim
        return new_board
    
    def print(self):
        s = ""
        dim = self.dim
        
        for i in range(dim):
            for j in range(dim):
                s += self.board[i][j].value
                if j < dim - 1:
                    s+= '\t'
            if i< dim - 1:
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
        limit = board.dim
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
                top_value = top_piece.value
                if top_value in BOT_OPENING:
                    if i not in TOP_OPENING:
                        leaking = True
                else:
                    if i in TOP_OPENING:
                        leaking = True

            if left_piece != None:
                left_value = left_piece.value
                if left_value in RIGHT_OPENING:
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
        dim = board.dim
                
        actions = []
        for row in range(dim):
            for column in range(dim):
                piece = board.get_value(row,column)
                if not piece.locked:
                    possible_positions = piece.possible_positions(board, row, column)
                    piece.locked = True
                    if len(possible_positions) > 0:
                    #self.fools_errand(board, row, column)
                        for i in possible_positions:
                            actions.append((row, column, i))
                        return actions
                # if len(piece.possible_positions) > 0:
                #     self.fools_errand(board, row, column)
                #     for i in piece.possible_positions:
                #         actions.append((row, column, i))
                #     piece.possible_positions.clear()
                #    return actions
        return actions
                    

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        (row, column, value) = action
        dim = state.board.dim
        board = list()
        for i in range(dim):
            new_line = list()
            for j in range(dim):
                k = state.board.get_value(i, j).value
                if(k[0] == "F"):
                    v = F_Piece(k)
                elif(k[0] == "B"):
                    v = B_Piece(k)
                elif(k[0] == "V"):
                    v = V_Piece(k)
                elif(k[0] == "L"):
                    v = L_Piece(k)
                if state.board.get_value(i, j).locked:
                    v.locked = True
                
                # new_possible_positions = []
                # for l in state.board.board[i][j].possible_positions:
                #     new_possible_positions.append(l)
                # v.possible_positions = new_possible_positions
                new_line.append(v)
            board.append(new_line)

        new_board = Board()
        new_board.board = board
        new_board.dim = state.board.dim
        new_state = PipeManiaState(new_board)
        new_state.board.action(action)
        new_state.board.get_value(row, column).locked = True
        

        self.current = new_state
        return new_state
        

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        #print("Estado: ", state.id)
        piece_count = 0
        
        for i in range(state.board.dim):
            for j in range(state.board.dim):
                testing_value = state.board.get_value(i, j).value #getvalue?
                if(testing_value in TOP_OPENING):
                    if(state.board.get_value(i - 1, j) == None):
                        return False
                    elif(state.board.get_value(i - 1, j).value not in BOT_OPENING):
                        return False
                if(testing_value in RIGHT_OPENING):
                    if(state.board.get_value(i, j + 1) == None):
                        return False
                    elif(state.board.get_value(i, j + 1).value not in LEFT_OPENING):
                        return False
                if(testing_value in BOT_OPENING):
                    if(state.board.get_value(i + 1, j) == None):
                        return False
                    elif(state.board.get_value(i + 1, j).value not in TOP_OPENING):
                        return False
                if(testing_value in LEFT_OPENING):
                    if(state.board.get_value(i, j - 1) == None):
                        return False
                    elif(state.board.get_value(i, j - 1).value not in RIGHT_OPENING):
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
    #problem.border_pieces(board)
    goal_node = depth_first_tree_search(problem)
    #print("Is goal?", problem.goal_test(goal_node.state))
    #print("State: ", goal_node.state.id)
    print(goal_node.state.board.print(), sep="")
    
    
    pass
