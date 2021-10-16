import random
import time
import logging
import ai.RubiksDataset as data
from datetime import timedelta
from keras.models import Sequential
from keras.layers import Dense, Activation


def save_model(model, model_name):
    model.save("models/" + model_name)


if __name__ == '__main__':
    NUM_SCRAMBLES = 5
    LOSS_GOAL = 0.2
    ACCURACY_GOAL = 1

    logging.getLogger('tensorflow').disabled = True

    model = Sequential()
    model.add(Dense(162, input_shape=(162,)))
    model.add(Dense(120))
    model.add(Activation('relu'))
    model.add(Dense(12))
    model.add(Activation('sigmoid'))

    model.compile(optimizer="Adam",
                  loss=["sparse_categorical_crossentropy"],
                  metrics=["accuracy"])

    start_time = time.time()
    test_loss, test_acc = 1, 0
    session = 0
    while test_acc < ACCURACY_GOAL or test_loss > LOSS_GOAL:
        session += 1
        print("\nFitting Model Session {}\n".format(session))
        train_x, train_y = data.create_training_data(100, NUM_SCRAMBLES)
        model.fit(train_x, train_y, epochs=10)
        print("\nEvaluating Model - Session {}\n".format(session))
        test_x, test_y = data.create_training_data(100, NUM_SCRAMBLES)
        test_loss, test_acc = model.evaluate(test_x, test_y)
        save_model(model, "Training")
    save_model(model, str(NUM_SCRAMBLES) + "_" + str(test_loss) + "_" + str(test_acc))
    print("Training Completed in {}".format(timedelta(seconds=time.time() - start_time)))
