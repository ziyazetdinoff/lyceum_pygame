import pygame
import sys
import random


from pygame.locals import *


class Par(object):
    def __init__(self):
        self.width = 800  # ширина окна
        self.height = 501

# Создаём все константы проекта


q = Par()
board_width = 5  # количество столбцов
board_height = 5  # количество рядов
tile_size = 80  # размер одной плитки


black = (0, 0, 0)
green = (253, 77, 154)
dark = (255, 160, 36)
white = (255, 255, 255)
brightblue = (0, 50, 255)
darktur = (3, 54, 73)


bgcolor = darktur
tile_color = dark
button_color = white
button_next_color = black
message_color = white
text_color = white
boarder_color = brightblue
basic_font_size = 20
left = 'left'
right = 'right'

fps = 30
blank = None


xmargin = int((q.width - (tile_size * board_width + (board_width - 1))) / 2)
ymargin = int((q.height - (tile_size * board_height + (board_height - 1))) / 2)

up = 'up'
down = 'down'


def main():
    global basic_font, reset_surf, fps_clock, display_surf
    global reset_rect, solve_surf, solve_rect, new_surf, new_rect

    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((q.width, q.height))
    pygame.display.set_caption('Пазл из Плиток')
    basic_font = pygame.font.Font('freesansbold.ttf', basic_font_size)

    #  Здесь хранятся данные о кнопках "Заново", "Новая игра", "Решение"
    reset_surf, reset_rect = make_text('Заново',    text_color, tile_color, q.width - 120, q.height - 90)
    new_surf,   new_rect = make_text('Новая игра', text_color, tile_color, q.width - 120, q.height - 60)
    solve_surf, solve_rect = make_text('Решение',    text_color, tile_color, q.width - 120, q.height - 30)

    main_board, solution_seq = generate_new_puzzle(80)
    solve_board = get_starting_board()  # решённый пазл точно такой же, как и вначале
    all_moves = []  # список шагов

    while True:  # основной игровой цикл
        slide_to = None  # направление, если плитка может куда-либо сдвинуться
        msg = 'Двигайте плитку кнопками или же нажимайте на неё'  # подсказка игроку
        if main_board == solve_board:  # в случае решения пазла
            msg = 'Решено!'

        draw_board(main_board, msg)  # вывод подсказки на экран

        check_for_quit()   # проверка на выход
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = get_spot_clicked(main_board, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # проверяем нажал ли игрок куда либо
                    # нажал на "Заново"
                    if reset_rect.collidepoint(event.pos):
                        reset_animation(main_board, all_moves)
                        all_moves = []
                    # нажал на "Решение"
                    elif solve_rect.collidepoint(event.pos):
                        reset_animation(main_board, solution_seq + all_moves)
                        all_moves = []
                    # нажал на "Новая Игра"
                    elif new_rect.collidepoint(event.pos):
                        main_board, solution_seq = generate_new_puzzle(80)
                        all_moves = []

                else:

                    blankx, blanky = get_blank_position(main_board)
                    if spotx == blankx + 1 and spoty == blanky:
                        slide_to = left
                    elif spotx == blankx and spoty == blanky + 1:
                        slide_to = up
                    elif spotx == blankx and spoty == blanky - 1:
                        slide_to = down
                    elif spotx == blankx - 1 and spoty == blanky:
                        slide_to = right
            elif event.type == KEYUP:
                # проверяем нажал ли пользователь кнопку для сдвига плитки
                if event.key in (K_LEFT, K_a) and is_valid_move(main_board, left):
                    slide_to = left
                elif event.key in (K_RIGHT, K_d) and is_valid_move(main_board, right):
                    slide_to = right
                elif event.key in (K_DOWN, K_s) and is_valid_move(main_board, down):
                    slide_to = down
                elif event.key in (K_UP, K_w) and is_valid_move(main_board, up):
                    slide_to = up

        if slide_to:
            slide_animation(main_board, slide_to, 'Двигайте плитку кнопками или же нажимайте на неё', 8)
            make_move(main_board, slide_to)
            all_moves.append(slide_to)  # записываем данный ход в список
        pygame.display.update()
        fps_clock.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for event in pygame.event.get(QUIT):  # проверка на выход
        terminate()
        # завершаем
    for event in pygame.event.get(KEYUP):  # проверка нажатых клавиш
        if event.key == K_ESCAPE:
            terminate()
            # завершаем если нажата клавиша Esc
        pygame.event.post(event)


def get_starting_board():
    # Функция, которая даёт нам список с плитками исходя из их количества
    # Например, если у нас по 2 плитке в ширину и в высоту
    # Тогда функция возвратит [[1, 3], [2, blank]]
    counter = 1
    board = []
    for x in range(board_width):
        column = []
        for y in range(board_height):
            column.append(counter)
            counter += board_width
        board.append(column)
        counter -= board_width * (board_height - 1) + board_width - 1

    board[board_width - 1][board_height - 1] = blank
    return board


def get_blank_position(board):
    for x in range(board_width):
        for y in range(board_height):
            if board[x][y] == blank:
                return x, y


def make_move(board, move):
    blankx, blanky = get_blank_position(board)

    if move == up:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == down:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == left:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == right:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def is_valid_move(board, move):
    # проверка на возможность данного хода
    blankx, blanky = get_blank_position(board)
    return (move == up and blanky != len(board[0]) - 1) or \
           (move == down and blanky != 0) or \
           (move == left and blankx != len(board) - 1) or \
           (move == right and blankx != 0)


def get_random_move(board, last_move=None):
    valid_moves = [up, down, left, right]

    # удаляем ходы, которые невозможны
    if last_move == left or not is_valid_move(board, right):
        valid_moves.remove(right)
    if last_move == right or not is_valid_move(board, left):
        valid_moves.remove(left)
    if last_move == up or not is_valid_move(board, down):
        valid_moves.remove(down)
    if last_move == down or not is_valid_move(board, up):
        valid_moves.remove(up)

    return random.choice(valid_moves)


def get_left_top_of_tile(tile_x, tile_y):
    top = ymargin + (tile_y * tile_size) + (tile_y - 1)
    lef = xmargin + (tile_x * tile_size) + (tile_x - 1)

    return lef, top


def get_spot_clicked(board, x, y):
    # находим координаты кнопки
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            lef, top = get_left_top_of_tile(tilex, tiley)
            tile_rect = pygame.Rect(lef, top, tile_size, tile_size)
            if tile_rect.collidepoint(x, y):
                return tilex, tiley
    return None, None


def draw_tile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = get_left_top_of_tile(tilex, tiley)
    pygame.draw.rect(display_surf, tile_color, (left + adjx, top + adjy, tile_size, tile_size))
    text_surf = basic_font.render(str(number), True, text_color)
    text_rect = text_surf.get_rect()
    text_rect.center = left + int(tile_size/ 2) + adjx, top + int(tile_size/ 2) + adjy
    display_surf.blit(text_surf, text_rect)


def make_text(text, color, bgcolor, top, left):
    # создаем области для текста
    text_surf = basic_font.render(text, True, color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect


def draw_board(board, message):
    display_surf.fill(bgcolor)

    if message:
        text_surf, text_rect = make_text(message, message_color, bgcolor, 5, 5)
        display_surf.blit(text_surf, text_rect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                draw_tile(tilex, tiley, board[tilex][tiley])

    left, top = get_left_top_of_tile(0, 0)
    width = board_width * tile_size
    height = board_height * tile_size
    pygame.draw.rect(display_surf, boarder_color, (left - 5, top - 5, width + 11, height + 11), 4)

    display_surf.blit(reset_surf, reset_rect)
    display_surf.blit(new_surf, new_rect)
    display_surf.blit(solve_surf, solve_rect)


def slide_animation(board, direction, message, animation_speed):

    blankx, blanky = get_blank_position(board)
    if direction == up:
        movex = blankx
        movey = blanky + 1

    elif direction == down:
        movex = blankx
        movey = blanky - 1

    elif direction == left:
        movex = blankx + 1
        movey = blanky

    elif direction == right:
        movex = blankx - 1
        movey = blanky

    draw_board(board, message)
    base_surf = display_surf.copy()

    move_left, move_top = get_left_top_of_tile(movex, movey)
    pygame.draw.rect(base_surf, bgcolor, (move_left, move_top, tile_size, tile_size))

    for i in range(0, tile_size, animation_speed):
        # анимация плитки
        check_for_quit()
        display_surf.blit(base_surf, (0, 0))
        if direction == up:
            draw_tile(movex, movey, board[movex][movey], 0, -i)

        if direction == down:
            draw_tile(movex, movey, board[movex][movey], 0, i)

        if direction == left:
            draw_tile(movex, movey, board[movex][movey], -i, 0)

        if direction == right:
            draw_tile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        fps_clock.tick(fps)


def generate_new_puzzle(num_slides):

    sequence = []
    board = get_starting_board()
    draw_board(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    # пауза в пол секунды для плавности

    last_move = None

    for i in range(num_slides):
        move = get_random_move(board, last_move)
        slide_animation(board, move, 'Подождите, идёт создание нового пазла...', animation_speed=int(tile_size / 3))
        make_move(board, move)
        sequence.append(move)
        last_move = move

    return board, sequence


def reset_animation(board, all_moves):
    # переворачиваем список с нашими ходами
    rev_all_moves = all_moves[:]
    rev_all_moves.reverse()

    for move in rev_all_moves:
        if move == up:
            opposite_move = down
        elif move == down:
            opposite_move = up
        elif move == left:
            opposite_move = right
        elif move == right:
            opposite_move = left

        slide_animation(board, opposite_move, '', animation_speed=int(tile_size / 2))
        make_move(board, opposite_move)


if __name__ == '__main__':
    main()

