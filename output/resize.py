#!/usr/bin/python
from PIL import Image
import os, sys

path = os.getcwd()
dirs = os.listdir( path )

def resize():
    for item in dirs:
        is_python = os.path.splitext(item)[1] == ".py"
        if os.path.isfile(item) and not is_python:
            print(f"Resizing {item}")
            im = Image.open(item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((200,200), Image.ANTIALIAS)
            if not os.path.isdir(path + "\\resized"):
                os.mkdir(path + "\\resized")
            imResize.save(path + "\\resized\\" + item, 'PNG', quality=90)

resize()