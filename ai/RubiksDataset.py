import random
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from mysql import connector
from model.RubiksCube import RubiksCube
from RubiksMoves import encode_to_input
from ai.AISolver import AISolver


class RubiksDatabase:
    def __init__(self):
        self.conn = connector.connect(host="185.212.71.102", user="u625114106_DamonHolland", passwd="RubiksData123",
                                      database="u625114106_rubiks_data")
        print("Connection to MySQL DB successful")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS RubiksData(encoding VARCHAR(324), scramble INTEGER, PRIMARY KEY (encoding))")
        self.conn.commit()

    def insert(self, encoding, scramble):
        encoding_string = ""
        for elem in encoding:
            encoding_string += str(elem)
        try:
            self.cursor.execute("INSERT INTO RubiksData VALUES ('{}', '{}')".format(encoding_string, scramble))
            print("Added new data for scramble {}".format(scramble))
        except connector.errors.IntegrityError:
            self.cursor.execute("SELECT scramble FROM RubiksData WHERE encoding = '{}'".format(encoding_string))
            existing_scramble = self.cursor.fetchall()[0][0]
            if existing_scramble > scramble:
                print("Replaced existing scramble {} with {}".format(existing_scramble, scramble))
                self.cursor.execute("REPLACE INTO RubiksData VALUES ('{}', '{}')".format(encoding_string, scramble))
        self.conn.commit()

    def get_data(self, scramble_max, num_samples):
        results = []
        for i in range(scramble_max):
            self.cursor.execute("SELECT * FROM RubiksData WHERE scramble = {} ORDER BY RAND() LIMIT {}"
                                .format(i + 1, int(num_samples / scramble_max)))
            results += self.cursor.fetchall()
        data_input = []
        data_output = []
        for i in range(len(results)):
            rebuilt = []
            for char in results[i][0]:
                rebuilt.append(int(char))
            data_input.append(np.array(rebuilt))
            data_output.append(int(results[i][1]) - 1)
        shuffle = np.random.permutation(len(data_input))
        return np.array(data_input)[shuffle], np.array(data_output)[shuffle]

    def size(self):
        self.cursor.execute("SELECT Count(scramble) FROM RubiksData")
        return self.cursor.fetchall()[0][0]


if __name__ == '__main__':
    cube = RubiksCube()
    SCRAMBLE_AMOUNT = 10
    MAX_SOLVE_TIME = 10
    ai_solver = AISolver("models\9_Model")
    database = RubiksDatabase()
    while True:
        scramble_amount = SCRAMBLE_AMOUNT
        cube.reset()
        cube.scramble(scramble_amount)
        solve = ai_solver.solve(cube, MAX_SOLVE_TIME)
        database.insert(encode_to_input(cube), min(scramble_amount, len(solve)) if solve else scramble_amount)
