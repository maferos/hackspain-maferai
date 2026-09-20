"""The iris clamp on its X slide: rail, carriage, lift column and the clamp body, in CLAMP_POSE (parked back, high, iris open)."""
from hand_common import *

def build(root, M, cap_r=BOTTLE_60['cap_r'], pose=CLAMP_POSE):
    box('x_rail', -160, 0, HALF_IN - 6, HALF_IN, 224, 236, M.gray)
    box('x_servo', CAGE['x0'] + PLATE, -135, 50, HALF_IN, 250, 276, M.black); box('x_servo_led', -155, -143, 49.6, 50.4, 260, 266, M.led)
    box('x_carriage', -50 + pose['x'], -10 + pose['x'], 40, HALF_IN, 216, 246, M.black)              # rides with clamp_x
    box('lift_column', -37 + pose['x'], -23 + pose['x'], 40, 64, Z_IRIS + 64, 216, M.gray)
    clamp = empty('clamp', root, x=pose['x'], z=Z_IRIS + pose['lift'])    # iris plane at its z = 0; parked back and high
    box('lift_carriage', -41, -19, 36, 68, 64, 102, M.black, clamp)
    box('bridge_y', -42, -18, -4, 56, 62, 70, M.gray, clamp); box('bridge_x', -34, 0, -12, 12, 62, 70, M.gray, clamp)
    cyl('mount_disc', 20, 20, 60, 64, 0, 0, M.black, clamp); cyl('sun_motor', 14, 14, 70, 104, 0, 0, M.black, clamp); cyl('sun_motor_cap', 15, 15, 102, 106, 0, 0, M.gray, clamp)
    ring('housing_front', 69, 59, -4, 16, 0, 0, M.black, clamp, 32); ring('housing_shoulder', 69, 48, 16, 20, 0, 0, M.black, clamp, 32)
    for i in range(3):
        a = i * 2 * math.pi / 3 + math.pi / 3
        box(f'strut_{i}', -5, 5, -7, 7, 18, 60, M.black, clamp, rz=a, center=(54 * math.cos(a), 54 * math.sin(a), 39))
    ring('carrier', 46, 6, 42, 48, 0, 0, M.black, clamp, 24); ring('clutch', 60, 46, 48, 52, 0, 0, M.gray, clamp, 24); ring('top_ring', 60, 46, 56, 60, 0, 0, M.black, clamp, 24)
    ring('cam_ring', 59, 41, 18, 24, 0, 0, M.gold, clamp, 24); ring('ring_gear', 44, 36, 30, 38, 0, 0, M.gold, clamp, 24)
    th = math.acos((35 if pose['open'] else cap_r) / 55)                     # blades open (Ø70) or on the cap
    for k in range(6):
        phi = k * math.pi / 3; a = phi + th
        cx = 55 * math.cos(phi) + 6 * math.cos(a) - 31 * math.sin(a); cy = 55 * math.sin(phi) + 6 * math.sin(a) + 31 * math.cos(a)
        box(f'blade_{k}', -6, 6, -31, 31, k * 2.5, k * 2.5 + 2.5, M.gold, clamp, rz=a, center=(cx, cy, k * 2.5 + 1.25))
