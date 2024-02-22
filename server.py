import random
import socket
import struct
import time

import pygame

from gameobj import Game

# SERVER_IP = "10.14.143.190"
SERVER_IP = "localhost"
PORT = 8000

BUFFER_SIZE = 4000
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((SERVER_IP, PORT))
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
)


def process_positions(player_1, player_2):

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


while True:
    waiting_for_connections()
    # first time sends default original values in array
    int_data = [
        dataaa.y1,
        dataaa.y2,
        dataaa.bx,
        dataaa.by,
    ]

    response_data = struct.pack("!4f", *int_data)

    connection[0].send(response_data)
    connection[1].send(response_data)

    # receives and array with info [key_up,key_down(boolean)]
    player1, player2 = recieve_information()

    process_positions(player1, player2)
