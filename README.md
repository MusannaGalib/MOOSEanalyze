Package Name: pyMOOSE
Version: 1.0.0
Description:
-------------
pyMOOSE is a Python package designed to facilitate advanced analysis and visualization of scientific data, particularly focusing on post-processing simulation results. With a range of functions to generate contour plots, analyze variables over lines, and integrate with common scientific computing tools, pyMOOSE aims to streamline the workflow for researchers and engineers.

Installation:
--------------
To install pyMOOSE, run the following command in your terminal:

pip install pyMOOSE

Usage:
------
Here's how to get started with pyMOOSE:
There are 2 different ways

For windows:
Update 
```python
cd /d \path\to\Paraview\bin
PvPython \path\to\main_wrapper.py
```
Double click on the windows_run.bat file 


Running from main_wrapper.py
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

## Authors
This Software is developed by Musanna Galib


## Citing This Work
If you use this software in your research, please cite the following paper:


```python
BibTeX entry:
@article{YourPaper,
  title={Title of Your Paper},
  author={Your Name},
  journal={Journal/Conference},
  year={2024},
  publisher={Publisher}
}
```

### Contact, questions, and contributing
If you have questions, please don't hesitate to reach out to galibubc[at]student[dot]ubc[dot]ca

If you find a bug or have a proposal for a feature, please post it in the Issues. If you have a question, topic, or issue that isn't obviously one of those, try our GitHub Disucssions.

If your post is related to the framework/package, please post in the issues/discussion on that repository. 

