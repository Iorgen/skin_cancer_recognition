from keras import models
from keras import layers
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Conv1D
from keras.optimizers import Adam, RMSprop,SGD


def task_optimizer(optimizer):
    if (optimizer == "SGD"):
        return SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
    elif (optimizer == "RMSprop"):
        return RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
    elif (optimizer == "Adam"):
        return Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    else:
        return Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)


def topology_a(optimizer):
    #  input shape using shape off test samples
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), input_shape=(100, 75, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(128, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(256))
    model.add(layers.Activation('relu'))

    model.add(layers.Dense(7))
    model.add(layers.Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    print(model.summary())
    return model


def topology_b(optimizer):
    #  input shape using shape off test samples
    model = models.Sequential()
    model.add(layers.Conv2D(16, (3, 3), input_shape=(150,100,3)))
    model.add(layers.Activation('relu'))
    model.add(layers.Conv2D(16, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(32, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.Conv2D(32, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.Conv2D(64, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(64))
    model.add(layers.Activation('relu'))

    model.add(layers.Dense(64))
    model.add(layers.Activation('relu'))
    model.add(layers.Dropout(0.1))

    model.add(layers.Dense(3))
    model.add(layers.Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer = optimizer,
                  metrics=['accuracy'])
    print(model.summary())
    return model


def topology_c(optimizer):
    #  input shape using shape off test samples
    model = models.Sequential()
    model.add(layers.Conv2D(64, (3, 3), input_shape=(200,150,3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(128))
    model.add(layers.Activation('relu'))

    model.add(layers.Dense(128))
    model.add(layers.Activation('relu'))
    model.add(layers.Dropout(0.1))

    model.add(layers.Dense(3))
    model.add(layers.Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer = optimizer,
                  metrics=['accuracy'])
    print(model.summary())
    return model


def topology_d(optimizer):
    #  input shape using shape off test samples
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), input_shape=(100, 75, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3)))
    # model.add(layers.Conv2D(64, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3)))
    # model.add(layers.Conv2D(128, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3)))
    # model.add(layers.Conv2D(128, (3, 3)))
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(64))
    model.add(layers.Activation('relu'))
    model.add(layers.Dropout(0.1))

    model.add(layers.Dense(128))
    model.add(layers.Activation('relu'))
    model.add(layers.Dropout(0.1))

    model.add(layers.Dense(7))
    model.add(layers.Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    print(model.summary())
    return model