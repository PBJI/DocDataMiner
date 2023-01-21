import glob
import cv2
from sys import argv
from os import remove as remove
from os.path import exists

def image_filter(files):
    file_list = files
    if "list" not in str(type(files)):
        if "str" not in str(type(files)):
            raise Exception("Neither list of paths nor string")
        elif not exists(files):
            raise Exception("No path found")
        else:
            file_list = glob.glob(files)
    q = 0
    for i in file_list:
        try:
            img = cv2.imread(i)
            cv2.imshow("Preview", img)

            okay = True
            while(okay):
                key = cv2.waitKey(0)
                if key == 110:
                    try:
                        remove(i)
                        print(i + " Deleted")
                        okay = False
                    except Exception as e:
                        print(e)
                elif key == 121:
                    okay = False
                    print(i + " Not to be Deleted")
                elif key == 113:
                    q = 1
                    print("Quitted")
                    break
                else:
                    print(str(key) + " is not the right key type either y or n")
            cv2.destroyAllWindows()
            
            if (q == 1):
                break
        except Exception as e:
            print(e)
            
if __name__ == "__main__":
    try:
        image_list = glob.glob(argv[1])
    except:
        image_list = glob.glob("*")
    
    image_filter(image_list)
