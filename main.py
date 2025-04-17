import threading
import tkinter as tk
from gui import GameGUI
from api import run_api, set_gui_update_callback, game_instance # Import game_instance to link GUI

def main():
    # Create the Tkinter root window and GUI instance
    root = tk.Tk()
    gui = GameGUI(master=root)

    # --- Crucial Link: Connect API changes to GUI ---
    # Pass the GUI's update method to the API module.
    # We also need to ensure the GUI starts with the *same* game instance
    # that the API is using.
    gui.game = game_instance # Make GUI use the shared game instance from api.py
    set_gui_update_callback(gui.update_game_state)

    # Pack the GUI elements
    gui.pack()

    # --- Start the API server in a separate thread ---
    # Use a daemon thread so it exits when the main program (GUI) exits.
    api_thread = threading.Thread(target=run_api, kwargs={'host': '127.0.0.1', 'port': 5000}, daemon=True)
    api_thread.start()

    print("GUI and API server starting...")
    print("Access the API at http://127.0.0.1:5000")
    print("API Endpoints:")
    print("  GET /status")
    print("  POST /move/{up|down|left|right}")
    print("  POST /try_move/{up|down|left|right}")
    print("  POST /reset")


    # --- Start the Tkinter main loop (must be in the main thread) ---
    root.mainloop()

if __name__ == "__main__":
    main()