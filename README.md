[![PyPI downloads](https://img.shields.io/pypi/dm/MOOSEanalyze)](https://pypi.org/project/MOOSEanalyze/) 
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-red.svg)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/badge/release-v0.0.1-brightgreen)](https://github.com/MusannaGalib/MOOSEanalyze)
[![License: MIT](https://img.shields.io/badge/license-MIT_2.0-yellow)](https://opensource.org/licenses/MIT)
<!-- [![Paper](https://img.shields.io/badge/ACS_Energy_Lett-blue)](https://doi.org/your-paper-doi) -->

# MOOSEanalyze
MOOSEanalyze is a Python package designed to facilitate advanced analysis and visualization of post-processing of MOOSE simulation's exodus file format. MOOSEanalyze python packageis built on Paraview's PvPython module.


## Installation:

To install MOOSEanalyze, run the following command in your terminal:

```
pip install MOOSEanalyze
```

## Usage:

Here's how to get started with MOOSEanalyze:
There are 2 different ways

For windows:
Update ```windows_run.bat``` file
```python
cd /d \path\to\Paraview\bin
PvPython \path\to\main_wrapper.py
```
Double click on the ```windows_run.bat``` file 

For Linux:
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
    # call without specifying folder_names to auto-detect and process all folders
    compare_folders_at_time(base_directory, specific_times, var_names)
```

For comparing the dendrite lengths:
```python 
        calculate_max_x_coordinate(base_directory, folder_names)
        plot_points_vs_time_with_max_w(base_directory, folder_names)
```
Go to MOOSE_post_processsing_paraview.py and change the following  ```interface/i/aniso```, based on interface stress, current density or anisotropy cases, respectively
```python 
     # Change the following line to define which part of older name to be appeared in the plot legend 
     aniso_value = folder_name.split('aniso')[-1].strip()  #interface/i/aniso
```

## Authors
This Software is developed by Musanna Galib


## Citing This Work
If you use this software in your research, please cite the following paper:


```python
@misc{galib2025dendritesuppressionznbatteries,
      title={Dendrite Suppression in Zn Batteries Through Hetero-Epitaxial Residual Stresses Shield}, 
      author={Musanna Galib and Amardeep Amardeep and Jian Liu and Mauricio Ponga},
      year={2025},
      eprint={2502.03841},
      archivePrefix={arXiv},
      primaryClass={cond-mat.mtrl-sci},
      url={https://arxiv.org/abs/2502.03841}, 
}
```

### Contact, questions, and contributing
If you have questions, please don't hesitate to reach out to galibubc[at]student[dot]ubc[dot]ca

If you find a bug or have a proposal for a feature, please post it in the Issues. If you have a question, topic, or issue that isn't obviously one of those, try our GitHub Disucssions.

If your post is related to the framework/package, please post in the issues/discussion on that repository. 

