"""The micropipette fixed on the vial's axis, parked (tip at TIP_READY): rail on the -Y plate, carriage, arm plates, the pipette."""
from hand_common import *

def build(root, M):
    box('p_rail', 39, 51, -HALF_IN, -HALF_IN + 6, 137, TIP_READY + 228.5, M.black)
    box('p_servo', 29, 61, -67, -55, TIP_READY + 231.5, TIP_READY + 257.5, M.black); box('p_servo_led', 39, 51, -55.4, -54.6, TIP_READY + 241.5, TIP_READY + 247.5, M.led)
    pip = empty('pipette', root, z=TIP_READY)                                # the tip at its origin
    box('p_carriage', 29, 61, -67, -55, 117, 228.5, M.gray, pip)
    for z in (125, 168.5):
        box(f'p_arm_{int(z)}', -16, 61, -55, -16, z - 7, z + 7, M.gray, pip); ring(f'p_ring_{int(z)}', 17, 12.5, z - 8, z + 8, 0, 0, M.gray, pip, 16)
    cyl('p_tip', 2.4, 3.6, 0, 12, 0, 0, M.black, pip, 32); cyl('p_shaft', 3.6, 5.8, 12, 90, 0, 0, M.blue, pip, 32); cyl('p_collar', 5.8, 11.2, 90, 116, 0, 0, M.blue, pip, 40)
    box('p_body', -15, 15, -12, 12, 116, 221, M.white, pip); cyl('p_plunger', 4, 4, 219, 251, 3, 0, M.white, pip, 24); cyl('p_button', 8.5, 8.5, 251, 259.5, 3, 0, M.blue, pip, 32)
    cyl('p_actuator', 9, 9, 269.5, 305.5, 3, 0, M.black, pip, 32); box('p_actuator_arm', -6, 6, 14, 26, 284.5, 296.5, M.gray, pip)
    box('p_hook', -39, -11, -8, 8, 209.5, 216.5, M.gray, pip)
