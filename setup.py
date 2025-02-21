# setup.py
import sys
from cx_Freeze import setup, Executable

# Optional: This can help ensure 'pygame' modules get included
build_exe_options = {
    "packages": ["pygame"],
    "include_files": [
        # Add data files or folders here
        # e.g. ("src/assets", "assets"), to copy the folder into the build
        ("src"),
    ],
}

# Some games need to ensure Python knows where the base executable is
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # for a GUI app with no console window
    # base = None       # if you want a console window for debugging

setup(
    name="CS-Monopoly",
    version="1.0",
    description="My Monopoly Game with Pygame",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="src/main.py",  # Path to your main script
            base=base,
            target_name="CSMonopoly.exe",  # The name of the executable
        )
    ],
)
