import math
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


def get_angle(a, b, c=None):
    try:
        if not c:
            a_coordinate_x, a_coordinate_y = a
            b_coordinate_x, b_coordinate_y = b

            if (a_coordinate_x == b_coordinate_x):
                return 90

            angle = math.degrees(math.atan2(abs(b_coordinate_y - a_coordinate_y), abs(b_coordinate_x - a_coordinate_x)))

            return angle
        else:
            distance_a = get_distance(b, c)
            distance_b = get_distance(c, a)
            distance_c = get_distance(a, b)

            angle = math.degrees(math.acos((distance_a ** 2 + distance_c ** 2 - distance_b ** 2) / (2 * distance_a * distance_c)))

            return angle

    except:
        return None


def get_distance(a, b, type=None):
    try:
        a_coordinate_x, a_coordinate_y = a
        b_coordinate_x, b_coordinate_y = b

        if not type:
            distance = math.sqrt((b_coordinate_x - a_coordinate_x) ** 2 + (b_coordinate_y - a_coordinate_y) ** 2)
        elif type == 'vertical':
            distance = abs(b_coordinate_y - a_coordinate_y)

        return distance

    except:
        return None
