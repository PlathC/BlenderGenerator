import bpy
import sys, os

path = "_PATH_"
file = "_MAIN_FILE_"
sys.path.append(path)
filename = os.path.join(path, file)
exec(compile(open(filename).read(), filename, 'exec'))