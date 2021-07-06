import subprocess
from ST7789 import ST7789 as Screen

dimensions_cache = None


def get_screen_dimensions(dimensions_cache=dimensions_cache):
    if dimensions_cache: return dimensions_cache
    cmd = ['xrandr']
    cmd2 = ['grep', '*']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()
    resolution_string, junk = p2.communicate()
    resolution = resolution_string.split()[0]
    dimensions_cache = [int(x) for x in resolution.decode().split('x')]
    return dimensions_cache


def scale_dimension(new_scale, size, default_scale=240):
    return int(size / default_scale * new_scale)
