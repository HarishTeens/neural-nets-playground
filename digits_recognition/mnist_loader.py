"""
mnist_loader
~~~~~~~~~~~~

A library to load the MNIST image data from Kaggle's CSV format.
Kaggle MNIST dataset: https://www.kaggle.com/datasets/oddrationale/mnist-in-csv

Expected files:
    ../data/mnist_train.csv  (60,000 rows)
    ../data/mnist_test.csv   (10,000 rows)

Each CSV row format: label, pixel0, pixel1, ..., pixel783

For details of the data structures returned, see the doc strings for
``load_data`` and ``load_data_wrapper``.  In practice, ``load_data_wrapper``
is the function usually called by our neural network code.
"""

#### Libraries
import numpy as np


def load_data():
    """Return the MNIST data as a tuple containing the training data,
    the validation data, and the test data.

    Reads from Kaggle's CSV format:
        ../data/mnist_train.csv  — used for training + validation
        ../data/mnist_test.csv   — used for testing

    The ``training_data`` is returned as a tuple with two entries.
    The first entry contains the actual training images — a numpy
    ndarray with 50,000 entries, each a 784-dimensional vector of
    pixel values normalized to [0, 1].

    The second entry is a numpy ndarray of 50,000 digit labels (0..9).

    ``validation_data`` is similar but contains 10,000 images (the last
    10,000 rows of mnist_train.csv).

    ``test_data`` contains 10,000 images from mnist_test.csv.
    """
    # Load train CSV — first column is label, rest are 784 pixels
    train_raw = np.loadtxt("../../mnist/mnist_train.csv", delimiter=",", skiprows=1)
    test_raw = np.loadtxt("../../mnist/mnist_test.csv", delimiter=",", skiprows=1)

    # Normalize pixel values from [0, 255] to [0, 1]
    train_images = train_raw[:, 1:] / 255.0
    train_labels = train_raw[:, 0].astype(int)

    test_images = test_raw[:, 1:] / 255.0
    test_labels = test_raw[:, 0].astype(int)

    # Split train into 50,000 training + 10,000 validation
    training_data = (train_images[:50000], train_labels[:50000])
    validation_data = (train_images[50000:], train_labels[50000:])
    test_data = (test_images, test_labels)

    return (training_data, validation_data, test_data)


def load_data_wrapper():
    """Return a tuple containing ``(training_data, validation_data, test_data)``.
    Based on ``load_data``, but the format is more convenient for use in our
    neural network implementation.

    ``training_data`` is a list of 50,000 2-tuples ``(x, y)`` where:
        x — 784-dimensional numpy.ndarray (column vector, shape (784,1))
        y — 10-dimensional numpy.ndarray, one-hot encoding of the digit

    ``validation_data`` and ``test_data`` are lists of 10,000 2-tuples ``(x, y)`` where:
        x — 784-dimensional numpy.ndarray (column vector, shape (784,1))
        y — integer digit label (0..9)

    The different y formats (one-hot for training, integer for validation/test)
    match what the network's cost and evaluation functions expect.
    """
    tr_d, va_d, te_d = load_data()

    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = list(zip(training_inputs, training_results))

    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = list(zip(validation_inputs, va_d[1]))

    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = list(zip(test_inputs, te_d[1]))

    return (training_data, validation_data, test_data)


def vectorized_result(j):
    """Return a 10-dimensional unit vector with a 1.0 in the jth position
    and zeroes elsewhere.  Used to convert a digit (0..9) into a one-hot
    target vector for the neural network output layer."""
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e
