import sys
import os
import ComputerVisionStatic

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai.AISolver import AISolver
from model.RubiksCube import RubiksCube
from ai.RubiksMoves import MoveDecoder, move_reverse
import time
import serial

SCRAMBLE_AMOUNT = 20
TIME_LIMIT = 15
SPEED = "100"
COM_PORT = "COM4"
BAUDRATE = 9600

PARALLEL_MOVES = {"U": "D",
                  "D": "U",
                  "F": "B",
                  "B": "F",
                  "L": "R",
                  "R": "L"}


def parseMovesSolve(move_array):
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

def parseMovesScramble(move_array):
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



def sendSerial(serial_message, ser):
    print("Serial Input: {}".format(serial_message))
    serial_message += "\n"
    for char in serial_message:
        ser.write(char.encode('utf-8'))
        time.sleep(.00001)


def PhysicalSolve():
    ai_solver = AISolver("../ai/models/10_Model")
    rubiks_cube = RubiksCube()
    # set up serial
    ser = serial.Serial()
    ser.baudrate = BAUDRATE
    ser.port = COM_PORT
    try:
        ser.open()
        time.sleep(7)
    except serial.serialutil.SerialException:
        print("Failed to open Serial")
        ser.close()
        return
    # Scan Cube for AI to solve - For Now we just scramble ourselves.
    scramble = ComputerVisionStatic.scanCube()

    # Send Scramble to Motors
    sendSerial(parseMovesScramble(scramble), ser)

    # Use AI To Calculate Solve
    start_t = time.time()
    solve_moves = ai_solver.solve(rubiks_cube, TIME_LIMIT)
    solve_moves = [MoveDecoder[i] for i in solve_moves]
    print("AI solved cube in {} seconds.".format(round(time.time() - start_t, 2)))
    print("Solve: {}".format(str(solve_moves)))

    # Send Solve to Motors
    sendSerial(parseMovesSolve(solve_moves), ser)
    
    time.sleep(7)
    ser.close()

if __name__ == '__main__':
    PhysicalSolve()