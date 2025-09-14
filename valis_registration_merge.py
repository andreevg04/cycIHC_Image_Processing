import pathlib
import os
import cv2
import numpy as np
from valis import registration, feature_detectors


MAX_FEATURES = 7000 #you can set it based on registration result
# Create feature detector that has a lower maximum feature count since its always the same tissue slide
class OrbVggFD_low_fd(feature_detectors.FeatureDD):
   """Uses ORB for feature detection and VGG for feature description"""
   def __init__(self,  kp_detector=cv2.ORB_create(nfeatures=MAX_FEATURES, fastThreshold=0), kp_descriptor=cv2.xfeatures2d.VGG_create(scale_factor=1.25)): 
       #scale_factor can also be increased or decreased based on results and/or memory issues
       super().__init__(kp_detector=kp_detector, kp_descriptor=kp_descriptor)


all_src_dir = "/path/to/directory with each grayscale image to be fused" #following our workflow this would be the folder named processed_cores
dir_list = [d for d in pathlib.Path(all_src_dir).iterdir() if os.path.isdir(d)] # each d is a folder containing the images to be aligned and merged
dst_dir = "path/to/results" #path to the merged images, each in a separate folder following the VALIS documentation


for i, d in enumerate(dir_list):

   print(os.path.split(d)[1])
   # Set `feature_detector_cls` to feature detector that uses fewer features
   registrar = registration.Valis(str(d), dst_dir, feature_detector_cls=OrbVggFD_low_fd, imgs_ordered=True) #ensuring registration will be from the first to the last image


   rigid_registrar, non_rigid_registrar, error_df = registrar.register()

   # Merge channels and save as ome.tiff
   # Valis did not detect channel names in the slide metadata, so create channel name dictionary
   channel_name_dict = {}
   for slide_obj in registrar.slide_dict.values():
       channel_names = ["DAPI", slide_obj.name.split("_")[1]] #the Heamtoxylin backbone will be renamed as DAPI
       channel_name_dict[slide_obj.src_f] = channel_names

   merged_f = os.path.join(registrar.dst_dir, registrar.name + "_merged.ome.tiff")
   registrar.warp_and_merge_slides(dst_f=merged_f, channel_name_dict=channel_name_dict, drop_duplicates=False, Q = 80, compression="jp2k") #you can change Q and the compression if the image is too large or of too low quality

registration.kill_jvm()
