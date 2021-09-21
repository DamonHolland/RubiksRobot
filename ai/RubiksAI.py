import ai.CategoricalEncoding as ce
from threading import Thread
from model.RubiksCube import RubiksCube
from visuals.RubiksVisualizer import RubiksVisualizer



def encode_to_input(cube) -> str:
    encoding = ""
    for face_color in cube.faces:
        encoding += ce.EncodingDict[face_color]
    return encoding

if __name__ == '__main__':
    rubiks_cube = RubiksCube()
    visuals = RubiksVisualizer()
    visual_thread = Thread(target=visuals.start, args=[rubiks_cube])
    visual_thread.start()
    print("Encoded Input: " + encode_to_input(rubiks_cube))


