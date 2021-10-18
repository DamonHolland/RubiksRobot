import logging
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import ai.RubiksDataset as Data
import time
import tensorflow as tf
from datetime import timedelta
from keras import Sequential
from keras.layers import Dense, Activation, InputLayer


def save_model(model_to_save, model_name):
    model_to_save.save("models/" + model_name)


def load_model(model_name):
    if model_name:
        return tf.keras.models.load_model("models/" + model_name)
    else:
        return None


def create_model():
    new_model = Sequential()
    new_model.add(InputLayer(324))
    new_model.add(Dense(228))
    new_model.add(Activation('relu'))
    new_model.add(Activation('softmax'))
    new_model.compile(optimizer="Adam", loss=["sparse_categorical_crossentropy"], metrics=["accuracy"])
    new_model.summary()
    return new_model


if __name__ == '__main__':
    NUM_SCRAMBLES = 4
    LOSS_GOAL = 0.2
    ACCURACY_GOAL = 1
    BATCH_SIZE = 1000
    NUM_EPOCHS = 10
    EVALUATION_SIZE = 100
    # Set To None If you want to create a new model
    # Set to the name of the model if you want to continue training
    MODEL_NAME = None

    model = load_model(MODEL_NAME) if MODEL_NAME else create_model()

    logging.getLogger('tensorflow').disabled = True
    print("\nThere are approximately {} permutations for {} scrambles.\n".format(12 * pow(11, NUM_SCRAMBLES - 1), NUM_SCRAMBLES))

    start_time = time.time()
    test_loss, test_acc = 100, 0
    session = 0
    while test_acc < ACCURACY_GOAL or test_loss > LOSS_GOAL:
        session_time = time.time()
        session += 1
        print("********** Session {} **********".format(session))
        print("Fitting Model".format(session))
        train_x, train_y = Data.create_training_data(BATCH_SIZE, NUM_SCRAMBLES)
        model.fit(train_x, train_y, epochs=NUM_EPOCHS, verbose=0)
        print("Evaluating Model".format(session))
        test_x, test_y = Data.create_training_data(EVALUATION_SIZE, NUM_SCRAMBLES)
        test_loss, test_acc = model.evaluate(test_x, test_y)
        save_model(model, "Training")
        print("Session Time {}".format(timedelta(seconds=time.time() - session_time)))
        print("Running Time {}".format(timedelta(seconds=time.time() - start_time)))
        print("******************************{}\n".format("*" * int(session / 10)))
    save_model(model, str(NUM_SCRAMBLES) + "_" + str(test_acc) + "_" + str(test_loss))
    print("Training Completed in {}".format(timedelta(seconds=time.time() - start_time)))
    print("\nModel Saved as {}\n".format(str(NUM_SCRAMBLES) + "_" + str(test_acc) + "_" + str(test_loss)))
