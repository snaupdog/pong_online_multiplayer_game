import random
import socket
import struct
import time

import pygame

from gameobj import Game

SERVER_IP = "10.14.142.97"
BUFFER_SIZE = 4098
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((SERVER_IP, 8000))
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
    recievefrom1 = connection[0].recv(BUFFER_SIZE)
    rcv = connection[1].recv(BUFFER_SIZE)
    player_1_info = struct.unpack("!2?", recievefrom1)
    player_2_info = struct.unpack("!2?", rcv)

    return player_1_info, player_2_info


last_print_time = time.time()

while True:
    waiting_for_connections()
    # first time sends default original values in array
    int_data = [
        dataaa.y1,
        dataaa.y2,
        dataaa.bx,
        dataaa.by,
    ]

    print("no - error")
    print(int_data)
    response_data = struct.pack("!4f", *int_data)

    print("error")

    connection[0].send(response_data)
    connection[1].send(response_data)

    # receives and array with info [key_up,key_down(boolean)]
    player1, player2 = recieve_information()

    process_positions(player1, player2)

    # Print "hello" every 5 seconds
    current_time = time.time()
    if current_time - last_print_time >= 5:
        print(f"this is player 1 : - {dataaa.sc1}\nthis is player 2 : - {dataaa.sc2}")
        last_print_time = current_time
