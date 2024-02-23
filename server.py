import random
import socket
import ssl
import struct
import time

import pygame

from gameobj import Game

BUFFER_SIZE = 5000


SERVER_IP = "10.1.18.95"
# SERVER_IP = "localhost"
# PORT = 8000


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (SERVER_IP, 12345)
server_socket.bind(server_address)


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

server_socket = ssl_context.wrap_socket(server_socket, server_side=True)

server_socket.listen(2)

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

    dataaa.update_paddle(player_1, player_2)
    dataaa.collisions()


def waiting_for_connections():
    while len(connection) < 2:
        conn, addr = server_socket.accept()
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

    response_data = struct.pack("!4f", *int_data)

    connection[0].send(response_data)
    connection[1].send(response_data)

    # receives and array with info [key_up,key_down(boolean)]
    player1, player2 = recieve_information()

    process_positions(player1, player2)
