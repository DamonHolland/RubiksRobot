import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time
import serial
from ai.AISolver import AISolver
from ai.RubiksMoves import MoveDecoder
from model.RubiksCube import RubiksCube
from model.RubiksVisualizer import RubiksVisualizer
from cv.ComputerVisionStatic import ComputerVisionStatic

SCRAMBLE_AMOUNT = 20
TIME_LIMIT = 15
SPEED = "120"
COM_PORT = "COM3"
BAUDRATE = 9600
SERIAL_DELAY = 7

PARALLEL_MOVES = {"U": "D", "D": "U", "F": "B", "B": "F", "L": "R", "R": "L"}


def parse_moves_simplify(move_array):
    # Convert to degrees
    for i in range(len(move_array)):
        if len(move_array[i]) > 1:  move_array[i] = move_array[i][0] + "-90"
        else: move_array[i] = move_array[i] + "90"
    # Combine Consecutive Moves
    i = 1
    while i < len(move_array):
        if move_array[i][0] == move_array[i - 1][0]:
            degree1 = int(move_array[i][1:])
            degree2 = int(move_array[i - 1][1:])
            move_array[i - 1] = move_array[i - 1][0] + str(degree1 + degree2)
            move_array.pop(i)
        i += 1
    # Combine Parallel Moves
    i = 1
    while i < len(move_array):
        if move_array[i][0] == PARALLEL_MOVES[move_array[i - 1][0]]:
            move_array[i - 1] += move_array[i]
            move_array.pop(i)
        i += 1
    return SPEED + ' ' + ' '.join(move_array)


def parse_moves_strict(move_array):
    # Convert to degrees
    for i in range(len(move_array)):
        if len(move_array[i]) > 1:
            move_array[i] = move_array[i][0] + "-90"
        else:
            move_array[i] = move_array[i] + "90"
    # Combine Consecutive Moves
    i = 1
    while i < len(move_array):
        if move_array[i][0] == move_array[i - 1][0]:
            degree1 = int(move_array[i][1:])
            degree2 = int(move_array[i - 1][1:])
            move_array[i - 1] = move_array[i - 1][0] + str(degree1 + degree2)
            move_array.pop(i)
        i += 1
    return SPEED + ' ' + ' '.join(move_array)


def send_serial(serial_message, ser):
    print("Serial Input: {}".format(serial_message))
    serial_message += "\n"
    for char in serial_message:
        ser.write(char.encode('utf-8'))
        time.sleep(.00001)


def robot_control():
    # Set up serial
    ser = serial.Serial()
    ser.baudrate = BAUDRATE
    ser.port = COM_PORT
    try:
        ser.open()
        time.sleep(SERIAL_DELAY)
    except serial.serialutil.SerialException:
        print("Failed to open Serial")
        ser.close()
        return

    # Scan Cube for AI to solve
    send_serial("lights on", ser)
    cv_static = ComputerVisionStatic()
    rubiks_cube = RubiksCube(cv_static.scanCube())
    _visualizer = RubiksVisualizer(rubiks_cube)

    # Use AI To Calculate Solve
    ai_solver = AISolver("../ai/models/10_Model")
    solve_moves = ai_solver.solve(rubiks_cube, TIME_LIMIT)
    solve_moves = [MoveDecoder[i] for i in solve_moves]

    # Send Solve to Motors
    send_serial(parse_moves_simplify(solve_moves), ser)

    time.sleep(SERIAL_DELAY)
    ser.close()


if __name__ == '__main__':
    robot_control()
