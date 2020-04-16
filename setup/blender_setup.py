import bpy
import os

filename = os.path.join("_PATH_", "_FILE_NAME_.py")
exec(compile(open(filename).read(), filename, 'exec'))