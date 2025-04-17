# 2048 Game with MCP Server for AI Control

This project provides a GUI-based 2048 game with a RESTful API, along with an MCP (Model-Controller-Player) server that allows AI agents to control the game programmatically.

## Components

- **GUI Game**: A visual implementation of the 2048 game built with Tkinter
- **RESTful API**: A Flask-based API to interact with the game
- **MCP Server**: A fastmcp-based server that exposes standardized endpoints for AI control
- **AI Agent**: A simple example AI that plays the game using heuristics

## Requirements

```
Flask>=2.0
fastmcp>=0.2.0
numpy>=1.20.0
requests>=2.25.0
```

## Installation

1. Clone this repository
2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

### Starting the Game and API

To start the 2048 game with its RESTful API:

```
python main.py
```

This will:
- Launch the GUI window showing the 2048 game
- Start the RESTful API server on http://127.0.0.1:5000
- Allow both manual play (via the GUI) and API-based control

### Starting the MCP Server

To start the MCP server for AI control:

```
python mcp_server.py
```

This will:
- Start the MCP server on port 8000
- Connect to the game's API (make sure the game is already running)
- Expose standardized endpoints for AI control

### Running the Example AI Agent

To run the example AI agent that plays the game:

```
python ai_agent.py
```

This will:
- Connect to the MCP server (make sure it's running)
- Begin playing the game autonomously
- Display move decisions and game state in the console

## API Endpoints

### Game RESTful API (Port 5000)

- `GET /status`: Returns the current game state
- `POST /move/{direction}`: Makes a move in the specified direction ('up', 'down', 'left', 'right')
- `POST /reset`: Resets the game to its initial state

### MCP Server API (Port 8000)

- `GET /observations`: Returns the current game state in a standardized format
- `POST /actions`: Sends actions to the game (format: `{"move": "up|down|left|right"}`)
- `GET /rewards`: Returns current rewards for reinforcement learning
- `GET /terminal`: Checks if the game is in a terminal state
- `POST /reset`: Resets the game

## Creating Your Own AI

You can create your own AI agent by:

1. Using the example `ai_agent.py` as a template
2. Implementing your own decision-making logic in the `choose_move` method
3. Using reinforcement learning or more sophisticated algorithms for better results

## License

This project is open-source. Feel free to modify and distribute as needed. 