import os
import sys
import subprocess

def build_with_nuitka():
    """Build the application as a standalone executable using Nuitka with icon."""
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the icon path
    icon_path = os.path.join(current_dir, "assets", "2048_icon.ico")
    
    # Make sure the icon exists
    if not os.path.exists(icon_path):
        print(f"Error: Icon file not found at {icon_path}")
        return False
    
    # Build the Nuitka command
    nuitka_command = [
        ".\\.venv\\Scripts\\python","-m","nuitka",
        "--onefile",
        "--windows-icon-from-ico=" + icon_path,
        "--enable-plugin=tk-inter",  # Support for Tkinter
        "--include-data-dir=assets=assets",  # Include the assets directory
        "--windows-console-mode=disable",  # Optional: Hide console window
        "--output-dir=dist",  # Output to dist directory
        "--lto=yes",
        "main.py"  # Main application script
    ]
    
    # Print the command being executed
    print("Executing Nuitka build command:")
    print(" ".join(nuitka_command))
    
    # Execute the Nuitka build command
    try:
        subprocess.run(nuitka_command, check=True)
        print("\nBuild completed successfully!")
        print(f"Executable created in {os.path.join(current_dir, 'dist')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        return False
    except Exception as e:
        print(f"\nUnexpected error during build: {e}")
        return False

if __name__ == "__main__":
    success = build_with_nuitka()
    sys.exit(0 if success else 1) 