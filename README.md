# 2048 Game with MCP Server for AI Control

This project provides a GUI-based 2048 game with a RESTful API, along with an MCP (Model-Controller-Player) server that allows AI agents to control the game programmatically.

## Components

- **GUI Game**: A visual implementation of the 2048 game built with Tkinter
- **RESTful API**: A Flask-based API to interact with the game
- **MCP Server**: A fastmcp-based server that exposes standardized endpoints for AI control

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

```json
"mcpServers": {
    "2048_game": {
      "name": "2048 game",
      "type": "stdio",
      "description": "2048 game control mcp",
      "isActive": true,
      "command": "uv",
      "args": [
        "--directory",
        "/directory/to/your/python_script",
        "run",
        "mcp_server.py"
      ]
    }
}
```

This will:
- enable MCP server


## API Endpoints

### Game RESTful API (Port 5000)

- `GET /status`: Returns the current game state
- `POST /move/{direction}`: Makes a move in the specified direction ('up', 'down', 'left', 'right')
- `POST /reset`: Resets the game to its initial state


## License

This project is open-source. Feel free to modify and distribute as needed. 