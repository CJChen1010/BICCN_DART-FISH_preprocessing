This repository is used to document custom codes in Zhang lab to preprocess BICCN DART-FISH images. To run the custom codes, we install the required python packages in conda virtual environment, "DF_201012" and install SimpleElastix. 

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
```
