def imageData = getCurrentImageData()
def server = imageData.getServer()

// Define base output path (relative to project)
def imageName = GeneralTools.getNameWithoutExtension(server.getMetadata().getName())
def imageParts = imageName.tokenize('_')
def cycleNumber = imageParts[0]
def marker = imageParts[1]
def blockID = imageParts[2]

def pathOutput = buildFilePath(PROJECT_BASE_DIR, 'TMA_Cores')
mkdirs(pathOutput)

for (core in getTMACoreList()) {
    if (core.isMissing()) {
        println("Core ${core.getName()} is missing. Skipping...")
        continue
    }

    def coreROI = core.getROI()
    def coreID = core.getName()

    // Create folder structure if it doesn't exist
    def coreOutputPath = buildFilePath(pathOutput, coreID)
    mkdirs(coreOutputPath)

    // Define output file name with naming convention: CycleNumber_Marker_CoreID.tif
    def outputFilePath = buildFilePath(coreOutputPath, blockID + "_" + coreID + ".tif")

    // Extract and save the core image
    def requestROI = RegionRequest.createInstance(server.getPath(), 1, coreROI)
    writeImageRegion(server, requestROI, outputFilePath)
}

println('Done')