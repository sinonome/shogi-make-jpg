import info

test = 'sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1'

class Board:
    def __init__(self):
        self.board = [['' for _ in range(9)] for _ in range(9)]
        self.turn = None
        self.num_of_turn = None
        self.isComp = False
        self.now = [0, 0]
        self.isComp_hand = False

    def add_info(self, command, *param):
        if self.isComp:
            raise Exception("盤面は既に完成しています")

        if command == 'skip':
            # 盤面スキップ回数
            self.check_now()
            count, = param
            self.now[1] += count
        elif command == 'add':
            # 情報を入力
            self.check_now()
            x, y = self.now
            self.board[x][y] = '+' * param[1] + param[0]
            self.now[1] += 1
        elif command == 'next':
            # 次の行に
            self.now[0] += 1
            self.now[1] = 0
        elif command == 'finish':
            # 終了する
            self.isComp = True
        else:
            raise Exception("不正なcommandです:", command)

    def add_hand(self, command, *param):
        if command == 'add':
            # 情報を入力
            pass
        elif command == 'finish':
            # 終了する
            pass
        else:
            raise Exception("不正なcommandです:", command)

    def set_turn(self, turn):
        if turn in {'b', 'w'}:
            self.turn = (turn == 'b')
        else:
            raise Exception("不正な値です:", turn)

    def set_num_of_turn(self, num):
        self.num_of_turn = int(num)

    def check_now(self):
        if self.now[0] >= 9 or self.now[1] >= 9:
            raise Exception("範囲外の指定があります")


class Piece:
    def __init__(self, piece, isGradeUp = False):
        if piece == "":
            # 空の盤面を表す
            self.piece = ""
            self.turn = None
            self.isGradeUp = None
        else:
            _piece = piece.lower()
            if not _piece in info.all_piece:
                raise Exception("不正なパラメータです:", piece)
            self.piece = _piece             # 常に小文字
            self.turn = (piece == _piece)   # true : 先手
            self.isGradeUp = isGradeUp      # 成っているかどうか


class ParseSfen:
    def __init__(self, sfen):
        self.sfen = sfen
        self.info = Board()
        self.parse()

    def parse(self):
        sfen_data = self.sfen.split(" ")
        if sfen_data[0] == 'sfen':
            board, *board_data = sfen_data[1:]

        # 盤面の読み込み
        print(board, board_data)
        isGradeUp = False
        for piece in board:
            if piece.isdecimal():
                if isGradeUp:
                    raise Exception("+の後に数字がくることはありません。")
                self.info.add_info('skip', int(piece))
            elif piece == '+':
                if isGradeUp:
                    raise Exception("'++' の表記があります。")
                isGradeUp = True
            elif piece.lower() in info.all_piece:
                self.info.add_info('add', piece, isGradeUp)
                isGradeUp = False
            elif piece == '/':
                if isGradeUp:
                    raise "'+/' という表記が存在します。"
                self.info.add_info('next')
            else:
                raise Exception("不正なパラメータです:", piece)

        self.info.add_info('finish')

        # 手番
        self.info.set_turn(board_data[0])

        # 手駒
        if sfen_data[1] == '-':
            self.info.add_hand('finish')
        else:
            for piece in sfen_data[1]:
                self.info.add_hand('add', piece)
            self.info.add_hand('finish')

        # 手数
        self.info.set_num_of_turn(board_data[2])


if __name__ == "__main__":
    board = ParseSfen(test)
    print(*board.info.board, sep='\n')
    print("手番 :", "Black" if board.info.turn else "White")
    print("手数 :", board.info.num_of_turn)