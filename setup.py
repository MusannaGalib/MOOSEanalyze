from setuptools import setup, find_packages

try:
    with open('README.md', 'r') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name='MOOSEanalyze',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.1.5',
        'matplotlib>=3.3.3',
        'numpy>=1.19.4',
        'seaborn>=0.13.2'
        # 'vtk' # Uncomment this if vtk is available through pip
        # 'paraview' # Uncomment this if paraview is available through pip
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'your_script=your_package.module:function',
        ],
    },
    # Additional metadata about your package.
    author='Musanna Galib',  # Replace with your name
    author_email='galibubc@student.ubc.ca',  # Replace with your email
    description="A Python package for post-processing MOOSE data",
    license='MIT',
    license_files=["LICENSE"],
    keywords="MOOSE, Post-processing, Pvpython-paraview",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/MusannaGalib/MOOSEanalyze/",   # project home page, if any
)
