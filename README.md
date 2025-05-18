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
All data and codes to process DART-FISH images are kept in the same directory with the following structure of directories. 
## 0_Raw
0_Raw directory contails all tiff files from one DART-FISH experiments. The examples below shows the output tiff files from Leica SP8 microscope. Each tiff file is named after "round_name1"_s*_z*_ch*.tif format, where s is the field of view (FOV) number, z the number for z-stack, and ch the fluorescent channel.
## 1_Projected

## 2_Registered

## 3_Decoded

## 4_CellAssigment

## Codes
```
Experiment    
|___0_Raw
│   │___"Round_name1"
│   │       "round_name1"_s*_z*_ch00.tif
|   |       "round_name1"_s*_z*_ch01.tif
|   |       "round_name1"_s*_z*_ch02.tif
|   |       "round_name1"_s*_z*_ch03.tif
│   |        ...
|   |___"Round_name2"
│   │       "round_name1"_s*_z*_ch00.tif
|   |       "round_name1"_s*_z*_ch01.tif
|   |       "round_name1"_s*_z*_ch02.tif
|   |       "round_name1"_s*_z*_ch03.tif
│   |        ...
|___1_Projected
|   │___"FOV001"    
|   │       MIP_"round_name1"_FOV001_ch00.tif
|   |       MIP_"round_name1"_FOV001_ch01.tif
|   |       MIP_"round_name1"_FOV001_ch02.tif
|   |       MIP_"round_name1"_FOV001_ch03.tif
|   |       ...
|   |___"FOV002"
|   |       ...
|___2_Registered
|___3_Decoded
|___4_CellAssignment
|___Codes
|   |___"code_lib"
|   |___"_codebook"
```
# Maximal intensity projection and image registration

# Image stitching

# Starfish decoding

# Nucleus segmentation and assigment of decoded spots to nuclei

