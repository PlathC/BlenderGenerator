import bpy
import sys, os

path = "D:\\Documents\\Cours\\UTBM\\S2\\IN55\\BlenderGenerator"
file = "main.py"
sys.path.append(path)
filename = os.path.join(path, file)
module = compile(open(filename).read(), filename, 'exec')

exec(module)
