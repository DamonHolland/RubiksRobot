import logging
import os
import time
import ai.RubiksDataset as Data
import tensorflow as tf
from datetime import timedelta
from keras import Sequential
from keras.layers import Dense, Activation


def save_model(model_to_save, model_name):
    model_to_save.save("models/" + model_name)
    print("\nModel Saved as {}\n".format(model_name))


def load_model(model_name):
    if model_name:
        return tf.keras.models.load_model("models/" + model_name)
    else:
        return None


if __name__ == '__main__':
    NUM_SCRAMBLES = 3
    LOSS_GOAL = 0.2
    ACCURACY_GOAL = 1
    EPOCH_SIZE = 128
    NUM_EPOCHS = 10
    EVALUATION_SIZE = 128
    # Set To None If you want to create a new model
    # Set to the name of the model if you want to continue training
    MODEL_NAME = "Training"

    model = load_model(MODEL_NAME)
    logging.getLogger('tensorflow').disabled = True

    if not model:
        model = Sequential()
        model.add(Dense(162, input_shape=(162,)))
        model.add(Dense(1024))
        model.add(Activation('relu'))
        model.add(Dense(2048))
        model.add(Activation('relu'))
        model.add(Dense(1024))
        model.add(Activation('relu'))
        model.add(Dense(12))
        model.add(Activation('sigmoid'))

        model.compile(optimizer="Adam",
                      loss=["sparse_categorical_crossentropy"],
                      metrics=["accuracy"])

    os.system('cls')
    start_time = time.time()
    test_loss, test_acc = 1, 0
    session = 0
    while test_acc < ACCURACY_GOAL or test_loss > LOSS_GOAL:
        session += 1
        print("\nFitting Model Session {}\n".format(session))
        train_x, train_y = Data.create_training_data(EPOCH_SIZE, NUM_SCRAMBLES)
        model.fit(train_x, train_y, epochs=NUM_EPOCHS, verbose=2)
        print("\nEvaluating Model - Session {}\n".format(session))
        test_x, test_y = Data.create_training_data(EVALUATION_SIZE, NUM_SCRAMBLES)
        test_loss, test_acc = model.evaluate(test_x, test_y)
        save_model(model, "Training")
    save_model(model, str(NUM_SCRAMBLES) + "_" + str(test_acc) + "_" + str(test_loss))
    print("Training Completed in {}".format(timedelta(seconds=time.time() - start_time)))
