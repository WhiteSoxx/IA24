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
    connects_to = []
    exits  = []
    """Representação interna de uma peça do PipeMania."""
    def __init__(self, value: str):
        self.value = value

    def rotate(self, clockwise: bool):
        """Roda a peça 90° no sentido dos ponteiros do relógio se
        'clockwise' for True, caso contrário, no sentido contrário."""
        # TODO
        pass
    
    def set_exits(self):
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

class L_Piece(Piece):
    def __init__(self, value: str):
        super().__init__(value)
        self.set_exits()
        
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

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    board = []; # Game Board

    def get_value(self, row: int, col: int) -> Piece:
        """Devolve o valor na respetiva posição do tabuleiro."""
        v = self.board[row][col]
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
        
        #action = (row, col, orientation)
        #orientation = True -> clockwise
        #orientation = False -> counter-clockwise
        
        #podemos usar match? (um switch para strings)
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
        return board

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
        # TODO
        pass

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        
        new_state = PipeManiaState(state.board)
        new_state.board.action(action)
        return new_state
        

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

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
    
    game = Board()
    game.board = game.parse_instance()

    problem = PipeMania(game)
    initial_state = PipeManiaState(game)
    print(initial_state.board.get_value(2, 2))
    # Realizar ação de rodar 90° clockwise a peça (2, 2)
    result_state = problem.result(initial_state, (2, 2, True))
    # Mostrar valor na posição (2, 2):
    print(result_state.board.get_value(2, 2))
    
    pass
