import os
import pickle
import socket
import struct
import time

import pygame
from pygame import mixer
from pygame.locals import *

from gameobj import Game

# mixer.init()
# mixer.music.load('assets/bg_music.wav')

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 650
BALL_RADIUS = 10

BUFFER_SIZE = 4000

PINKISH = (250, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
leftscore = 0
rightscore = 0
won = False
scorefont = pygame.font.SysFont("comicsans",50)
winscore = 2
SERVER_IP = "10.14.143.190"
PORT = 8000


pwidth, pheight = 20, 100

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"Left:{leftscore}                                        Right:{rightscore}")


# bong_img = pygame.image.load(os.path.join('assets', 'bong.png'))
# bong = pygame.transform.scale(bong_img, (150, 150))
#
# bogn_img = pygame.image.load(os.path.join('assets', 'bogn.png'))
# bogn = pygame.transform.scale(bogn_img, (150, 150))
#
# bolll_img = pygame.image.load(os.path.join('assets', 'balll.png'))
# bolll = pygame.transform.scale(bolll_img, (330, 330))


def draw_paddles(x, y, p, info):
    if p == 1:
        pygame.draw.rect(win, (100, 100, 100), (x, y, pwidth, pheight))
        # win.blit(bong, (x - 45, y - 35))
    if p == 2:
        pygame.draw.rect(win, (200, 200, 200), (x, y, pwidth, pheight))
        # win.blit(bogn, (x - 105, y - 35))


def draw_ball(x, y):
    pygame.draw.circle(win, BLACK, [x, y], BALL_RADIUS)


def update_score(x):
    global leftscore, rightscore, won,winscore
    if x < 0:
        rightscore += 1

    elif x > SCREEN_WIDTH:
        leftscore += 1


    print(x)
    print(leftscore)
    print(rightscore)

    if leftscore >= winscore:
        won = True
        wintext = "Left Player Won!"
    elif rightscore >= winscore:
        won = True
        wintext = "Right Player Won!"

    if won:
        text = scorefont.render(wintext, 1, WHITE)
        win.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        ball.reset()


    # if x<0:
    #     rightscore+=1
    # elif x>SCREEN_WIDTH:
    #     leftscore+=1
    #
    # if leftscore >= winscore:
    #     won = True
    #     wintext = "Left Player Won!"
    # elif rightscore >= winscore:
    #     won = True
    #     wintext = "Right Player Won!"
    #
    # if won:
    #     text = scorefont.render(wintext, 1, WHITE)
    #     win.blit(text, (SCREEN_WIDTH//2 - text.get_width() //2, SCREEN_HEIGHT//2 - text.get_height()//2))
    #     pygame.display.update()
    #     pygame.time.delay(2000)
    #     ball.reset()
        


def recieve_data():
    # this should ideally return a game object
    int_data = clientsocket.recv(BUFFER_SIZE)

    data = struct.unpack("!4f", int_data)
    return data


# bg_img = pygame.image.load('assets/bg.png')


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((SERVER_IP, PORT))

# hitSound = pygame.mixer.Sound('hit.mp3')


# def checkscoreupdate(prev_ball_x, prev_ball_y, current_ball_x, current_ball_y):
#     if (prev_ball_x != current_ball_x) or (prev_ball_y != current_ball_y):
#         hitSound.play()
#


def main():
    game_finished = False
    key_up = False
    key_down = False
    # prev_count1 = 0
    # prev_count2 = 0

    # pygame.mixer.music.play(-1)
    while game_finished == False:
        # waits for other client here
        info = recieve_data()

        win.fill(PINKISH)
        # win.blit(bg_img, (0, 0))

        draw_paddles(30, info[0], 1, info)
        draw_paddles(SCREEN_WIDTH - 30 - pwidth, info[1], 2, info)

        draw_ball(info[2], info[3])
        update_score(info[2])
        # we can also di if score is updated instead
        # of sending another value
        # checkscoreupdate(info[4], info[5], prev_count1, prev_count2)
        # prev_count1, prev_count2 = info[4], info[5]

        for event in pygame.event.get():
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
        clientsocket.send(data_arr)

        pygame.display.update()


# main()

main()
