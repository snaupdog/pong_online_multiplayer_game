# Multiplayer Pong Game

This project implements a multiplayer Pong game using sockets and Pygame. The game allows two players to compete against each other in a classic Pong match.

## Features

- Real-time multiplayer Pong game.
- Server-client architecture for handling game state and player communication.
- Pygame for rendering and handling player input.
- Sockets for handling network communication

## Getting Started

<img width="997" alt="Screenshot 2024-03-04 at 2 28 24 PM" src="https://github.com/snaupdog/pong_online_multiplayer_game/assets/116204740/5e13b722-20f9-4415-b03e-96b850757ef5">


### Prerequisites

- Python 3.x
- Pygame library (install using `pip install pygame`)

### Installation



1. **Clone the Repository:**
   
   git clone https://github.com/your-username/pong-multiplayer.git

2. Navigate to project directory:

        cd pong-multiplayer
        pip install pygame

3. Configure Server:

    Open constanst.py and set SERVER_IP and PORT:

        SERVER_IP = "your-server-ip"
        PORT = your-port-number
4. Run Server: 

    python server.py

5. Run Two Client Instances:

    * Open two terminals and run the client in each:
    * python client.py

Notes:
Ensure the server is running before clients connect.
Ensure the clients are connected via server ips address

