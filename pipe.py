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


class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    board = []; # Game Board

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        v = self.board[row][col]
        if row < 0 or row >= len(self.board) or col < 0 or col >= len(self.board[0]):
            return None
        else:
            return self.board[row][col]
        
    #implementada por nós, podemos?
    def set_value(self, row: int, col: int, value: str):
        """Altera o valor na respetiva posição do tabuleiro."""
        self.board[row][col] = value
        
    def action(self, action: tuple) -> str:
        value = self.get_value(action[0], action[1])
        orientation = action[2]
        
        #action = (row, col, orientation)
        #orientation = True -> clockwise
        #orientation = False -> counter-clockwise
        
        #podemos usar match? (um switch para strings)
        if value == "None":
            return "None"
        elif value == "FC":
            if orientation == True:
                value = "FD"
            elif orientation == False: #apenas por uma questão de clareza, else funcionava bem
                value = "FE"
        elif value == "FB":
            if orientation == True:
                value = "FE"
            elif orientation == False:
                value = "FD"
        elif value == "FE":
            if orientation == True:
                value = "FC"
            elif orientation == False:
                value = "FB"
        elif value == "FD":
            if orientation == True:
                value = "FB"
            elif orientation == False:
                value = "FC"
        elif value == "BC":
            if orientation == True:
                value = "BD"
            elif orientation == False:
                value = "BE"
        elif value == "BB":
            if orientation == True:
                value = "BE"
            elif orientation == False:
                value = "BD"
        elif value == "BE":
            if orientation == True:
                value = "BC"
            elif orientation == False:
                value = "BB"
        elif value == "BD":
            if orientation == True:
                value = "BB"
            elif orientation == False:
                value = "BC"
        elif value == "VC":
            if orientation == True:
                value = "VD"
            elif orientation == False:
                value = "VE"
        elif value == "VB":
            if orientation == True:
                value = "VE"
            elif orientation == False:
                value = "VD"
        elif value == "VE":
            if orientation == True:
                value = "VC"
            elif orientation == False:
                value = "VB"
        elif value == "VD":
            if orientation == True:
                value = "VB"
            elif orientation == False:
                value = "VC"
        elif value == "LH":
            value = "LV"
        elif value == "LV":
            value = "LH"
            
        return value
        

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
            board.append(line)
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
        
        state.board.set_value(action[0], action[1], self.current.board.action(action))
        new_state = PipeManiaState(state.board)
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
