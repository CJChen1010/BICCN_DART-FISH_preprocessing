# import immac, re, shutil, warnings, sys
import re, shutil, warnings, sys	# Kian: added 201011
from time import time
from datetime import datetime
from code_lib import TwoDimensionalAligner_2_NOR6 as myAligner # Kian: added 201011
from os import chdir, listdir, getcwd, path, makedirs, remove,  walk
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from code_lib import tifffile as tiff # <http://www.lfd.uci.edu/~gohlke/code/tifffile.py> # Kian: added 201011 Chien-Ju editted 201123


# server = "voyager"

# if server.capitalize() == "Voyager":
# 	server_selector = "_Voyager"
# if server.capitalize() == "Miner":
# 	server_selector = ""

# if server.capitalize() == "Voyager":
# 	server_selector = "_Voyager"
# if server.capitalize() == "Miner":
# 	server_selector = ""

def listdirectories(directory='.', pattern = '*'):	# Kian: added 201011
	'''
	listdirectories returns a list of all directories in path
	'''
	directories = []
	for i in next(walk(directory))[1]:
#		if match(pattern, i): 
			directories.append(i)
	directories.sort()
	return directories

def mip_gauss_tiled(rnd, fov, dir_root, dir_output='./MIP_gauss', sigma=0.7, channel_int='ch00'):
	'''
	Modified from Matt Cai's MIP.py 
	Maximum intensity projection along z-axis
	'''
	# get current directory and change to working directory
	current_dir = getcwd()
	
	dir_parent = path.join(dir_root)
	chdir(dir_parent + rnd)
		
	#get all files for position for channel
	image_names = [f for f in listdir('.') if re.match(r'.*_s' + '{:03d}'.format(fov) + r'.*_' + channel_int + r'\.tif', f)]

	# put images of correct z_range in list of array
	nImages = len(image_names)
	image_list = [None]*nImages
	for i in range(len(image_names)):
		image_list[i] = (ndimage.gaussian_filter(plt.imread(image_names[i]), sigma=sigma))
		  
	# change directory back to original
	chdir(current_dir)

	image_stack = np.dstack(image_list)
	
	max_array = np.amax(image_stack, axis=2)
	
	# PIL unable to save uint16 tif file
	# Need to use alternative (like libtiff)
	
	#Make directories if necessary
	if not dir_output.endswith('/'):
		dir_output = "{0}/".format(dir_output)
	#mkreqdir(dir_output)
	if not path.isdir(dir_output + 'FOV{:03d}'.format(fov)):
		makedirs(dir_output + 'FOV{:03d}'.format(fov))
		
	#Change to output dir and save MIP file
	chdir(dir_output)
	tiff.imsave('FOV{:03d}'.format(fov) + '/MIP_' + rnd + '_FOV{:03d}'.format(fov) + '_' + channel_int + '.tif', max_array)
	
	# change directory back to original
	chdir(current_dir)

	
# sample_date = "200316"
# sample_name = "K2000063_1-A-63x-ROI2"	

# name_full = sample_date + '-' + sample_name

#Raw Data Folder
dir_data_raw = "/media/NAS4/Chien-Ju/BICCN_DART-FISH/20220928/"

#Processed data output folder
# dir_data = "/media/Scratch_SSD{}/rque/DART-FISH/".format(server_selector)

#Where MIPs are written to
dir_output = "../1_Projected_NOR6"
if not path.isdir(dir_output):
	makedirs(dir_output)

#Where Aligned MIPs are written to
dir_output_aligned = "../2_Registered_NOR6"
if not path.isdir(dir_output_aligned):
	makedirs(dir_output_aligned)

#rounds
# rnd_list = ["draq5"]
rnd_list = ["anchor", "dc0", "dc1", "dc2", "dc3", "dc4", "dc5", "dc6", "dc7", "draq5"]


#Number of FOVs
n_fovs = 556 #12x3

#sigma for gaussian blur
sigma = 0.7

#Which cycle to align to
cycle_reference = rnd_list[round(len(rnd_list)/2)] # dc3
channel_DIC_reference = 'ch01' # DIC channel for reference cycle
channel_DIC = 'ch01' # DIC channel for (non-reference) decoding cycles (the channel we use for finding alignment parameters)
cycle_other = ['anchor', 'draq5'] # if there are other data-containing folders which need to be aligned but are not names "CycleXX"
channel_DIC_other = {'anchor': 'ch01', 'draq5':'ch01'} # DIC channel for otPher data-containing folders


t0 = time()

#MIP


for rnd in rnd_list:
	if ("draq5" in rnd):
		channel_list = [0, 1]		
	else:
		channel_list = [0, 1, 2, 3]
	

	for channel in channel_list:
		print('Generating MIPs for ' + rnd + ' channel {0} ...'.format(channel))

		for fov in range(n_fovs):
			mip_gauss_tiled(rnd, fov, dir_data_raw, dir_output, sigma = sigma, channel_int="ch0{0}".format(channel))
		print('Done\n')
	
t1 = time()

print('Elapsed time ', t1 - t0)

# # #Align

position_list = listdirectories(path.join(dir_output))
currentTime = datetime.now() 
reportFile = path.join(dir_output_aligned, currentTime.strftime("%Y-%d-%m_%H:%M_SITKAlignment.log"))
sys.stdout = open(reportFile, 'w') # redirecting the stdout to the log file
for position in position_list:
#	position = 'Position{:03d}'.format(posi)
#	cycle_list = ["dc3","dc4","DRAQ5"]
	for rnd in rnd_list:
		print(datetime.now().strftime("%Y-%d-%m_%H:%M:%S: " + str(position) + ', cycle '+ rnd + ' started to align'))
		aligner = myAligner.TwoDimensionalAligner(
				destinationImagesFolder = path.join(dir_output, position), 
				originImagesFolder = path.join(dir_output, position),
				originMatchingChannel = channel_DIC if rnd not in cycle_other else channel_DIC_other[rnd],
				destinationMatchingChannel = channel_DIC_reference, 
				imagesPosition = position, 
				destinationCycle = cycle_reference,
				originCycle = rnd,
				resultDirectory = path.join(dir_output_aligned, position),
				MaximumNumberOfIterations = 400)
		for file in [file for file in listdir() if file.startswith('IterationInfo.0')]:
				if path.isfile(path.join(dir_output_aligned, position, "MetaData", file)): # removing a file with the same name already exists, remove it.
					remove(path.join(dir_output_aligned, position, "MetaData", file))
				shutil.move(src = file, dst = path.join(dir_output_aligned, position, "MetaData"))
			
t2 = time()
sys.stdout = sys.__stdout__ # restoring the stdout pipe to normal
print('Elapsed time ', t2 - t1)

print('Total elapsed time ',  t2 - t0)
 

