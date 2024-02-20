import pickle
import random
import socket
import time

import pygame

from gameobj import Game

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('10.1.18.2', 8000))
serversocket.listen(2)

connection = []

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 650
BALL_RADIUS = 5

pwidth, pheight = 20, 100


dataaa = Game(
    SCREEN_HEIGHT // 2 - pheight // 2,
    SCREEN_HEIGHT // 2 - pheight // 2,
    SCREEN_HEIGHT // 2,
    SCREEN_WIDTH // 2,
    0,
    0,
)


def process_positions(player_1, player_2):

    global ball_y_speed, ball_x_speed
    dataaa.update_paddle(player_1, player_2)
    dataaa.collisions()


def waiting_for_connections():
    while len(connection) < 2:
        conn, addr = serversocket.accept()
        connection.append(conn)


def recieve_information():
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))

    return player_1_info, player_2_info


last_print_time = time.time()

while True:
    waiting_for_connections()
    # first time sends default original values in array
    tuppyp = (
        dataaa.y1,
        dataaa.y2,
        dataaa.bx,
        dataaa.by,
        dataaa.sc1,
        dataaa.sc2,
    )

    data_arr = pickle.dumps(tuppyp)

    connection[0].send(data_arr)
    connection[1].send(data_arr)

    # receives and array with info [key_up,key_down(boolean)]
    player1, player2 = recieve_information()

    process_positions(player1, player2)

    # Print "hello" every 5 seconds
    current_time = time.time()
    if current_time - last_print_time >= 5:
        print(
            f'this is player 1 : - {dataaa.sc1}\nthis is player 2 : - {dataaa.sc2}'
        )
        last_print_time = current_time
