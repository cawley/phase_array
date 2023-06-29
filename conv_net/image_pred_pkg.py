from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

model = Sequential()

# input layer that takes a 16x16 grayscale image (pixel values between 0 and 63)
model.add(Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=(16, 16, 1)))

# convolutional and max pooling layers
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

# 2D to 1D
model.add(Flatten())

# dense layer
model.add(Dense(128, activation="relu"))

# output layer with 64 nodes
model.add(Dense(64))

model.compile(optimizer="adam", loss="mean_squared_error")

model.summary()
