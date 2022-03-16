import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time

PARALLEL_MOVES = {"U": "D", "D": "U", "F": "B", "B": "F", "L": "R", "R": "L"}


def parse_moves_simplify(move_array, motor_speed):
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
    return motor_speed + ' ' + ' '.join(move_array)


def parse_moves_strict(move_array, motor_speed):
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
    return motor_speed + ' ' + ' '.join(move_array)


def send_serial(ser, serial_message):
    print("Serial Input: {}".format(serial_message))
    serial_message += "\n"
    for char in serial_message:
        ser.write(char.encode('utf-8'))
        time.sleep(.00001)
