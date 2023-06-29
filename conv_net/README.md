## Convolutional Neural Network for Sharp Image Prediction from Noise
### [Detailed Overview Here](https://github.com/cawley/phase_array/main/conv_net/README.md#relu-rectified-linear-unit-functions)
### Initialize Parameters: 
This step is a bit like setting the initial positions for all the players on a soccer field before the game starts. Each player (or "parameter") has an important role in the game (the "prediction task"), and their initial positions could affect the outcome of the game. The function initialize_parameters() is responsible for setting these starting positions.

### Forward Propagation: 
This is where the model makes its prediction. It's a bit like seeing how the play unfolds after the whistle blows. The ball is passed between players (data flows between parameters), with each player influencing the trajectory of the ball (each parameter affects the final prediction) based on their position and strategy. The function forward_propagation() manages this process.

### Compute Cost:
After the prediction is made, we need to assess how well the model did. This is done by comparing the model's prediction to the true answer, and calculating a 'cost' or 'loss'. The lower the cost, the better the model's prediction. It's a bit like a referee judging the quality of the play. The function compute_cost() calculates this cost.

### Backward Propagation: 
Based on the cost, the model identifies how each player could have played better. It determines how each player (parameter) should change their strategy (adjust their values) to make a better play next time. This is done through a process called "backpropagation", handled by the backward_propagation() function.

### Update Parameters: 
Here the players (parameters) adjust their strategies based on the feedback from the backpropagation step. They make small changes to their strategies (parameter values are updated) in hopes of performing better in the next play. This step is handled by update_parameters_with_adam().

### Iterate: 
The model repeats this process many, many times (each iteration is a bit like a new game). Each time, the players get a little better at their game, and the model's predictions become a little more accurate.

![alt text](https://github.com/cawley/phase_array/blob/adb77d2a6ff5f12d40eb4c314bd67f72104a255c/files/layers.gif)

### ReLU (Rectified Linear Unit) Functions

1.  `relu(Z)`: Applies the ReLU activation function elementwise on the input `Z`. ReLU function is max(0, Z), and it introduces non-linearity in the network, enabling the network to learn complex patterns.
2.  `relu_backward(dA, Z)`: Implements the backward propagation for a single ReLU unit. It calculates the gradient of the loss with respect to the pre-activation value.

### Parameter Initialization
3. `initialize_parameters(layer_dims)`: Initializes weights randomly and biases to zeros for each layer in our network. It takes a list where each element represents the number of units in the corresponding layer. This random initialization helps in breaking the symmetry during backpropagation and ensures each neuron learns different features.

### Forward Propagation 
4. `conv_forward(A_prev, W, b, hparameters)`: Implements the forward propagation for a convolution function. It performs the convolution of `W` over `A_prev` (the activations of the previous layer) and adds the bias `b`. This is a key operation in Convolutional Neural Networks.
5.  `relu_forward(Z)`: Implements the forward propagation for the ReLU activation function.
6.  `pool_forward(A_prev, hparameters, mode='max')`: Implements the forward propagation for a pooling function. This function reduces the spatial size of the representation to reduce the amount of parameters and computation in the network, and it also helps control overfitting.

### Backward Propagation
7. `conv_backward(dZ, cache)`: Implements the backward propagation for a convolution function. This calculates the gradients with respect to the loss to update the parameters during the training phase.
8.  `relu_backward(dA, cache)`: Implements the backward propagation for a single ReLU unit. This calculates the gradient of the loss with respect to the pre-activation value.
9.  `create_mask_from_window(x)`: This is a helper function used during the backpropagation through a maxpooling layer. It creates a "mask" matrix which keeps track of where the maximum of the matrix is. This is necessary for the pooling_backward function.
10.  `pool_backward(dA, cache, mode='max')`: Implements the backward propagation for a pooling function. This function calculates the gradient for the pooling layer.

### Model 
11. `model()`: This is the main function where the whole neural network is put together. It includes the process of forward propagation, calculating the cost, backward propagation, and updating the parameters. It supports three types of optimization methods: gradient descent (gd), momentum, and Adam. The function loops over `num_epochs`, where in each epoch, it creates mini batches of the input data, performs forward propagation, computes cost, performs backward propagation, and updates the parameters.

### Training the model: 
Training this neural network involves calling the `model()` function and passing in the necessary parameters. These parameters include the training data `X` and `Y`, the structure of the neural network `layers_dims`, the optimization method to use, learning rate, size of mini-batches, beta parameters for momentum and Adam optimizers, a small number `epsilon` to prevent division by zero in Adam optimizer, number of epochs, and whether to print the cost during training.
The training data `X` is the input data, where each column corresponds to a flattened image. `Y` are the true labels of the images. The structure of the neural network `layers_dims` is a list.
