import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai.AISolver import AISolver
from model.RubiksCube import RubiksCube
from ai.RubiksMoves import MoveDecoder
import time
import serial

PARALLEL_MOVES = {"U": "D",
                  "D": "U",
                  "F": "B",
                  "B": "F",
                  "L": "R",
                  "R": "L"}
SCRAMBLE_AMOUNT = 10
TIME_LIMIT = 15
SPEED = "200"
COM_PORT = "COM6"
BAUDRATE = 9600


def parseMoves(move_array):
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
    # Combine Parallel Moves
    i = 1
    while i < len(move_array):
        if move_array[i][0] == PARALLEL_MOVES[move_array[i - 1][0]]:
            move_array[i - 1] += move_array[i]
            move_array.pop(i)
        i += 1
    return SPEED + ' ' + ' '.join(move_array)


def sendSerial(serial_message):
    print("Serial Input: {}".format(serial_message))
    ser = serial.Serial()
    ser.baudrate = BAUDRATE
    ser.port = COM_PORT
    ser.open()
    if not ser.isOpen():
        print("Failed to open Serial")
    ser.write(serial_message.encode())
    ser.close()


def PhysicalSolve():
    ai_solver = AISolver("../ai/models/9_Training")
    rubiks_cube = RubiksCube()

    # Scan Cube for AI to solve - For Now we just scramble ourselves.
    print("Scrambled cube {} moves.".format(SCRAMBLE_AMOUNT))
    scramble = rubiks_cube.scramble(SCRAMBLE_AMOUNT)
    scramble = [MoveDecoder[i] for i in scramble]
    print("Scramble: {}".format(str(scramble)))

    # Send Scramble to Motors
    try:
        sendSerial(parseMoves(scramble))
    except:
        pass

    # Use AI To Calculate Solve
    start_t = time.time()
    solve_moves = ai_solver.solve(rubiks_cube, TIME_LIMIT)
    solve_moves = [MoveDecoder[i] for i in solve_moves]
    if not solve_moves:
        print("AI Failed to Find Solution")
        return
    print("AI solved cube in {} seconds.".format(round(time.time() - start_t, 2)))
    print("Solve: {}".format(str(solve_moves)))

    # Delay before solving, so we can see the scramble
    if time.time() - start_t < 2:
        time.sleep(2 - (time.time() - start_t))

    # Send Solve to Motors
    try:
        sendSerial(parseMoves(solve_moves))
    except:
        pass

if __name__ == '__main__':
    PhysicalSolve()