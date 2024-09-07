# video2canvas

This script can create a Javascript object with video information from a video file.

The javascript object can be played in **HTML Canvas** as a sequence of frames with pixel data.

## Python packages

* `opencv-python`: OpenCV, Open Source Computer Vision Library. BSD license and hence it’s free for both academic and commercial use.

## Usage

The main function is `video_convert.video_to_js()`

`video_to_js(video_file_in, width, height, frame_start, frame_end, js_file_out)`

* `video_file_in` : File name to convert
* `width` : Desired vieport width
* `height` : Desired viewport height
* `frame_start` : Initial frame to extract
* `frame_end` : Last frame to extract
* `js_file_out` : The output `.js` file to create the video.

The output file is not compressed, so the size is relative to the dimensions of the output in bytes:
`width` x `height` x 3 (rgb) x `frames` (Example: 118 x 150 x 3 x 15 ~ 780kb).


### Python code example

```python
import sys
from ..src.convert import Convert

try:
    filein = sys.argv[1]
    fileout = "video.js"
    convert = Convert()
    convert.video_to_js(filein, 120, 150, 1, 15, fileout)
except:
    print("Usage: %s video_file" % sys.argv[0])
```

```bash
python example.py multi.mov
```

### Javascript Video usage

Use this code snippet to embed your video in Canvas

```html
<canvas id=canvas></canvas>    
<script src="video.js" ></script>
<script src="player.js" ></script>
<script >
document.body.onload=function(){ 
    var player = new VideoPlayer("canvas", video)
    player.startVideo()
}
</script>
```

Where `video.js` is the video file generated by the script, and `player.js` is the Video player component to play the video vile format.



