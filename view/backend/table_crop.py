"""Table region shared by the fixed general cameras in MuJoCo and Replay."""
import math


# Keep the entire bench width and a margin above its samples. Recheck these
# fractions whenever either camera's framing changes.
TABLE_TOP = 0.30
TABLE_BOTTOM = 0.75


def table_region(frame):
    height = frame.shape[0]
    top = int(height * TABLE_TOP)
    bottom = math.ceil(height * TABLE_BOTTOM)
    return frame[top:bottom, :], top
