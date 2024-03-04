import os
import socket
import struct
import pygame
import time
from pygame import mixer
from pygame.locals import *
from gameobj import Game
from constants import * 
from constants import BLACK,PINKISH,GAME_SPEED




def draw_paddles(x, y, p, info):
    if p == 1:
        pygame.draw.rect(win, PINKISH, (x, y, pwidth, pheight))
        win.blit(bong, (x - 45, y - 35))
    if p == 2:
        pygame.draw.rect(win,PINKISH, (x, y, pwidth, pheight))
        win.blit(bogn, (x - 112, y - 35))


def draw_ball(x, y):
    pygame.draw.circle(win, BLACK, [x, y], BALL_RADIUS)
    win.blit(bolll, (x - 123, y - 120))


def update_score(x):
    global leftscore, rightscore, won, winscore
    if x <= 5:
        rightscore += 1
        hitSound.play()

    elif x >= SCREEN_WIDTH-5:
        leftscore += 1
        hitSound.play()

    left_score_text = scorefont.render(str(leftscore), True, WHITE)
    right_score_text = scorefont.render(str(rightscore), True, WHITE)

    win.blit(
        left_score_text,
        (
            SCREEN_WIDTH // 2 - 24 * left_score_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - left_score_text.get_height() // 2,
        ),
    )
    win.blit(
        right_score_text,
        (
            SCREEN_WIDTH // 2 + 20 * right_score_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - right_score_text.get_height() // 2,
        ),
    )

    if leftscore >= winscore:
        won = True
        wintext = "Left Player Won!"
    elif rightscore >= winscore:
        won = True
        wintext = "Right Player Won!"

    if won:
        text = scorefont.render(wintext, 1, WHITE)
        win.blit(
            text,
            (
                SCREEN_WIDTH // 2 - text.get_width() // 2,
                SCREEN_HEIGHT // 2 - text.get_height() // 2,
            ),
        )
        pygame.display.update()
        pygame.time.delay(2000)


def recieve_data():
    # this should ideally return a game object
    int_data = clientsocket.recv(BUFFER_SIZE)

    data = struct.unpack("!4f", int_data)
    return data

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((SERVER_IP, PORT))

pygame.init()

bg_img = pygame.image.load('assets/bg.png')
hitSound = pygame.mixer.Sound("assets/hit.wav")

clock = pygame.time.Clock()

scorefont = pygame.font.SysFont("comicsans", 50)
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Apparently")

bong_img = pygame.image.load(os.path.join("assets", "bong.png"))
bong = pygame.transform.scale(bong_img, (150, 150))

bogn_img = pygame.image.load(os.path.join("assets", "bogn.png"))
bogn = pygame.transform.scale(bogn_img, (150, 150))

bolll_img = pygame.image.load(os.path.join("assets", "balll.png"))
bolll = pygame.transform.scale(bolll_img, (330, 330))

def run_game():
    game_finished = False
    key_up = False
    key_down = False
    startscreen =True


    blah =True
    while game_finished == False:

        if startscreen:
            Blah = True
            while Blah:
                win.fill(PINKISH)

                # win.blit(title, (200, 100))

                text = scorefont.render("SPACECECE TO PLEY", 1, WHITE)
                win.blit(
                    text,
                    (
                        200,
                        400
                    ),
                )

                text = scorefont.render("BONGA", 1, BLACK)
                win.blit(
                    text,
                    (
                        200,
                        200
                    ),
                )

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            Blah  = False
                            startscreen = False

                



        # if blah:
        #     player_id = clientsocket.recv(BUFFER_SIZE)
        #     player_id_data = struct.unpack("!1i", player_id)
        #     print(f"this is player {player_id_data[0]}")
        #     blah = False

        clock.tick(GAME_SPEED)
        # waits for other client here
        win.blit(bg_img, (0, 0))
        try : 
            info = recieve_data()
        except: 
            break;


        draw_paddles(30, info[0], 1, info)
        draw_paddles(SCREEN_WIDTH - 30 - pwidth, info[1], 2, info)
        draw_ball(info[2], info[3])

        update_score(info[2])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_finished = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key_up = True
                if event.key == pygame.K_DOWN:
                    key_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    key_up = False
                if event.key == pygame.K_DOWN:
                    key_down = False

        arr = [key_up, key_down]
        data_arr = struct.pack("!2?", *arr)
        try : 
            clientsocket.send(data_arr)
        except:
            break;

    clientsocket.close()
    print("game ended")



# main()

run_game()
