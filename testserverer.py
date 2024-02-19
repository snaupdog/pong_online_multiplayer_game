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


dataaa = Game(200, 200, 400, 400, 0, 0)


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

    connection[0].send(data_arr)
    connection[1].send(data_arr)

    # receives and array with info [key_up,key_down(boolean)]
    player1, player2 = recieve_information()

    process_positions(player1, player2)
