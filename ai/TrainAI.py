import logging
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai.RubiksDataset import RubiksDatabase
import time
import tensorflow as tf
from datetime import timedelta
from keras import Sequential
from keras.layers import Dense, InputLayer, Dropout


def save_model(model_to_save, model_name):
    model_to_save.save("models/" + model_name)


def create_model(output_size):
    new_model = Sequential()
    new_model.add(InputLayer(324))
    new_model.add(Dense(4096, activation='relu'))
    new_model.add(Dropout(0.2))
    new_model.add(Dense(2048, activation='relu'))
    new_model.add(Dropout(0.2))
    new_model.add(Dense(324, activation='relu'))
    new_model.add(Dense(output_size, activation='softmax'))
    new_model.compile(optimizer=tf.keras.optimizers.Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    new_model.summary()
    return new_model


if __name__ == '__main__':
    NUM_SCRAMBLES = 10
    LOSS_GOAL = 0.1
    ACCURACY_GOAL = 1.0
    BATCH_SIZE = 8192
    NUM_EPOCHS = 5
    EVALUATION_SIZE = 8192

    db = RubiksDatabase()

    model = create_model(NUM_SCRAMBLES)
    logging.getLogger('tensorflow').disabled = True

    start_time = time.time()
    test_loss, test_acc = 100, 0
    session = 0
    while test_acc < ACCURACY_GOAL or test_loss > LOSS_GOAL:
        session_time = time.time()
        session += 1
        print("********** Session {} **********".format(session))
        print("Fitting Model".format(session))
        train_x, train_y = db.get_data(NUM_SCRAMBLES, BATCH_SIZE)
        model.fit(train_x, train_y, epochs=NUM_EPOCHS)
        print("Evaluating Model".format(session))
        test_x, test_y = db.get_data(NUM_SCRAMBLES, EVALUATION_SIZE)
        test_loss, test_acc = model.evaluate(test_x, test_y)
        print("Session Time {}".format(timedelta(seconds=time.time() - session_time)))
        print("Running Time {}".format(timedelta(seconds=time.time() - start_time)))
        print("******************************{}\n".format("*" * len(str(session))))
        save_model(model, "Training")
    save_model(model, str(NUM_SCRAMBLES) + "_" + str(test_acc) + "_" + str(test_loss))
    print("9_Model Completed in {}".format(timedelta(seconds=time.time() - start_time)))
    print("\nModel Saved as {}\n".format(str(NUM_SCRAMBLES) + "_" + str(test_acc) + "_" + str(test_loss)))
