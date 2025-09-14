from ij import IJ, WindowManager
from ij.io import DirectoryChooser
from java.io import File

# Function to close an image
def close_image(title):
    if WindowManager.getWindow(title) is not None:
        IJ.selectWindow(title)
        IJ.run("Close")

# Prompt to choose extracted images/cores
dc = DirectoryChooser("Select the primary folder")
dir = dc.getDirectory()

# Determine the base directory to place processed_cores parallel to cores
baseDir = dir
processedDir = baseDir + "Processed_Cores/" 

# Get a list of subfolders in the primary directory (all the extracted cores)
subfolders = File(dir).listFiles()

# Only create the "processed_cores" directory if there are subfolders
if any(folder.isDirectory() for folder in subfolders):
    File(processedDir).mkdir()

# Process each subfolder if it is a directory
for folder in subfolders:
    if folder.isDirectory():
        subDir = folder.getAbsolutePath() + "/"
        processedSubDir = processedDir + folder.getName() + "/"

        # Create the corresponding subdirectory in processed_cores
        File(processedSubDir).mkdir()

        # Process each image in the subdirectory
        imageList = File(subDir).list()
        for imageName in imageList:
            if imageName.endswith(".tif"):  # Ensure only .tifs are processed
                # Open the image
                IJ.open(subDir + imageName)
                originalImage = imageName

                # Perform Colour Deconvolution
                IJ.run("Colour Deconvolution", "vectors=[H AEC] hide")

                # Define the new image names after deconvolution to close and not include the residual channel
                colour1 = originalImage + "-(Colour_1)"
                colour2 = originalImage + "-(Colour_2)"
                colour3 = originalImage + "-(Colour_3)"

                # Close the residual channel
                close_image(colour3)

                mergedImage = None
                # Merge channels
                IJ.run("Merge Channels...", "c1=" + colour1 + " c2=" + colour2 + " create")
                mergedImage = "Composite"

                # Close the color images
                close_image(colour1)
                close_image(colour2)

                # Convert the merged image to grayscale and invert
                IJ.selectWindow(mergedImage)
                imp = IJ.getImage()  # Get the current image
                imp.setProp("CompositeProjection", "null")
                imp.setDisplayMode(IJ.GRAYSCALE)
                IJ.run(imp, "Invert", "stack")

                # Set scale to the scanned known resolution
                IJ.run("Set Scale...", "distance=1 known=0.25 unit=um")

                # Save the grayscale image
                grayscaleImage = originalImage.split('.')[0] + "_grayscale.tif"
                IJ.saveAs("Tiff", processedSubDir + grayscaleImage)

                # Close the images after processing is done    
                close_image(grayscaleImage)
                close_image(originalImage)

print("Processing complete.")


