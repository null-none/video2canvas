import sys
from ..src.convert import Convert

try:
    filein = sys.argv[1]
    fileout = "video.js"
    convert = Convert()
    convert.video_to_js(filein, 120, 150, 1, 15, fileout)
except:
    print("Usage: %s video_file" % sys.argv[0])
