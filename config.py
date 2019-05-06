# This file is for config
# some parameters may have to be changed to adapted to different terminal
# 

import os
import sys
import inspect
import re

# wangwei-macbook: 0
# wangwei-PC: 1
# wangwei-实验室服务器: 2
# wangwei-Windows: 3
# zhuangxu: 4
machine = 3

print("===================================================================================")
# 根据上面的值进行三选一
if machine == 0 :
    # macbook
    project_path = "/Users/Waybaba/PycharmProjects/Machine_learning/MyProject/"
    data_path = "/Users/Waybaba/PycharmProjects/Machine_learning/Date_and_Else/variables/"
    use_GPU = False
    assert os.path.exists(project_path),"File path error, Check the config file !!!"
    print("Running on Macbook ...")

elif machine ==1 :
    # 远程控制的PC
    project_path = "/home/waybaba/Documents/Code/MyProject/"
    data_path = "/home/waybaba/Documents/Code/Data_and_Else/variables/"
    use_GPU = False
    assert os.path.exists(project_path),"File path error, Check the config file !!!"
    print("Running on PC ...")

elif machine == 2:
    # 实验室服务器
    gpu_choice = '1'
    os.environ['CUDA_VISIBLE_DEVICES']=gpu_choice
    project_path = "/wangwei/Crisscrossing_Convolution/Code/"
    data_path = "/wangwei/variables/"
    use_GPU = True
    assert os.path.exists(project_path),"File path error, Check the config file !!!"
    print("Running on lib614 GPU computer ...")
    print("Using GPU "+gpu_choice+" ...")

elif machine == 3:
    # Windows
    project_path = "C:/Users/Way/iCloudDrive/Research/Crisscrossing_Convolution/Code/"
    data_path = 'E:/Data_for_Code/'
    use_GPU = False
    assert os.path.exists(project_path), "File path error, Check the config file !!!"
    print("Running on Windows computer ...")
elif machine == 4:
    # zhuangxu
    project_path = ""
    data_path = ''
    use_GPU = False
    assert os.path.exists(project_path), "File path error, Check the config file !!!"
    print("Running on zhuangxu computer ...")


print("project_path: "+project_path)
print("data_path: "+ data_path)
print("===================================================================================")




sys.path.append(project_path)