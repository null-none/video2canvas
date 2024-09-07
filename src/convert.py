import sys
import cv2


class Convert(object):

    def resize_frame(self, frame, view_width, view_height):
        height, width, _ = frame.shape
        reduction_factor = (float(view_height)) / height * 100
        reduced_width = int(width * reduction_factor / 100)
        reduced_height = int(height * reduction_factor / 100)
        dim = (reduced_width, reduced_height)
        resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_LINEAR)
        return resized_frame

    def pixel_to_rgb(self, pixel):
        bgr = tuple(float(x) for x in pixel[:3])
        return tuple(reversed(bgr))

    def get_video(self, filename):
        return cv2.VideoCapture(filename)

    def get_video_props(self, cap):
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        return width, height, length, fps

    def get_frame(self, cap, view_width=None, view_height=None):
        while cap.isOpened():
            _ret, frame = cap.read()
            if frame is None:
                break
            else:
                if view_height is None or view_width is None:
                    yield frame
                else:
                    yield self.resize_frame(frame, view_width, view_height)

    def video_to_js(
        self, infile, cwidth, cheight, frame_start, frame_end, outfile=None
    ):
        opacity = 255
        comp = 26
        cap = get_video(infile)
        if outfile is None:
            writer = sys.stdout
        else:
            writer = open(outfile, "w")
            print("Writing to %s ..." % outfile)
        width, height, length, real_fps = self.get_video_props(cap)
        real_freq = int(1000 / real_fps)

        writer.write("video ={\n")
        writer.write('"width":%s,\n' % cwidth)
        writer.write('"height":%s,\n' % cheight)
        writer.write('"fps":%s,\n' % real_fps)
        writer.write('"freq":%s,\n' % real_freq)
        writer.write('"data":[\n')
        fn = 0
        i = 0
        fwidth = 0
        fheight = 0
        for rframe in self.get_frame(cap, cwidth, cheight):
            fn += 1
            if fn < frame_start:
                continue
            if fn > frame_end:
                break
            fheight, fwidth, _ = rframe.shape
            pad = max(int(cwidth) - fwidth, 0)
            writer.write('"')
            for j in range(fheight - 1):
                for i in range(fwidth):
                    pixel = rframe[j][i]
                    r, g, b = self.pixel_to_rgb(pixel)
                    writer.write("%s" % int(r / comp))
                    writer.write("%s" % int(g / comp))
                    writer.write("%s" % int(b / comp))
            writer.write('",\n')
            writer.flush()
        writer.write('""\n')
        writer.write(" ],\n")
        writer.write('"frame_width":%s,\n' % fwidth)
        writer.write('"frame_height":%s\n' % fheight)
        writer.write("}\n")
        writer.flush()
