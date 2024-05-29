import pygame

input_path = "./files/in/GUIINPUT.txt"
output_path = "./files/out/GUIOUTPUT.txt"

X_POS = 200
Y_POS = 200
WIDTH = 830
HEIGHT = 830
PIECE_WIDTH = 100
PIECE_HEIGHT = 100
FPS = 30

b_bishop=b_king=b_knight=b_pawn=b_queen=b_rook=w_bishop=w_king=w_knight=w_pawn=w_queen=w_rook=None
def load_assets():
    global b_bishop, b_king, b_knight, b_pawn,b_queen, b_rook
    global w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook
    scale_x = PIECE_WIDTH / 100
    scale_y = PIECE_HEIGHT / 100

    b_bishop = pygame.image.load('assets/b_bishop_png_512px.png')
    b_bishop = pygame.transform.scale(b_bishop, (80 * scale_x,80 * scale_y))

    b_king = pygame.image.load('assets/b_king_png_512px.png')
    b_king = pygame.transform.scale(b_king, (80 * scale_x,80 * scale_y))

    b_knight = pygame.image.load('assets/b_knight_png_512px.png')
    b_knight = pygame.transform.scale(b_knight, (80 * scale_x,80 * scale_y))

    b_pawn = pygame.image.load('assets/b_pawn_png_512px.png')
    b_pawn = pygame.transform.scale(b_pawn, (80 * scale_x,80 * scale_y))

    b_queen = pygame.image.load('assets/b_queen_png_512px.png')
    b_queen = pygame.transform.scale(b_queen, (80 * scale_x,80 * scale_y))

    b_rook = pygame.image.load('assets/b_rook_png_512px.png')
    b_rook = pygame.transform.scale(b_rook, (80 * scale_x,80 * scale_y))
    #---

    w_bishop = pygame.image.load('assets/w_bishop_png_512px.png')
    w_bishop = pygame.transform.scale(w_bishop, (80 * scale_x,80 * scale_y))

    w_king = pygame.image.load('assets/w_king_png_512px.png')
    w_king = pygame.transform.scale(w_king, (80 * scale_x,80 * scale_y))

    w_knight = pygame.image.load('assets/w_knight_png_512px.png')
    w_knight = pygame.transform.scale(w_knight, (80 * scale_x,80 * scale_y))

    w_pawn = pygame.image.load('assets/w_pawn_png_512px.png')
    w_pawn = pygame.transform.scale(w_pawn, (80 * scale_x,80 * scale_y))

    w_queen = pygame.image.load('assets/w_queen_png_512px.png')
    w_queen = pygame.transform.scale(w_queen, (80 * scale_x,80 * scale_y))

    w_rook = pygame.image.load('assets/w_rook_png_512px.png')
    w_rook = pygame.transform.scale(w_rook, (80 * scale_x,80 * scale_y))