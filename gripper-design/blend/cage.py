"""The black cage: two windowed side plates (as frames of boxes), the back plate and the servo head. The model ends here."""
from hand_common import *

def build(root, M):
    x0, x1, z0, z1 = CAGE['x0'], CAGE['x1'], CAGE['z0'], CAGE['z1']
    W = [(-150, 30, 110, 200), (-150, 30, 280, 440)]                      # the windows: clamp zone, pipette zone
    for s, tag in ((1, 'P'), (-1, 'N')):
        y0 = HALF_IN if s > 0 else -HALF_OUT; y1 = y0 + PLATE
        box(f'cage_side_{tag}_foot', x0, x1, y0, y1, z0, W[0][2], M.black)
        box(f'cage_side_{tag}_band', x0, x1, y0, y1, W[0][3], W[1][2], M.black)
        box(f'cage_side_{tag}_top', x0, x1, y0, y1, W[1][3], z1, M.black)
        box(f'cage_side_{tag}_back', x0, W[0][0], y0, y1, W[0][2], W[1][3], M.black)
        box(f'cage_side_{tag}_front', W[0][1], x1, y0, y1, W[0][2], W[1][3], M.black)
    box('cage_back', x0, x0 + PLATE, -HALF_IN, HALF_IN, z0, z1, M.black)
    box('head', HEAD['x0'], HEAD['x1'], -HALF_OUT, HALF_OUT, HEAD['z0'], z1, M.black)
    box('head_top', HEAD['x0'], HEAD['x1'], -HALF_OUT, HALF_OUT, z1 - 4, z1 + 2, M.gray)
    box('head_led', HEAD['x1'] - 0.2, HEAD['x1'] + 0.4, -8, 8, 497, 503, M.led)
