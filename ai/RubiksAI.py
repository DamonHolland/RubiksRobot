import time

import ai.RubiksDataset as data
from datetime import timedelta
from keras.models import Sequential
from keras.layers import Dense, Activation
from ai.RubiksMoves import MoveDict

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

    test_loss, test_acc = 1, 0

    start_time = time.time()
    while test_acc != 1 or test_loss > 0.2:
        print("\nFitting Model\n")
        train_x, train_y = data.create_training_data(40, 1)
        model.fit(train_x, train_y, epochs=10)
        print("\nEvaluating Model\n")
        test_x, test_y = data.create_training_data(40, 1)
        test_loss, test_acc = model.evaluate(test_x, test_y)

    print("Training Completed in {}".format(timedelta(seconds=time.time() - start_time)))

    print("\nSingle Solve Test\n")
    single_x, single_y = data.create_training_data(1, 1)
    print("Performing single scramble: {}".format(MoveDict[single_y[0] + 1] if single_y[0] % 2 == 0 else MoveDict[single_y[0] - 1]))
    prediction = list(model.predict(single_x)[0])
    print(prediction)
    print("AI predicts move {}".format(MoveDict[prediction.index(max(prediction))]))

