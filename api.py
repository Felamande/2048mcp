from flask import Flask, jsonify, request
import threading
import logging
import game_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # Reduce Flask's default logging noise

app = Flask(__name__)

# --- Game State Management ---
# A lock is crucial to prevent race conditions when multiple requests
# try to modify the game state simultaneously.
game_lock = threading.Lock()

def set_gui_update_callback(callback):
    """Sets the function to call when the game state changes."""
    game_manager.set_gui_update_callback(callback)

def trigger_gui_update():
    """Calls the registered GUI update callback if it exists."""
    game_manager.trigger_gui_update()

# --- API Endpoints ---

@app.route('/status', methods=['GET'])
def get_status():
    """Returns the current game status."""
    with game_lock:
        status = game_manager.get_instance().get_status()
    return jsonify(status)

@app.route('/move/<direction>', methods=['POST'])
def move(direction):
    """Attempts to make a move in the specified direction."""
    valid_directions = ['up', 'down', 'left', 'right']
    if direction not in valid_directions:
        return jsonify({"result": "fail", "error": "Invalid direction"}), 400

    result_status = "fail"
    error_message = None
    status_code = 200 # Default OK

    with game_lock:
        game_instance = game_manager.get_instance()
        if game_instance.game_over:
            result_status = "fail"
            error_message = "Game is over"
            status_code = 400 # Bad request as game is over
        else:
            try:
                moved = game_instance.move(direction)
                if moved:
                    result_status = "ok"
                    # Explicitly trigger GUI update
                    game_manager.trigger_gui_update()
                else:
                    # Check if the game is over *after* the move attempt
                    if game_instance.game_over:
                         result_status = "fail"
                         error_message = "Game over - no more moves possible"
                         status_code = 400 # Game ended
                         # Explicitly trigger GUI update to show final state
                         game_manager.trigger_gui_update()
                    else:
                        result_status = "ok"
                        error_message = "but your move did not change the board"
            except Exception as e:
                result_status = "fail"
                error_message = f"Internal server error: {str(e)}"
                status_code = 500
                print(f"Error during move '{direction}': {e}") # Log internal errors

        # Get current game status to include in response
        current_status = game_instance.get_status()
    print(f"<{direction}>: {current_status} {result_status} {error_message}")
    response = {
        "game_result": result_status,
        "current_status": current_status
    }
    if error_message:
        response["error"] = error_message

    return jsonify(response), status_code

@app.route('/reset', methods=['POST'])
def reset_game():
    """Resets the game to its initial state."""
    with game_lock:
        game_manager.reset_instance()
    return jsonify({"result": "ok", "message": "Game reset successfully"})

@app.route('/try_move/<direction>', methods=['POST'])
def try_move(direction):
    """Simulates a move in the specified direction without affecting the actual game state."""
    valid_directions = ['up', 'down', 'left', 'right']
    if direction not in valid_directions:
        return jsonify({"result": "fail", "error": "Invalid direction"}), 400

    with game_lock:
        game_instance = game_manager.get_instance()
        # Use the try_move method to simulate the move without changing the game state
        result = game_instance.try_move(direction)
        
    response = {
        "game_result": "ok" if result["valid"] else "fail",
        "simulated_status": {
            "board": result["board"],
            "score": result["score"],
            "game_over": result["game_over"],
            "size": game_instance.size
        }
    }
    
    if not result["valid"]:
        if result["game_over"]:
            response["error"] = "Game over - no more moves possible"
        else:
            response["error"] = "Move would not change the board"
    
    return jsonify(response)

# --- Flask App Runner ---
def run_api(host='127.0.0.1', port=5000):
    """Runs the Flask development server."""
    # Use threaded=True to handle multiple requests, especially important
    # if GUI updates take time or block.
    # use_reloader=False is important when running alongside tkinter
    print(f"Starting Flask API server on http://{host}:{port}")
    app.run(host=host, port=port, threaded=True, use_reloader=False)

if __name__ == '__main__':
    # This allows running the API standalone for testing
    run_api()