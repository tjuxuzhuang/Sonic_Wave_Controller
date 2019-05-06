import config
from Data_Processing.data_processing import get_data

import model.fc_cnn_model as fc_model
import model.unet_raw as unet_raw_model



# wrapping all the data pre-processing steps in the get_data() function
train_data,train_label,test_data,test_label = get_data()



# wrapping all the model bulding steps in the get_model() function
model = fc_model.get_model()



"""




"""