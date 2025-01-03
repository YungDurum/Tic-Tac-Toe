'''
Hi Sogyo, this is my implementation for the game of TicTacToe

Its a two player game but I also implemented the mode of playing solo against a smart agent. 
I must say the smart agent is not that smart yet, but its a work in progress. The smart agent was trained by using Q-Learning (reinforcement learning).

For this game I used pygame, which was new to me. 
'''

import pygame
from tic_tac_toe_helper import TicTacToe, AIplayer
from time import sleep, time

# Initialize game and create instance of TicTacToe
pygame.init()
game = TicTacToe()

# Define colors and Font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)
PURPLE = (191,62,255)
FONT = "Press_Start_2P/PressStart2P-Regular.ttf"

# Screen size
WIDTH = 600
HEIGHT = 600
GRID_WIDTH = 400
GRID_HEIGHT = 400
CELL_SIZE = 19

#Functions for creating pygame objects.
def drawing_a_grid_in_the_center_off_the_screen(cell_size=80, board=[None for x in range(3) for y in range(3)]):
    # Calculate grid dimensions
    width = len(board[0])
    height = len(board)

    grid_width = width * cell_size
    grid_height = height * cell_size
    
    # Calculate offsets to center the grid
    offset_x = (screen.get_width() - grid_width) // 2
    offset_y = (screen.get_height() - grid_height) // 2

    # Important variable for checking what square has been clicked
    square_positions = [[None for _ in range(3)] for _ in range(3)]

    for i in range(width):
        for j in range(height):
            rect = pygame.Rect(offset_x + j * cell_size, offset_y + i * cell_size, cell_size, cell_size)
            square_positions[i][j] = rect
            if board[i][j] == "X":
                font = pygame.font.Font(FONT,int(cell_size/2))
                displaytext = font.render("X", False, YELLOW)
                textRect = displaytext.get_rect()
                textRect.center = rect.center
                screen.blit(displaytext, textRect)
            elif board[i][j] == "O":
                font = pygame.font.Font(FONT,int(cell_size/2))
                displaytext = font.render("O", False, PURPLE)
                textRect = displaytext.get_rect()
                textRect.center = rect.center
                screen.blit(displaytext, textRect)
            pygame.draw.rect(screen, WHITE, rect, 1)
    
    return square_positions

def text_in_screen_font_PRESS_Start_2p(text, size, color, left, top):
    font = pygame.font.Font(FONT,size)
    displaytext = font.render(text, False, color)
    textRect = displaytext.get_rect()
    textRect.center = (left, top)
    screen.blit(displaytext, textRect)
    return textRect

def box_object(text, size, color_text, color_box, left, top, width, height):
    font = pygame.font.Font(FONT,size)

    button = pygame.Rect(left, top, width,height)
    displaytext = font.render(text, False, color_text)
    textRect = displaytext.get_rect()
    textRect.center = button.center
    pygame.draw.rect(screen, color_box, button)
    screen.blit(displaytext, textRect)

    # returns buttonobject for interactions
    return button



# Set variables for game interaction
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start = False # Menu screen or not
running = True
player = 0 # flag for how many players are playing
progress_flag = 0 # Flags if game is in progress or not
click_flag = False #Flags if interaction with click has been made
move_flag = 0 #Flags if a move has been made

while running:
    click, _, _ = pygame.mouse.get_pressed()
    if click:
        mouse = pygame.mouse.get_pos()
    
    if start == False:
        text_in_screen_font_PRESS_Start_2p("_X",70,YELLOW,4.25*WIDTH/12,160)
        text_in_screen_font_PRESS_Start_2p("O_",70,PURPLE,7.75*WIDTH/12,160)
        text_in_screen_font_PRESS_Start_2p("THE GAME",75,WHITE,WIDTH/2,HEIGHT/2)
        subtitle = text_in_screen_font_PRESS_Start_2p("click to start",20,WHITE,WIDTH/2,HEIGHT/2+75)

        if click == 1:
            if subtitle.collidepoint(mouse):
                start = True  
                Iterations = 15
                for x in range(Iterations):
                    screen.fill(BLACK)
                    text_in_screen_font_PRESS_Start_2p("_X",70,YELLOW,4.25*WIDTH/12,160)
                    text_in_screen_font_PRESS_Start_2p("O_",70,PURPLE,7.75*WIDTH/12,160)

                    # Animation title parameters
                    start_size = 75
                    end_size = 45
                    start_place = HEIGHT/2
                    end_place = 50

                    text_in_screen_font_PRESS_Start_2p("THE GAME", int(start_size-(start_size-end_size)*(x/Iterations)), WHITE, WIDTH / 2, int((start_place-(start_place-end_place)*x/Iterations)))
                    sleep(0.1)
                    pygame.display.flip()

    # Menu screen choose one or two players.
    elif start and player == 0:
        Oneplayer_button = box_object("One Player", 10, BLACK, WHITE, 1.5*(WIDTH / 8), (HEIGHT / 2)-40, WIDTH / 4, 50)
        Twoplayer_button = box_object("Two Player",10, BLACK, WHITE ,4.5*(WIDTH / 8), (HEIGHT / 2)-40, WIDTH / 4, 50)

        if click == 1 and click_flag == False:
                click_flag == True
                if Oneplayer_button.collidepoint(mouse):
                    player = 1
                    sleep(0.2)
                    continue
                elif Twoplayer_button.collidepoint(mouse):
                    player = 2
                    sleep(0.2)
                    continue

    elif player:
        """
        From here the TicTacToe game is setup. This first part will be the same for one player games and two player games. 
        This mostly comes down to the rules of the game that will remain similar and does not depend on what mode is selected. The chronology of the statements and lines is important in this section, because drawing can override eachother.

        1. First the things are drawn that are always vissible. So the grid the exit button and the score
        2. A termination function is activated when the exit button is clicked
        3. When a move is made (move flag is 1). The move statement will check be activated. 
            First there will be checked if the game has ended. 
                In case there is a winner:
                    The winner will be drawn, and the score will be updated.
                In case there is no winner
                    A draw will be drawn.
                The game will go back to the beginning state (progress_flag = zero)
            In case there is no end and their are two player playing:
                The next player will be drawn on the screen.

        This next part depends on if their is only one player or two players.
            When one player is selected:
                It will be checked if it is the AI-turn 
                    The move will be made by the AI. 
                If not:
                    The move will be made by the player.

            If two player is selected:
                Every move will be made by the player. The click_flag makes sure only one move will be made per click.
        """
        #Draw the up to date grid and the exit button.
        positions_in_grid = drawing_a_grid_in_the_center_off_the_screen(cell_size=80, board=game.state)
        exit_button = text_in_screen_font_PRESS_Start_2p("Exit",10,WHITE,10* WIDTH/12,10*HEIGHT/12)
        text_in_screen_font_PRESS_Start_2p(str(game.score["X"]), 30, YELLOW, WIDTH/12, 125)
        text_in_screen_font_PRESS_Start_2p(str(game.score["O"]), 30, PURPLE, 11* WIDTH/12, 125)
        
        # Exit button check
        if click and exit_button.collidepoint(mouse) and click_flag == False:
            screen.fill(BLACK)
            player = 0
            progress_flag = 0
            click_flag = True
            start = False
            game = TicTacToe()
            continue

        #  If a move has been made this will check if a winner has been found.
        if move_flag:
            move_flag = 0
            box_object("One Player", 10, BLACK, BLACK, WIDTH/4, 60, WIDTH /2, 100) 
            if game.end(game.state) and progress_flag == 1:
                progress_flag = 0
                who = game.winner(game.state)
                screen.fill(BLACK)
                if who == "X":
                    text_in_screen_font_PRESS_Start_2p("WINNER", 30, WHITE, WIDTH/2, 70)
                    text_in_screen_font_PRESS_Start_2p("X", 40, YELLOW, WIDTH/2, 125)
                elif who == "O":
                    text_in_screen_font_PRESS_Start_2p("WINNER", 30, WHITE, WIDTH/2, 70)
                    text_in_screen_font_PRESS_Start_2p("O", 40, PURPLE, WIDTH/2, 125)
                else:
                    text_in_screen_font_PRESS_Start_2p("DRAW", 30, WHITE, WIDTH/2, 115)
                continue
            
            # In case a move is made and there is no winner. In the screen it shows whos turn it is.
            if player == 2:
                text_in_screen_font_PRESS_Start_2p(str(game.whoplays())+" TURN", 20, WHITE, WIDTH/2, 2.5*HEIGHT/12)


        # The board and screen will be cleaned, and the amound of game that are played will be updated.
        if progress_flag == 0:
            if click == 1 and click_flag == False:
                progress_flag = 1
                click_flag = True
                if game.games_played != 0:
                    game.next_round()    
                
                game.games_played += 1
                screen.fill(BLACK)        
                if player == 2:
                    text_in_screen_font_PRESS_Start_2p(str(game.whoplays())+" TURN", 20, WHITE, WIDTH/2, 2.5*HEIGHT/12)
        
        

        # one player mode
        elif player == 1 and progress_flag == 1:
            # if AI player turn
            if game.whoplays() == "O" and click_flag == False:
                move_flag = 1
                best_action = AIplayer.choose_action(game.state, False)
                game.move(best_action)
                text_in_screen_font_PRESS_Start_2p("....", 20, WHITE, WIDTH/2, 2.9*HEIGHT/12)
                pygame.display.flip()
                sleep(1)

            else:
                if click == 1 and click_flag == False:
                    click_flag = True
                    for row in range(len(positions_in_grid)):
                        for column in range(len(positions_in_grid[row])):
                            if positions_in_grid[row][column].collidepoint(mouse):
                                move_flag = 1
                                game.move((row,column))
        
                       
        # Two player mode
        elif player == 2 and progress_flag == 1:
                if click == 1 and click_flag == False:
                    click_flag = True
                    for row in range(len(positions_in_grid)):
                        for column in range(len(positions_in_grid[row])):
                            if positions_in_grid[row][column].collidepoint(mouse):
                                move_flag=1
                                game.move((row,column))
                                break
               
        
    # Check if there has already been clicked so not mutiple clicks happen at the same time.
    if click == 0: 
        click_flag = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state and draw to the screen
    pygame.display.flip()