from random import randint  # подключение рандома


class Dot: # Точка
    def __init__(self, x, y):   # иницилизация точки
        self.x = x
        self.y = y

    def __eq__(self, other):    # сравнение точки
        return self.x == other.x and self.y == other.y

    def __repr__(self):     # печать точки
        return "(" + str(self.x) + " , " + str(self.y) + ")"


class Ship:  # Кораблик
    def __init__(self, bow, l, o):  # иницилизация кораблика
        self.bow = bow  # точка носа кораблика
        self.l = l      # длина кораблика
        self.o = o      # маркер расположения кораблика (горизонт, вертикаль)
        self.lives = l      # количество жизней кораблика (длина)

    @property
    def dots(self):  # Метод создание кораблика
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x  # нос караблика
            cur_y = self.bow.y

            if self.o == 0:  # тело караблика
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))     # добавление точек в кораблик по длине

        return ship_dots

    def shooten(self, shot):  # выстрел в караблик
        return shot in self.dots


class Board:    # Поле
    def __init__(self, hid=False, size=6):  # иницилизация поля
        self.size = size    # размер поля
        self.hid = hid  # видимость кораблика на поле
        self.count = 0  # количество подбитых корабликов
        self.field = [["O"] * size for _ in range(size)]    # создание поля
        self.busy = []  # лист занетых точек
        self.ships = []     # лист точек кораблей

    def add_ship(self, ship):   # добавление кораблика на поле
        for d in ship.dots:
            if self.out(d) or d in self.busy:   # проверка ошибки расположения кораблика
                raise BoardWrongShipException()

        for d in ship.dots:     # добавление кораблика на поле
            self.field[d.x][d.y] = "■"  # заполнение поля
            self.busy.append(d)     # добавление координат в поле занятых клеток

        self.ships.append(ship)     # добавление кораблика в массив точек кораблей
        self.contour(ship)      # оконтовка кораблика

    def contour(self, ship, verb=False):    # контур кораблика
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1),   (0, 0),  (0, 1),
                (1, -1),   (1, 0),  (1, 1)
                                            ]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."

                    self.busy.append(cur)   # заполнение поля занятых точек

    def prinfield(self, other):      # Вывод поля
        res =  "-------------------------------------------------------------- \n"
        res += "          Поле Игрока                 Поле Компьютера    \n"
        res += "-------------------------------------------------------------- \n"
        res += "  || 1 | 2 | 3 | 4 | 5 | 6 ||   || 1 | 2 | 3 | 4 | 5 | 6 || "
        for i in range(6):  # проход по спискам
            res += "\n" + str(i + 1) + " ||"

            for j in range(6):      # проход по списку поля игрока
                line = str()
                line += " " + self.field[i][j] + " |"   # формирование строки поля игрока

                if self.hid:
                    line = line.replace("■", "O")   # проверка отображения кораблей на поле
                res += line


            res += "|   ||"     # добавление разделителя

            for j in range(6):      # проход по списку поля компьютера
                line = str()
                line += " " + other.field[i][j] + " |"      # формирование строки поля компьютера

                if other.hid:
                    line = line.replace("■", "O")   # проверка отображения кораблей на поле

                res += line

            res += "| " + str(i + 1)    # добавление нумерации поля

        return res

    def out(self, d):   # проверка ошибки поля (за пределы поля)
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):  # выстрел
        if self.out(d):     # проверка ошибки поля
            raise BoardOutException()

        if d in self.busy:  # проверка ошибки клетки
            raise BoardUsedException()

        self.busy.append(d)     # добавление точки в поле занятых клеток

        for ship in self.ships:     # проход по кораблику
            if d in ship.dots:      # если точка в кораблике
                ship.lives -= 1     # минус жизнь
                self.field[d.x][d.y] = "X"  # заполнение поля

                if ship.lives == 0:     # если жизней у кораблика нет
                    self.count += 1     # обновление счетчика подбитых кораблей
                    self.contour(ship, verb=True)   # создание контура бодбитого кораблика
                    print("Корабль уничтожен!")
                    return True     # при уничкожении кораблика + ход

                else:
                    print("Корабль подбит!")
                    return True     # при подбитии кораблика + ход

        self.field[d.x][d.y] = "."      # заполнение поля промахом
        print("Промах!")
        return False    # нет дополнительного хода

    def begin(self):    # обновления поля занятых точек
        self.busy = []


class BoardException(Exception):    # класс ошибок
    pass


class BoardOutException(BoardException):    # ошибка поля
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):   # ошибка клетки
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):  # ошибка положения кораблика
    pass


class Player:   # клас игрок
    def __init__(self, board, enemy):
        self.board = board      # своё поле
        self.enemy = enemy      # поле врага

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:    # отлов ошибок
                target = self.ask()     # запрос точки
                repeat = self.enemy.shot(target)    # выстрел по запрошенной точке
                return repeat

            except BoardException as e:
                print(e)


class AI(Player):   # ХОД КОМПЬЮТЕРА
    def ask(self):
        step = 1
        for i in range(6):
            for j in range(6):
                if self.enemy.field[i][j] == "X":    # ищем попадание на поле
                    if i == 0:
                        if self.enemy.field[i + 1][j] == "■":
                            if step:
                                d = Dot(i + 1, j)
                                step = 0
                                break

                    if i == 5:
                        if self.enemy.field[i - 1][j] == "■":
                            if step:
                                d = Dot(i - 1, j)
                                step = 0
                                break

                    if 5 > i > 0:
                        if self.enemy.field[i - 1][j] != "■" and self.enemy.field[i + 1][j] == "■":
                            if step:
                                d = Dot(i + 1, j)
                                step = 0
                                break

                        if self.enemy.field[i - 1][j] == "■" and self.enemy.field[i + 1][j] != "■":
                            if step:
                                d = Dot(i - 1, j)
                                step = 0
                                break

                    if j == 0:
                        if self.enemy.field[i][j + 1] == "■":
                            if step:
                                d = Dot(i, j + 1)
                                step = 0
                                break

                    if j == 5:
                        if self.enemy.field[i][j - 1] == "■":
                            if step:
                                d = Dot(i, j - 1)
                                step = 0
                                break

                    if 5 > j > 0:
                        if self.enemy.field[i][j - 1] != "■" and self.enemy.field[i][j + 1] == "■":
                            if step:
                                d = Dot(i, j + 1)
                                step = 0
                                break

                        if self.enemy.field[i][j - 1] == "■" and self.enemy.field[i][j + 1] != "■":
                            if step:
                                d = Dot(i, j - 1)
                                step = 0
                                break

        if step:
            while True:     # треляем по не занятым клеткам
                d = Dot(randint(0, 5), randint(0, 5))
                if d not in self.enemy.busy:
                    break

        print("Ход компьютера: " + str(d.x + 1) + " " + str(d.y + 1))
        return d


class User(Player):     # ход игрока
    def ask(self):
        while True:     # запрос координат
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:     # класс игра
    def __init__(self, size=6):
        self.size = size    # задание размера доски
        pl = self.random_board()    # доска игрока
        co = self.random_board()    # доска компьютера
        co.hid = True  # отображение корабликов
        self.ai = AI(co, pl)    # определение полей для компьютера
        self.us = User(pl, co)      # определение полей для пользователя

    def random_board(self):     # создание рандомной доски
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):     # добавление на доску кораблей
        lens = [3, 2, 2, 1, 1, 1, 1]    # список длин корабликов
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1

                if attempts > 2000:
                    return None

                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break

                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def greet(self):    # приветствие
        print("------------------------------")
        print("         МОРСКОЙ БОЙ          ")
        print("------------------------------")
        print("          начнем игру         ")
        print("       люди против машин      ")
        print("------------------------------")
        print("       формат ввода: x y      ")
        print("       x - номер строки       ")
        print("       y - номер столбца      ")
        print("------------------------by-ZAV")

    def loop(self):
        num = 0
        while True:
            print(self.us.board.prinfield(self.ai.board))   # вывод доски

            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()

            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print(self.us.board.prinfield(self.ai.board))  # вывод доски
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print(self.us.board.prinfield(self.ai.board))  # вывод доски
                print("-" * 20)
                print("Компьютер выиграл!")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()

# тело программы
seebatle = Game()
seebatle.start()