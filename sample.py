import tensorflow as tf
from tensorflow.keras import layers, models

model = models.Sequential()
# First Convolutional Layer
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(0.25))
# Second Convolutional Layer
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(0.25))
# Flatten Layer
model.add(layers.Flatten())
# Dense Layer
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dropout(0.5))
# Output Dense Layer
model.add(layers.Dense(10, activation='softmax'))
# Compile the model
model.compile(
optimizer='adam',
loss='categorical_crossentropy',
metrics=['accuracy']
)
# Fit the model
history = model.fit(
X_train, y_train,
epochs=10,
batch_size=32,
validation_data=(X_valid, y_valid)
)
# Print the model summary
print(model.summary())