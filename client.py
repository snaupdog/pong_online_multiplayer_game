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
BALL_RADIUS = 8

BUFFER_SIZE = 4000

PINKISH = (250, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
leftscore = 0
rightscore = 0
won = False
scorefont = pygame.font.SysFont("comicsans", 50)
winscore = 2
# SERVER_IP = "10.14.143.190"
SERVER_IP = "localhost"
PORT = 8000
GAME_SPEED = 60

pwidth, pheight = 20, 100

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Apparently")


bong_img = pygame.image.load(os.path.join("assets", "bong.png"))
bong = pygame.transform.scale(bong_img, (150, 150))

bogn_img = pygame.image.load(os.path.join("assets", "bogn.png"))
bogn = pygame.transform.scale(bogn_img, (150, 150))

bolll_img = pygame.image.load(os.path.join("assets", "balll.png"))
bolll = pygame.transform.scale(bolll_img, (330, 330))


def draw_paddles(x, y, p, info):
    if p == 1:
        pygame.draw.rect(win, (100, 100, 100), (x, y, pwidth, pheight))
        win.blit(bong, (x - 45, y - 35))
    if p == 2:
        pygame.draw.rect(win, (200, 200, 200), (x, y, pwidth, pheight))
        win.blit(bogn, (x - 112, y - 35))


def draw_ball(x, y):
    pygame.draw.circle(win, BLACK, [x, y], BALL_RADIUS)
    win.blit(bolll, (x - 123, y - 120))


def update_score(x):
    global leftscore, rightscore, won, winscore
    if x <= 0:
        rightscore += 1
        hitSound.play()

    elif x >= SCREEN_WIDTH:
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


# bg_img = pygame.image.load('assets/bg.png')


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((SERVER_IP, PORT))

# hitSound = pygame.mixer.Sound("hit.mp3")
hitSound = pygame.mixer.Sound("hit1.wav")

clock = pygame.time.Clock()


def main():
    game_finished = False
    key_up = False
    key_down = False

    # pygame.mixer.music.play(-1)
    while game_finished == False:
        clock.tick(GAME_SPEED)

        # waits for other client here
        info = recieve_data()

        win.fill(PINKISH)
        # win.blit(bg_img, (0, 0))

        draw_paddles(30, info[0], 1, info)
        draw_paddles(SCREEN_WIDTH - 30 - pwidth, info[1], 2, info)
        draw_ball(info[2], info[3])

        update_score(info[2])
        pygame.display.update()

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


# main()

main()
