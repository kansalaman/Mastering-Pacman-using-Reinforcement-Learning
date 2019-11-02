import numpy as np

# Preprocessing function: github.com/ageron/tiny-dqn
def preprocess(image):
    pacman_colour = np.array([210, 164, 74]).mean()
    cropped_image = image[1:176:2, ::2]
    grey_scaled = cropped_image.mean(axis=2)
    grey_scaled[grey_scaled == pacman_colour] = 0
    norm_image = (grey_scaled - 128)/128 - 1

    return np.expand_dims(norm_image.reshape(88,80,1), axis=0)

def mergeFrames(images, fps_factor):
    img_from_frames = np.expand_dims(np.zeros((88,80,1), np.float64), axis=0)

    for image in images:
        img_from_frames += image

    if (len(images)) < fps_factor:
        return img_from_frames / fps_factor
    else:
        return img_from_frames / fps_factor
