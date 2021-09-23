from threading import Thread
from model.RubiksCube import RubiksCube
from visuals.RubiksVisualizer import RubiksVisualizer
import tensorflow as tf
from tensorflow import keras
import ai.RubiksDataset as data
from keras.models import Sequential
from keras.layers import Dense, Activation
from model.RubiksMoves import MoveDict

if __name__ == '__main__':

    model = Sequential()
    model.add(Dense(162, input_shape=(162,)))
    model.add(Dense(48, input_shape=(162,)))
    model.add(Activation('relu'))
    model.add(Dense(12, input_shape=(48,)))
    model.add(Activation('sigmoid'))

    model.compile(optimizer="Adam",
                  loss=["sparse_categorical_crossentropy"],
                  metrics=["accuracy"])

    train_x, train_y = data.createTrainingData(30, 1)
    model.fit(train_x, train_y, epochs=10, steps_per_epoch=25, verbose=2)

    print("\nFitting Complete\n\nEvaluating Model\n")

    test_x, test_y = data.createTrainingData(30, 1)
    test_loss, test_acc = model.evaluate(test_x, test_y)

    print("Single Solve Test")
    single_x, single_y = data.createTrainingData(1, 1)
    if single_y[0] % 2 == 0:
        inverse_move = MoveDict[single_y[0] + 1]
    else:
        inverse_move = MoveDict[single_y[0] - 1]
    print("Performing single scramble: {}".format(inverse_move))
    prediction = model.predict(single_x)
    prediction = prediction[0]
    print(prediction)
    max = 0
    max_i = 0
    for i in range(len(prediction)):
        if prediction[i] > max:
            max = prediction[i]
            max_i = i
    print("AI predicts move {}".format(MoveDict[max_i]))

