from setuptools import setup, find_packages

setup(
    name='pyMOOSE',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'numpy',
        # 'vtk' # Uncomment this if vtk is available through pip
        # 'paraview' # Uncomment this if paraview is available through pip
    ],
    entry_points={
        'console_scripts': [
            'your_script=your_package.module:function',
        ],
    },
    # Additional metadata about your package.
    author='Musanna Galib',  # Replace with your name
    author_email='galibubc@student.ubc.ca',  # Replace with your email
    description="'A Python package for post-processing MOOSE data",
    license="MIT",
    keywords="MOOSE post-processing using Pvpython-paraview",
    url="http://example.com/HelloWorld/",   # project home page, if any
)
