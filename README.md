# Sonic_Wave_Controller

2019.05.06

## Quick Start

Read the config file and make some changes based on you computer settings.

## Project Structure

- root folder: main.py for running and config.py for changing settings .

  ```python
  # revise machine index number to quickly change between devices.
  machine = 2
  ```

  ```python
  # choose one unused number for your device
  if machine == 0 :
      # macbook
      project_path = "/Users/Waybaba/PycharmProjects/Machine_learning/MyProject/"
      data_path = "/Users/Waybaba/PycharmProjects/Machine_learning/Date_and_Else/variables/"
      use_GPU = False
      assert os.path.exists(project_path),"File path error, Check the config file !!!"
      print("Running on Macbook ...")
  ```

- model: some pre-defined models which can be imported in the main.py.

- Data_Processing: all modules related to data processing.

- hardware_part: for raspberry-Pi based delay signal generator.

- others: other related file.

