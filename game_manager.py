from game_logic import GameLogic

# Shared game instance
_game_instance = GameLogic()

# GUI update callback
_gui_update_callback = None

def get_instance():
    """Gets the current game instance."""
    global _game_instance
    return _game_instance

def set_instance(new_instance):
    """Sets a new game instance and triggers GUI update if callback is set."""
    global _game_instance
    _game_instance = new_instance
    
    # Trigger GUI update if callback is set
    trigger_gui_update()

def reset_instance():
    """Resets the game by creating a new GameLogic instance."""
    set_instance(GameLogic())

def set_gui_update_callback(callback):
    """Sets the function to call when the game state changes."""
    global _gui_update_callback
    _gui_update_callback = callback

def trigger_gui_update():
    """Triggers a GUI update with the current game state."""
    if _gui_update_callback:
        _gui_update_callback(_game_instance.get_status()) 