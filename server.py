import random
import socket
import struct
import time

import pygame

from gameobj import Game

from constants import * 


connection = []

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((SERVER_IP, PORT))
serversocket.listen(2)

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
    player_no=1

    while len(connection) < 2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(f" player {player_no} connected at {addr} ")
        player_no+=1



    # msg = [1]
    # responsemsg = struct.pack("!1i",*msg)
    # connection[0].send(responsemsg)

    # msg2 = [2]
    # responsemsg = struct.pack("!1i",*msg2)
    # connection[1].send(responsemsg)

    



def recieve_information():
    recievefrom1 = connection[0].recv(BUFFER_SIZE)
    rcv = connection[1].recv(BUFFER_SIZE)
    player_1_info = struct.unpack("!2?", recievefrom1)
    player_2_info = struct.unpack("!2?", rcv)

    return player_1_info, player_2_info


waiting_for_connections()

# connection[0].send("player 1")
# connection[1].send("Plyaer 2")


while True:
    # first time sends default original values in array
    int_data = [
        dataaa.y1,
        dataaa.y2,
        dataaa.bx,
        dataaa.by,
    ]

    response_data = struct.pack("!4f", *int_data)

    try : 
        connection[0].send(response_data)
        connection[1].send(response_data)

    # receives and array with info [key_up,key_down(boolean)]
        player1, player2 = recieve_information()
        process_positions(player1, player2)

    except:
        break
try:
    connection[0].close()
    connection[1].close()
    serversocket.close()
    print("all sockets closed properly")
except:
    print("error closing sockets")
