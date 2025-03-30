from setuptools import setup

APP = ["src/main.py"]
OPTIONS = {"argv_emulation": True, "includes": ["pygame"], "includes": ["pygame.locals"]} 
setup(
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)