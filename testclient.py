import os
import pickle
import socket
import time

import pygame

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


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8000))


class Game:
    def __init__(self, y1, y2, by, bx, sc1, sc2):
        self.y1 = y1
        self.y2 = y2

        self.by = by
        self.bx = bx

        self.sc1 = 0
        self.sc2 = 0


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


def display():
    game_finished = False
    key_up = False
    key_down = False
    while game_finished == False:
        info = recieve_data()
        # recieve game object and update ball position and bat position on screen
        win.fill(PINKISH)
        draw_paddles(10, info.y1, 1, info)
        draw_paddles(SCREEN_WIDTH - 10 - pwidth, info.y2, 2, info)
        draw_ball(info.bx, info.by)

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
        data_arr = pickle.dumps(arr)
        # send key up and key down to server for processing
        clientsocket.send(data_arr)

    # info = [player_1_y, player_2_y, ball_y, ball_x, score_1, score_2]


display()
