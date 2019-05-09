import config
import numpy as np
import matplotlib.pyplot as plt

# input a 3D array
# convert into gray-image
# save into project_path-Others-image
def convert2img(input_array,img_name):
    save_path = config.project_path + "Others/image/"
    shape = input_array.shape[:2]
    plt.imshow(input_array.reshape(shape), cmap=plt.cm.gray, interpolation='nearest')
    plt.savefig(save_path + img_name)
    print("save_img: " + img_name)
