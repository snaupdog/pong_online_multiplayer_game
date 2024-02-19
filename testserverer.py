import pickle
import random
import socket

import pygame

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8000))
serversocket.listen(2)

connection = []
ball_y_speed = 4
ball_x_speed = 4

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 650
BALL_RADIUS = 5


class Game:
    def __init__(self, y1, y2, by, bx, sc1, sc2):
        self.y1 = y1
        self.y2 = y2
        self.by = by
        self.bx = bx
        self.sc1 = 0
        self.sc2 = 0

        self.check = False
        self.paddle_velocity = 4
        self.paddle_width = 20
        self.paddle_height = 100
        self.ball_radius = 5

    def update_paddle(self, player_1, player_2):

        if player_1[0] == True:
            self.y1 -= 1
        else:
            self.y1 = self.y1
        if player_1[1] == True:
            self.y1 += 1
        else:
            self.y1 = self.y1

        if player_2[0] == True:
            self.y2 -= 1
        else:
            self.y2 = self.y2
        if player_2[1] == True:
            self.y2 += 1
        else:
            self.y2 = self.y2

class Ball:
    MAXVEL = 8
    COLOR = (120,210,012)   # change to pinkish later

    def __init__(self, x, y, radius):
        self.x = self.origx = x
        self.y = self.origy = y
        self.radius = radius
        self.x_vel = self.MAXVEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.origx
        self.y = self.origy
        self.y_vel = 0
        self.x_vel *= -1

dataaa = Game(200, 200, 400, 400, 0, 0)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS)


def process_positions(player_1, player_2):

    global ball_y_speed, ball_x_speed
    dataaa.update_paddle(player_1, player_2)

    print(dataaa.bx)
    print(dataaa.by)


def waiting_for_connections():
    while len(connection) < 2:
        conn, addr = serversocket.accept()
        connection.append(conn)


def recieve_information():
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))

    return player_1_info, player_2_info


print(dataaa.check)


while True:
    waiting_for_connections()
    # first time sends default original values in array

    data_arr = pickle.dumps(dataaa)
    ball_data = pickle.dumps(ball)
    data = [data_arr,ball_data]
    connection[0].send(data_arr)
    connection[1].send(data_arr)

    connection[0].send(ball_data)
    connection[1].send(ball_data)
    # receives and array with info [key_up,key_down(boolean)]
    player1, player2 = recieve_information()

    process_positions(player1, player2)
