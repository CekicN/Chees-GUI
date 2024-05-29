from typing import List
import config
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT
import pygame
from filelock import FileLock
from pynput import mouse
import os

def analyze_fen(fen):
    fen_board = fen.split(' ')[0]
    rows = fen_board.split('/')

    piece_symbols = {
        'r': 'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king', 'p': 'pawn',
        'R': 'rook', 'N': 'knight', 'B': 'bishop', 'Q': 'queen', 'K': 'king', 'P': 'pawn'
    }

    white_pieces = []
    white_locations = []
    black_pieces = []
    black_locations = []

    for i, row in enumerate(rows):
        col = 0
        for char in row:
            if char.isdigit():
                col += int(char)
            else:
                piece = piece_symbols[char]
                location = (col, i)
                if char.isupper():
                    white_pieces.append(piece)
                    white_locations.append(location)
                else:
                    black_pieces.append(piece)
                    black_locations.append(location)
                col += 1

    return white_pieces, white_locations, black_pieces, black_locations

def read_file():
    global white_pieces, white_locations, black_pieces, black_locations, fen, evaluations, ev
    file_path = config.input_path
    lock = FileLock(file_path + ".lock")
    with lock:
        with open(file_path, "r") as f:
            fen = f.readline()
            fen = fen.replace("\n", '')
            evaluations = []
            ev = ""
            for i in f:
                i = i.replace("\n", '')
                evaluations.append(i)
                ev += i
    white_pieces, white_locations, black_pieces, black_locations = analyze_fen(fen)

def write_to_file(from_coords,click_coords):
    potez = chr(from_coords[0] + ord('a'))
    potez += str(7 - (from_coords[1] - 1))
    potez += chr(click_coords[0] + ord('a'))
    potez += str(7 - (click_coords[1] - 1))

    file_path = config.output_path
    lock = FileLock(file_path + ".lock")
    with lock:
        with open(file_path, "w") as file:
            if potez in ev:
                file.write(f"Move:{potez}")
            else:
                file.write(f"Search:{potez}")
def read_config():
    global config_data
    file_path = "./files/config.txt"
    lock = FileLock(file_path + ".lock")
    with lock:
        with open(file_path, "r") as f:
            config.X_POS = int(f.readline().strip())
            config.Y_POS = int(f.readline().strip())
            config.WIDTH = int(f.readline().strip())
            config.HEIGHT = int(f.readline().strip())
            FPS = int(f.readline().strip())

def write_to_config():
    file_path = "./files/config.txt"
    lock = FileLock(file_path + ".lock")
    with lock:
        with open(file_path, "w") as f:
            f.write(str(config.X_POS))
            f.write("\n")
            f.write(str(config.Y_POS))
            f.write("\n")
            f.write(str(config.WIDTH))
            f.write("\n")
            f.write(str(config.HEIGHT))
            f.write("\n")
            f.write(str(config.FPS))


def draw_board():
    for i in range(32):
        col = i % 4 #0 1 2 3
        row = i // 4 #0 0 0 0

        if row % 2 == 0:
            pygame.draw.rect(screen, (189,218,231),
            [(6 * config.PIECE_WIDTH) - (col * 2 * config.PIECE_WIDTH), row * config.PIECE_HEIGHT, config.PIECE_WIDTH, config.PIECE_HEIGHT])
        else:
            pygame.draw.rect(screen, (189,218,231),
            [(7 * config.PIECE_WIDTH) - (col * 2 * config.PIECE_WIDTH), row * config.PIECE_HEIGHT, config.PIECE_WIDTH, config.PIECE_HEIGHT])
    pygame.draw.rect(screen, 'white', [8*config.PIECE_WIDTH, 0, 30, config.HEIGHT])
    pygame.draw.rect(screen, 'white', [0, 8*config.PIECE_HEIGHT, config.WIDTH, 30])

    for i in range(8):
        screen.blit(font.render(str(8 - i), True, 'black'), (8*config.PIECE_WIDTH + 5, i * config.PIECE_HEIGHT + (config.PIECE_HEIGHT / 2) - 5))
        screen.blit(font.render(chr(i + ord('a')), True, 'black'), 
                    (i * config.PIECE_WIDTH + (config.PIECE_WIDTH / 2) - 5, 8*config.PIECE_HEIGHT + 5))
    
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, config.PIECE_HEIGHT * i), (8*config.PIECE_WIDTH, config.PIECE_HEIGHT * i), 2)
        pygame.draw.line(screen, 'black', (config.PIECE_WIDTH * i, 0), (config.PIECE_WIDTH * i, 8*config.PIECE_HEIGHT), 2)


def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(config.w_pawn, (white_locations[i][0] * config.PIECE_WIDTH + 10, white_locations[i][1] * config.PIECE_HEIGHT + 10))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * config.PIECE_WIDTH + 10, white_locations[i][1] * config.PIECE_HEIGHT + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [white_locations[i][0] * config.PIECE_WIDTH + 1, white_locations[i][1] * config.PIECE_HEIGHT + 1, config.PIECE_WIDTH, config.PIECE_HEIGHT], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(config.b_pawn, (black_locations[i][0] * config.PIECE_WIDTH + 10, black_locations[i][1] * config.PIECE_HEIGHT + 10))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * config.PIECE_WIDTH + 10, black_locations[i][1] * config.PIECE_HEIGHT + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * config.PIECE_WIDTH + 1, black_locations[i][1] * config.PIECE_HEIGHT + 1, config.PIECE_WIDTH, config.PIECE_HEIGHT], 2)

def draw_evaluations():
    pieces = []
    boja_slova = []
    for x in evaluations:
        move = x.split("   ")[0]
        e = x.split("   ")[1]
        x1 = (ord(move[0]) - ord('a'))
        y1 = 7 - (int(move[1]) - 1)
        x2 = (ord(move[2]) - ord('a'))
        y2 = 7 - (int(move[3]) - 1)
        is_black_piece = (x2 + y2) % 2 != 0
        has_figure = True if (x2,y2) in white_locations or (x2,y2) in black_locations else False
        boja = "white"
        if is_black_piece and not has_figure:
            boja = "white"
        elif not is_black_piece and not has_figure:
            boja = "black"
        elif not is_black_piece and has_figure:
            boja = (255, 127, 39)
        else:
            boja = (255, 0, 166)
        boja_slova.append(boja)
        pieces.append((x1,y1,x2,y2,e))
    big_rect_width = config.PIECE_WIDTH / 1.5
    big_rect_height = config.PIECE_HEIGHT / 2
    boje = ["orange", "purple", "yellow", "red", "green"]
    pomeraj = [(0, config.PIECE_HEIGHT - 20, 0, config.PIECE_HEIGHT - big_rect_height),
               (0, 0, 0, 0),
               (config.PIECE_WIDTH - 20, 0, config.PIECE_WIDTH - big_rect_width, 0),
               (config.PIECE_WIDTH - 20, config.PIECE_HEIGHT - 20, config.PIECE_WIDTH - big_rect_width, config.PIECE_HEIGHT - big_rect_height),
               ((config.PIECE_WIDTH / 2) - 10, (config.PIECE_HEIGHT / 2) - 10, (config.PIECE_WIDTH / 2) - (big_rect_width / 2), (config.PIECE_HEIGHT / 2) - (big_rect_height / 2))]
    font = pygame.font.Font("freesansbold.ttf", int(big_rect_height / 2))    
    for i in range(len(evaluations)):
        pygame.draw.rect(screen, boje[i], [pieces[i][0] * config.PIECE_WIDTH + pomeraj[i][0], pieces[i][1] * config.PIECE_HEIGHT + pomeraj[i][1], 20, 20], 5)
        pygame.draw.rect(screen, boje[i], [pieces[i][2] * config.PIECE_WIDTH + pomeraj[i][2], pieces[i][3] * config.PIECE_HEIGHT + pomeraj[i][3], big_rect_width, big_rect_height], 5)
        screen.blit(font.render(pieces[i][4],True,boja_slova[i]), (pieces[i][2] * config.PIECE_WIDTH + pomeraj[i][2] + 3, pieces[i][3] * config.PIECE_HEIGHT + pomeraj[i][3] + 10))

def on_click(x, y, button, pressed):
    if pressed:
        config.X_POS = x
        config.Y_POS = y
        write_to_config()
    else:
        config.WIDTH = x - config.X_POS
        config.HEIGHT = y - config.Y_POS
        write_to_config()
        config.PIECE_WIDTH = (config.WIDTH - 30) / 8
        config.PIECE_HEIGHT = (config.HEIGHT - 30) / 8
        config.load_assets()
        return False  

with mouse.Listener(on_click=on_click) as listener:
    listener.join()

white_pieces=white_locations=black_pieces=black_locations = []
evaluations:List[str] = []
ev = ""
fen = ""
selection = 100
turn_step = 0
from_coords = ()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (config.X_POS,config.Y_POS)
pygame.init()

screen = pygame.display.set_mode([config.WIDTH, config.HEIGHT])
pygame.display.set_caption("Chess")
font = pygame.font.Font("freesansbold.ttf", 20)
big_font = pygame.font.Font("freesansbold.ttf", 50)
timer = pygame.time.Clock()


white_images = [config.w_pawn, config.w_queen, config.w_king, config.w_knight, config.w_rook, config.w_bishop]
black_images = [config.b_pawn, config.b_queen, config.b_king, config.b_knight, config.b_rook, config.b_bishop]


piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

hwnd = pygame.display.get_wm_info()["window"]
run = True
while run:
    read_config()
    timer.tick(config.FPS)
    screen.fill(((18,100,254)))
    read_file()

    draw_board()
    draw_pieces()
    draw_evaluations()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEOEXPOSE:
            prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
            paramFlags = (1, "hwnd"), (2, "lprect")

            GetWindowRect = prototype(("GetWindowRect", windll.user32), paramFlags)
            rect = GetWindowRect(hwnd)
            config.X_POS = rect.left
            config.Y_POS = rect.top
            write_to_config()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_cord = int(event.pos[0] // config.PIECE_WIDTH)
            y_cord = int(event.pos[1] // config.PIECE_HEIGHT)

            click_coords = (x_cord, y_cord)
            if turn_step <= 1:
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                        from_coords = white_locations[selection]
                if click_coords != from_coords and selection != 100:
                    print(from_coords, click_coords)
                    write_to_file(from_coords, click_coords)
                    turn_step = 2
                    selection = 100
                    from_coords = ()
            elif turn_step >= 2:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                        from_coords = black_locations[selection]
                if click_coords != from_coords and selection != 100:
                    print(from_coords, click_coords)
                    write_to_file(from_coords, click_coords)
                    turn_step = 0
                    selection = 100
                    from_coords = ()
    pygame.display.flip()
pygame.quit()