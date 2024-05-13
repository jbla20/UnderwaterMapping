from rosbag import Bag
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import cv2
import glob
from pathlib import Path

def extract_frame_from_bags(bag_dir, time=0.0, save=False):
    bridge = CvBridge()
    
    # Loop through each bag 
    for file_path in sorted(glob.glob(bag_dir + "/*.bag")):
        # Get the next path in the bag sequence (starts with original path)
        print("Extracting frame from: " + file_path)
        
        # Open the bag
        with Bag(file_path, "r") as bag:
            # Loop through each message in the source bag
            for topic, msg, t in bag.read_messages(topics=["/cam0/image_raw"]):
                if t.to_sec() < time:
                    continue
                
                try:
                    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
                except CvBridgeError as e:
                    print(e)
                
                cv2.putText(cv_image, Path(file_path).stem, (10,30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 255, 255), 2)
                
                if save:
                    save_path = "/storage/extraction/UnderwaterMapping/Utilities/Bag-conversion/Output/" + Path(file_path).stem + ".png"
                    cv2.imwrite(save_path, cv_image)
                else:
                    cv2.imshow("Image window", cv_image)
                    cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
                

if __name__ == "__main__":
    extract_frame_from_bags("/storage/data/bags/1,2", 0, save=True)