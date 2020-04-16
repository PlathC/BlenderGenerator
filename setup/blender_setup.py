
import bpy
import sys, os

path = "__PATH__"
file = "__MAIN__"
sys.path.append(path)
filename = os.path.join(path, file)
module = compile(open(filename).read(), filename, 'exec')

exec(module)
