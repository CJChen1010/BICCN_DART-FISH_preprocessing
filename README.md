This repository is used to document custom codes in Zhang lab to preprocess BICCN DART-FISH images. To run the custom codes, we install the required python packages in conda virtual environment, "DF_201012" and install SimpleElastix. 

# Create virtual environment and install required packages
Run these commands to build SimpleElastix in the DF_201012 environment.
```
mkdir ~/path/to/SimpleElastix_201012
cd ~/path/to/SimpleElastix_201012
mv DF201012.ymal ~/path/to/SimpleElastix_201012
```
Create and activate DF_201012 virtual environment
```
conda env create -f DF_201012_env.yml
conda activate DF_201012
```
Clone and build SimpleElastix
```
git clone https://github.com/SuperElastix/SimpleElastix
mkdir build
cd build
PYTHON_LIBRARY=~/anaconda3/envs/DF_201012/bin/python
cmake ../SimpleElastix/SuperBuild
make -j8
cd SimpleITK-build/Wrapping/Python
python Packaging/setup.py install --user
```
Download  FIJI and model weights for cellpose
Download FIJI from https://downloads.imagej.net/fiji/latest/fiji-linux64.zip and unzip it.
Cellpose's weights can be downloaded using the function "download_model_weights" in cellpose.models.

# Set up the structure of directories
```
project
│   README.md
│   file001.txt    
│
└───folder1
│   │   file011.txt
│   │   file012.txt
│   │
│   └───subfolder1
│       │   file111.txt
│       │   file112.txt
│       │   ...
│   
└───folder2
    │   file021.txt
    │   file022.txt
```
