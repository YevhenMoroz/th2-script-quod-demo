import os
import pathlib

print("OS")
print(os.getcwd())

print("absolute path")
print(pathlib.Path(__file__).parent.resolve())