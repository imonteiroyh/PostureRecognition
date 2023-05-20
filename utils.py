import numpy as np

def pad_right_down_corner(image, stride, pad_value):
    height = image.shape[0]
    width = image.shape[1]

    pad = [0 for _ in range(4)]

    if height % stride != 0:
        pad[2] = stride - (height % stride)

    if width % stride != 0:
        pad[3] = stride - (width % stride)

    image_padded = image

    pad_up = np.tile(image_padded[0:1, :, :] * 0 + pad_value, (pad[0], 1, 1))
    image_padded = np.concatenate((pad_up, image_padded), axis=0)

    pad_left = np.tile(image_padded[:, 0:1, :] * 0 + pad_value, (1, pad[1], 1))
    image_padded = np.concatenate((pad_left, image_padded), axis=1)

    pad_down = np.tile(image_padded[-1:, :, :] * 0 + pad_value, (pad[2], 1, 1))
    image_padded = np.concatenate((pad_down, image_padded), axis=0)

    pad_left = np.tile(image_padded[:, -1:, :] * 0 + pad_value, (1, pad[3], 1))
    image_padded = np.concatenate((pad_left, image_padded), axis=1)

    return image_padded, pad