import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import kociemba
from ai.RubiksMoves import MoveEncoder


def kociemba_string(cube):
    # Convert regular cube string to kociemba module accepted format
    string = ""
    for face in cube.faces[0:9]: string += cube.HUMAN_READABLE[face]
    for face in cube.faces[18:27]: string += cube.HUMAN_READABLE[face]
    for face in cube.faces[9:18]: string += cube.HUMAN_READABLE[face]
    string += cube.HUMAN_READABLE[cube.faces[47]]
    string += cube.HUMAN_READABLE[cube.faces[50]]
    string += cube.HUMAN_READABLE[cube.faces[53]]
    string += cube.HUMAN_READABLE[cube.faces[46]]
    string += cube.HUMAN_READABLE[cube.faces[49]]
    string += cube.HUMAN_READABLE[cube.faces[52]]
    string += cube.HUMAN_READABLE[cube.faces[45]]
    string += cube.HUMAN_READABLE[cube.faces[48]]
    string += cube.HUMAN_READABLE[cube.faces[51]]
    for face in cube.faces[36:45]: string += cube.HUMAN_READABLE[face]
    for face in cube.faces[27:36]: string += cube.HUMAN_READABLE[face]
    return string.replace('W', 'U').replace('G', 'F').replace('Y', 'D').replace('O', 'L')


def solve_kociemba(cube):
    # Pass modified string to Kociemba to generate solve
    try:
        solve = kociemba.solve(kociemba_string(cube)).split(' ')
    except ValueError:
        return None
    # Replace double moves with two single moves
    for i, item in list(enumerate(solve))[::-1]:
        if item == 'U2':
            solve[i:i + 1] = ['U', 'U']
        elif item == 'F2':
            solve[i:i + 1] = ['F', 'F']
        elif item == 'R2':
            solve[i:i + 1] = ['R', 'R']
        elif item == 'L2':
            solve[i:i + 1] = ['L', 'L']
        elif item == 'B2':
            solve[i:i + 1] = ['B', 'B']
        elif item == 'D2':
            solve[i:i + 1] = ['D', 'D']
    # Encode moves
    for i in range(len(solve)): solve[i] = MoveEncoder[solve[i]]
    return solve
