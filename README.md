![PyPI downloads](https://img.shields.io/pypi/dm/your-package-name)
[![Paper](https://img.shields.io/badge/ACS_Energy_Lett-blue)](https://doi.org/your-paper-doi)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-red.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/badge/release-v0.0.1-brightgreen)](https://github.com/MusannaGalib/pyMOOSE)
[![License: MIT](https://img.shields.io/badge/license-MIT_2.0-yellow)](https://opensource.org/licenses/MIT)

# pyMOOSE
pyMOOSE is a Python package designed to facilitate advanced analysis and visualization of post-processing of MOOSE simulation's exodus file format. pyMOOSE python packageis built on Paraview's PvPython module.

## Installation:

To install pyMOOSE, run the following command in your terminal:

```
pip install pyMOOSE
```

## Usage:

Here's how to get started with pyMOOSE:
There are 2 different ways

For windows:
Update ```windows_run.bat``` file
```python
cd /d \path\to\Paraview\bin
PvPython \path\to\main_wrapper.py
```
Double click on the ```windows_run.bat``` file 


Running from ```main_wrapper.py```
```python
cd path\to\Paraview\bin    ---> cd D:/Backup_31_July_2022/Research/Research/MOOSE/ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64/ParaView-5.11.0-RC1-Windows-Python3.9-msvc2017-AMD64/bin/
Run  in command line -----> ./PvPython path/to/main_wrapper.py
or
Run  in command line -----> ./PvPython path/to/MOOSE_post_processsing_paraview.py (This will run in the Default Data Folder)
```
For comparing between different folders manually
```python
    # Specify folder names to process only those folders
    folder_names = ['Bare_Zn','MLD_Alucone_eigen_0.5']
    for specific_time in specific_times:
        compare_folders_at_time(base_directory, specific_times, var_names, folder_names)
```
For comparing between different folders automatically
```python
    # Or, call without specifying folder_names to auto-detect and process all folders
    compare_folders_at_time(base_directory, specific_times, var_names)
```

For comparing the dendrite lengths
```python 
        calculate_max_x_coordinate(base_directory, folder_names)
        plot_points_vs_time_with_max_w(base_directory, folder_names)
```
    Change the following line to define which part of older name to be appeared in the plot legend 
    ```python 
     aniso_value = folder_name.split('aniso')[-1].strip()  #interface/i/aniso
    ```

## Authors
This Software is developed by Musanna Galib


## Citing This Work
If you use this software in your research, please cite the following paper:


```python
BibTeX entry:
@article{YourPaper,
  title={Dendrite Inhibition using Heteroepitaxial Residual Stress in Zn Metal Batteries},
  author={Musanna Galib, Jian Liu, and Mauricio Ponga},
  journal={ACS Energy Lett},
  year={2024},
  publisher={American Chemical Society}
}
```

### Contact, questions, and contributing
If you have questions, please don't hesitate to reach out to galibubc[at]student[dot]ubc[dot]ca

If you find a bug or have a proposal for a feature, please post it in the Issues. If you have a question, topic, or issue that isn't obviously one of those, try our GitHub Disucssions.

If your post is related to the framework/package, please post in the issues/discussion on that repository. 

