# cycIHC-Image-Processing
Code accompanying our manuscript  
["Spatial Correlation of the Extracellular Matrix to Immune Cell Phenotypes in the Tumor Boundary of Clear Cell Renal Cell Carcinoma Revealed by Cyclic Immunohistochemistry"](https://www.laboratoryinvestigation.org/article/S0023-6837(25)00040-6/fulltext)
## Tutorial

### 1. Core Extraction:
After aquiring all digital images, create new QuPath project and load the images using this naming convention CycleNumber_Marker_BlockID.
Using the TMA dearrayer tool in QuPath select and remove cores that you want or dont want to analyze. 
Run the CoreExtraction.groovy script. This will create a folder called TMA_Cores in the QuPath project directory and each folder in it will have the extracted cores. 

### 2. Color Deconvolution:
Open Fiji and run the script Deconvolution_Grayscale.py. The script will prompt to select the main folder where the extracted cores are. 
After selection, the script will automatically create a folder called "Processed_Cores" where all 2-channel images will be found. 

### 3. Merging and Fusion:
Then setting the path to the "Processed_Cores" folder in the valis_registration_merge.py and selecting a new path for the merged cores (see comment) this script will register and fuse the markers of each core.
For installing VALIS refer to the original documentation https://valis.readthedocs.io/en/latest/.
Examplified Folder Structure is shown in Supplementary Figure S1

Special thanks to Chandler Gatenbee!
