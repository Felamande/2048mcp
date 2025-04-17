from flask import Flask, jsonify, request
from game_logic import GameLogic
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # Reduce Flask's default logging noise

app = Flask(__name__)

# --- Game State Management ---
# We need a single instance of the game shared between requests.
# A lock is crucial to prevent race conditions when multiple requests
# try to modify the game state simultaneously.
game_instance = GameLogic()
game_lock = threading.Lock()

# --- GUI Update Callback ---
# This function will be set by the main application (`main.py` later)
# to allow the API to trigger GUI updates.
gui_update_callback = None

def set_gui_update_callback(callback):
    """Sets the function to call when the game state changes."""
    global gui_update_callback
    gui_update_callback = callback

def trigger_gui_update():
    """Calls the registered GUI update callback if it exists."""
    if gui_update_callback:
        try:
            # Run callback in a separate thread to avoid blocking API response
            threading.Thread(target=gui_update_callback, args=(game_instance.get_status(),)).start()
        except Exception as e:
            print(f"Error triggering GUI update: {e}") # Log error

# --- API Endpoints ---

@app.route('/status', methods=['GET'])
def get_status():
    """Returns the current game status."""
    with game_lock:
        status = game_instance.get_status()
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
        if game_instance.game_over:
            result_status = "fail"
            error_message = "Game is over"
            status_code = 400 # Bad request as game is over
        else:
            try:
                moved = game_instance.move(direction)
                if moved:
                    result_status = "ok"
                    # Trigger GUI update only if the move was successful and changed the board
                    trigger_gui_update()
                else:
                    # Check if the game is over *after* the move attempt
                    if game_instance.game_over:
                         result_status = "fail"
                         error_message = "Game over - no more moves possible"
                         status_code = 400 # Game ended
                         # Trigger GUI update to show final state
                         trigger_gui_update()
                    else:
                        result_status = "fail"
                        error_message = "Move did not change the board state"
                        # This isn't strictly an error, but indicates no change
                        # status_code = 200 or maybe 400 depending on desired API behavior
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
    global game_instance
    with game_lock:
        game_instance = GameLogic() # Create a new game instance
        trigger_gui_update() # Update GUI to show the new board
    return jsonify({"result": "ok", "message": "Game reset successfully"})


# --- Flask App Runner ---
# Note: This part is typically run from a main script, not directly here
# if integrating with a GUI in the same process.
# We will create a main.py later.

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