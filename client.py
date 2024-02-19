import os
import pickle
import socket
import time

import pygame
from pygame import mixer
from pygame.locals import *

from gameobj import Game

mixer.init()
mixer.music.load('assets/bg_music.wav')

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 650
BALL_RADIUS = 5


PINKISH = (250, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


pwidth, pheight = 20, 100

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong Apparently')


bong_img = pygame.image.load(os.path.join('assets', 'bong.png'))
bong = pygame.transform.scale(bong_img, (150, 150))

bogn_img = pygame.image.load(os.path.join('assets', 'bogn.png'))
bogn = pygame.transform.scale(bogn_img, (150, 150))

bolll_img = pygame.image.load(os.path.join('assets', 'balll.png'))
bolll = pygame.transform.scale(bolll_img, (330, 330))


def draw_paddles(x, y, p, info):
    if p == 1:
        pygame.draw.rect(win, (100, 100, 100), (x, y, pwidth, pheight))
        win.blit(bong, (x - 45, y - 35))
    if p == 2:
        pygame.draw.rect(win, (200, 200, 200), (x, y, pwidth, pheight))
        win.blit(bogn, (x - 110, y - 35))


def draw_ball(x, y):
    pygame.draw.circle(win, BLACK, [x, y], BALL_RADIUS)


def recieve_data():
    # this should ideally return a game object
    data = clientsocket.recv(1024)
    data = pickle.loads(data)
    return data


bg_img = pygame.image.load('assets/bg.png')


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8000))

scorefont = pygame.font.SysFont('comicsans', 50)
text = scorefont.render('STARTING SOON', 1, WHITE)


def main():
    Starting_screen = True
    game_finished = False
    key_up = False
    key_down = False

    mixer.music.play()
    while game_finished == False:
        # waits for other client here
        info = recieve_data()

        # win.fill(PINKISH)
        win.blit(bg_img, (0, 0))

        draw_paddles(10, info.y1, 1, info)
        draw_paddles(SCREEN_WIDTH - 10 - pwidth, info.y2, 2, info)

        draw_ball(info.bx, info.by)

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
        data_arr = pickle.dumps(arr)
        clientsocket.send(data_arr)
        Starting_screen = False

        pygame.display.update()


# main()

main()
