
import config
import numpy as np
import random
from scipy.io import loadmat

def get_data():
    # fetch raw data
    fields = []
    phases = []
    for i in range(191)[1:]:
        # data (500,500)
        fields.append(loadmat(r""+config.data_path + "sonic_data_2/" + "height0.14_"+str(i)+"randfield.mat")['capacity']) # name_template: "height0.14_1randfield.mat"
        # lable (8,8)
        phases.append(loadmat(r""+config.data_path + "sonic_data_2/" + "height0.14_"+str(i)+"randphase.mat")['initial_phase']) # name_template: "height0.14_1randphase"

    # reshape into numpy
    fields = np.array(fields)
    phases = np.array(phases)

    # norm field globally
    fields = fields - np.full(fields.shape,fields.min()) / (np.full(fields.shape,fields.max()) - (np.full(fields.shape,fields.min())))

    # norm phase separately
    for index_x in range(190):
        phases[index_x] = (phases[index_x] - np.full(phases[index_x].shape,phases[index_x].min())) / (np.full(phases[index_x].shape,phases[index_x].max()) - np.full(phases[index_x].shape,phases[index_x].min()))

    # split and shuffle
    state = np.random.get_state()
    np.random.shuffle(fields)
    np.random.set_state(state)
    np.random.shuffle(phases)
    num_of_date = fields.shape[0]
    train_num = int((4 * num_of_date) / 5)
    input_train, input_test, label_train, label_test = fields[0:train_num], fields[train_num:], phases[0:train_num], phases[train_num:]
    return input_train,label_train,input_test,label_test


if __name__ == '__main__':
    x = get_data()
    print("finish.")