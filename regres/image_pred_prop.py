import numpy as np
import time
import random


def relu(Z):
    return np.maximum(0, Z)


def relu_backward(dA, Z):
    dZ = np.array(dA, copy=True)
    dZ[Z <= 0] = 0
    return dZ


def initialize_parameters(layer_dims):
    np.random.seed(1)
    parameters = {}
    L = len(layer_dims)

    for l in range(1, L):
        parameters["W" + str(l)] = np.random.randn(
            layer_dims[l], layer_dims[l - 1]
        ) / np.sqrt(layer_dims[l - 1])
        parameters["b" + str(l)] = np.zeros((layer_dims[l], 1))

    return parameters


def conv_forward(A_prev, W, b, hparameters):
    # dimensions from A_prev shape
    (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape

    # dimensions from W shape
    (f, f, n_C_prev, n_C) = W.shape

    # stride from hyperparameters
    stride = hparameters["stride"]

    # padding from hyperparameters
    pad = hparameters["pad"]

    # dimensions of  CONV output
    n_H = int((n_H_prev - f + 2 * pad) / stride) + 1
    n_W = int((n_W_prev - f + 2 * pad) / stride) + 1

    # output volume Z with zeros
    Z = np.zeros((m, n_H, n_W, n_C))

    # A_prev_pad by padding A_prev
    A_prev_pad = np.pad(A_prev, ((0, 0), (pad, pad), (pad, pad), (0, 0)), "constant")

    for i in range(m):  # Loop over  batch of training examples
        a_prev_pad = A_prev_pad[i]  # Select ith training example padded activation
        for h in range(n_H):  # Loop over vertical axis of  output volume
            for w in range(n_W):  # Loop over horizontal axis of  output volume
                for c in range(n_C):  # Loop over channels of  output volume
                    # Find  corners of  current "slice"
                    vert_start = h * stride
                    vert_end = vert_start + f
                    horiz_start = w * stride
                    horiz_end = horiz_start + f

                    # use  corners to define  slice from a_prev_pad
                    a_slice_prev = a_prev_pad[
                        vert_start:vert_end, horiz_start:horiz_end, :
                    ]

                    # convolve slice with correct filter W and bias b return one output neuron
                    Z[i, h, w, c] = (
                        np.sum(np.multiply(a_slice_prev, W[..., c])) + b[..., c]
                    )

    # output shape
    assert Z.shape == (m, n_H, n_W, n_C)

    # cache for backprop
    cache = (A_prev, W, b, hparameters)

    return Z, cache


def relu_forward(Z):
    A = np.maximum(0, Z)  # ReLU activation

    assert A.shape == Z.shape

    cache = Z  # We store Z to use it later in backpropagation

    return A, cache


def pool_forward(A_prev, hparameters, mode="max"):
    # get dimensions from input shape
    (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape

    # get hyperparameters from "hparameters"
    f = hparameters["f"]  # filter size
    stride = hparameters["stride"]

    # Define dimensions of  output
    n_H = int(1 + (n_H_prev - f) / stride)
    n_W = int(1 + (n_W_prev - f) / stride)
    n_C = n_C_prev

    # Initialize output matrix A
    A = np.zeros((m, n_H, n_W, n_C))

    for i in range(m):  # loop over  training examples
        for h in range(n_H):  # loop on  vertical axis
            for w in range(n_W):  # loop on  horizontal axis
                for c in range(n_C):  # loop over  channels (depth)
                    # Find  corners of  current "slice" (≈4 lines)
                    vert_start = h * stride
                    vert_end = vert_start + f
                    horiz_start = w * stride
                    horiz_end = horiz_start + f

                    # Use  corners to define  current slice on  ith training example of A_prev
                    a_prev_slice = A_prev[
                        i, vert_start:vert_end, horiz_start:horiz_end, c
                    ]

                    # Compute  pooling operation on  slice
                    if mode == "max":
                        A[i, h, w, c] = np.max(a_prev_slice)

    # Store  input and hparameters in "cache" for pool_backward()
    cache = (A_prev, hparameters)

    # Making sure your output shape is correct
    assert A.shape == (m, n_H, n_W, n_C)

    return A, cache


def conv_backward(dZ, cache):
    # get information from  "cache"
    (A_prev, W, b, hparameters) = cache

    # get dimensions from A_prev shape
    (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape

    # get dimensions from W shape
    (f, f, n_C_prev, n_C) = W.shape

    # get information from "hparameters"
    stride = hparameters["stride"]
    pad = hparameters["pad"]

    # get dimensions from dZ shape
    (m, n_H, n_W, n_C) = dZ.shape

    # make dA_prev, dW, db with correct shapes
    dA_prev = np.zeros((m, n_H_prev, n_W_prev, n_C_prev))
    dW = np.zeros((f, f, n_C_prev, n_C))
    db = np.zeros((1, 1, 1, n_C))

    # add paddingto A_prev and dA_prev
    A_prev_pad = np.pad(A_prev, ((0, 0), (pad, pad), (pad, pad), (0, 0)), "constant")
    dA_prev_pad = np.pad(dA_prev, ((0, 0), (pad, pad), (pad, pad), (0, 0)), "constant")

    for i in range(m):  # loop over training examples
        # select ith training example from A_prev_pad and dA_prev_pad
        a_prev_pad = A_prev_pad[i]
        da_prev_pad = dA_prev_pad[i]

        for h in range(n_H):  # loop over vertical axis of  output volume
            for w in range(n_W):  # loop over horizontal axis of  output volume
                for c in range(n_C):  # loop over  channels of  output volume
                    # Find  corners of  current "slice"
                    vert_start = h
                    vert_end = vert_start + f
                    horiz_start = w
                    horiz_end = horiz_start + f

                    # use corners to define  slice from a_prev_pad
                    a_slice = a_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :]

                    # update gradients for window and filter parameters using code formulas given above
                    da_prev_pad[vert_start:vert_end, horiz_start:horiz_end, :] += (
                        W[:, :, :, c] * dZ[i, h, w, c]
                    )
                    dW[:, :, :, c] += a_slice * dZ[i, h, w, c]
                    db[:, :, :, c] += dZ[i, h, w, c]

        # let ith training example dA_prev be unpaded da_prev_pad
        dA_prev[i, :, :, :] = da_prev_pad[pad:-pad, pad:-pad, :]

    assert dA_prev.shape == (m, n_H_prev, n_W_prev, n_C_prev)

    return dA_prev, dW, db


def relu_backward(dA, cache):
    Z = cache
    dZ = np.array(dA, copy=True)  # converting dz to a correct object

    # z <= 0 --> dz = 0
    dZ[Z <= 0] = 0

    assert dZ.shape == Z.shape

    return dZ


def create_mask_from_window(x):
    mask = x == np.max(x)
    return mask


def pool_backward(dA, cache, mode="max"):
    # get information from cache
    (A_prev, hparameters) = cache

    # get hyperparameters from "hparameters"
    stride = hparameters["stride"]
    f = hparameters["f"]

    # dimensions of A_prev shape and dA shape
    m, n_H_prev, n_W_prev, n_C_prev = A_prev.shape
    m, n_H, n_W, n_C = dA.shape

    dA_prev = np.zeros(A_prev.shape)

    # loop over training examples
    for i in range(m):
        # select training example from A_prev
        a_prev = A_prev[i]
        for h in range(n_H):  # loop on vertical axis
            for w in range(n_W):  # loop on horizontal axis
                for c in range(n_C):  # loop over channels (depth)
                    # corners of current slice
                    vert_start = h
                    vert_end = vert_start + f
                    horiz_start = w
                    horiz_end = horiz_start + f

                    if mode == "max":
                        # corners and c to define current slice from a_prev
                        a_prev_slice = a_prev[
                            vert_start:vert_end, horiz_start:horiz_end, c
                        ]
                        # mask from a_prev_slice
                        mask = create_mask_from_window(a_prev_slice)
                        # dA = dA_prev + (mask multiplied by correct entry of dA)
                        dA_prev[
                            i, vert_start:vert_end, horiz_start:horiz_end, c
                        ] += np.multiply(mask, dA[i, h, w, c])

    assert dA_prev.shape == A_prev.shape

    return dA_prev


def model(
    X,
    Y,
    layers_dims,
    optimizer,
    learning_rate=0.0075,
    mini_batch_size=64,
    beta=0.9,
    beta1=0.9,
    beta2=0.999,
    epsilon=1e-8,
    num_epochs=10000,
    print_cost=True,
):
    costs = []  # keep track of cost

    parameters = initialize_parameters(layers_dims)

    if optimizer == "gd":
        pass  # no initialization required for gradient descent
    elif optimizer == "momentum":
        v = initialize_velocity(parameters)
    elif optimizer == "adam":
        v, s = initialize_adam(parameters)

    # optimizer loop
    for i in range(num_epochs):
        minibatches = random_mini_batches(X, Y, mini_batch_size)

        for minibatch in minibatches:
            (minibatch_X, minibatch_Y) = minibatch

            # forward prop
            a3, caches = forward_propagation(minibatch_X, parameters)

            # find cost
            cost = compute_cost(a3, minibatch_Y)

            # backprop
            grads = backward_propagation(minibatch_X, minibatch_Y, caches)

            # update params
            if optimizer == "gd":
                parameters = update_parameters_with_gd(parameters, grads, learning_rate)
            elif optimizer == "momentum":
                parameters, v = update_parameters_with_momentum(
                    parameters, grads, v, beta, learning_rate
                )
            elif optimizer == "adam":
                t = t + 1  # Adam counter
                parameters, v, s = update_parameters_with_adam(
                    parameters, grads, v, s, t, learning_rate, beta1, beta2, epsilon
                )

        if print_cost and i % 1000 == 0:
            print("Cost after epoch %i: %f" % (i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)

    return parameters
