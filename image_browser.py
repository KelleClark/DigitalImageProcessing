from tkinter import *
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import argparse
import cv2
import numpy as np
import os
import sys
import filetype


# set up an a list for files
images = []

filetypes = []
columns = []
rows = []
pixels = []
# index for the list of images in the browser
count = 0


# Get and parse the arguments
def get_args():
    parser = argparse.ArgumentParser(description='Image browser v1.0')
    parser.add_argument('path', metavar='dir',
                        help='The root directory to view photos in')
    parser.add_argument('--rows', type=int,  default=720,
                        help='Max number of rows on screen  (Default is 720)')
    parser.add_argument('--cols',  type=int, default=1080,
                        help='Max number of columns on screen (Default is 1080)')

    args = parser.parse_args()
    return(args)

# Check for images in the path and save the exact path to each
#   image in a list.
def load_path(path):
    global images
    rootDir = os.path.join(path)
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            pos_img = dirName + "/" + fname
            if cv2.haveImageReader(pos_img): # if it is a readable image
                images.append(pos_img)  #add it to the list of images
                filetypes.append(filetype.guess(pos_img).mime)
                columns.append("")
                rows.append("")
                pixels.append("")
    # If there is a problem with the given path, exit
    if len(images) == 0:
        print("Invalid path or there are no images in path")
        sys.exit(1)
    
 
# Load the first image from the directory as opencv
def opencv_img(count):
    # read and convert image
    image = cv2.imread(images[count])
    columns[count] = str(image.shape[1])
    rows[count] = str(image.shape[0])
    pixels[count] = str(image.shape[1] * image.shape[0])
    scale = min(get_args().rows / image.shape[0], get_args().cols / image.shape[1])
    srcTri = np.array([[0, 0], [image.shape[1] - 1, 0], [0, image.shape[0] - 1]]).astype(np.float32)
    dstTri = np.array( [[0, 0], [int(image.shape[1] * scale), 0], [0, int(image.shape[0] * scale)]] ).astype(np.float32)
    warp_mat = cv2.getAffineTransform(srcTri, dstTri)
    image = cv2.warpAffine(image, warp_mat, (image.shape[1], image.shape[0]))
    image = image[0:int(image.shape[0] * scale), 0:int(image.shape[1] * scale)]
    return(image)

# Convert it to ImageTK
# necessary to use cvtColor to correct to expected RGB color
def convert_img(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To proper format for tk
    im = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=im)
    return(imgtk)

# Wrapper to load the image for display
def load_img(count):
    return convert_img(opencv_img(count))


# Show metadata
def meta(event):
    global count
    impath  = images[count]
    info = os.lstat(impath)
    showinfo("Image Metadata", info)

# Go to next image    
def next_img(event):
    global count
    if count >= len(images) -1:
        count = -1 # -1 to offset regular function
    count = count + 1  # Next image in the list
    imgtk = load_img(count)
    tex = extract_meta()
    #Update the display
    label['image'] = imgtk
    label['text'] = tex[1]+"\nfrom "+tex[0]+"\n"+columns[count]+" x "+rows[count]+" ("+pixels[count]+" pixels)\nImage type: "+filetypes[count]+"\nFile size: "+str(os.lstat(images[count]).st_size)+" bytes"
    label.photo = imgtk
        
# Go to prior image    
def prev_img(event):
    global count
    if count <= 0:
        count = (len(images) - 1) + 1 # +1 to offset regular function
    count = count - 1  # Prior image in the list
    imgtk = load_img(count)
    tex = extract_meta()
    #Update the display
    label['image'] = imgtk
    label['text'] = tex[1]+"\nfrom "+tex[0]+"\n"+columns[count]+" x "+rows[count]+" ("+pixels[count]+" pixels)\nImage type: "+filetypes[count]+"\nFile size: "+str(os.lstat(images[count]).st_size)+" bytes"
    label.photo = imgtk

# Blur the image using Gaussianblur
def blur_img(event):
    global count
    imgtk = convert_img(cv2.GaussianBlur(opencv_img(count), (15, 15), cv2.BORDER_DEFAULT))
    tex = extract_meta()
    #Update the display
    label['image'] = imgtk
    label['text'] = tex[1]+"\nfrom "+tex[0]+"\n"+columns[count]+" x "+rows[count]+" ("+pixels[count]+" pixels)\nImage type: "+filetypes[count]+"\nFile size: "+str(os.lstat(images[count]).st_size)+" bytes"
    label.photo = imgtk 
    

# Apply an affine transformation
def affine_trans(event):
    global count
    src = cv2.cvtColor(opencv_img(count), cv2.COLOR_BGR2RGB)
    srcTri = np.array( [[0, 0], [src.shape[1] - 1, 0], [0, src.shape[0] - 1]] ).astype(np.float32)
    dstTri = np.array( [[0, src.shape[1]*0.33], [src.shape[1]*0.85, src.shape[0]*0.25], [src.shape[1]*0.15, src.shape[0]*0.7]] ).astype(np.float32)
    warp_mat = cv2.getAffineTransform(srcTri, dstTri)
    dst = cv2.warpAffine(src, warp_mat,(src.shape[1],src.shape[0]))
    imgtk = convert_img(dst)
    tex = extract_meta()
    #Update the display
    label['image'] = imgtk
    label['text'] = tex[1]+"\nfrom "+tex[0]+"\n"+columns[count]+" x "+rows[count]+" ("+pixels[count]+" pixels)\nImage type: "+filetypes[count]+"\nFile size: "+str(os.lstat(images[count]).st_size)+" bytes"
    label.photo = imgtk
                 
#Exit the program  
def quit_img(event):
    root.destroy() #Kill the display
    sys.exit(0)

def extract_meta():
    global count
    ind = images[count].rindex("/")
    ans = ['','']
    if ind != -1:
        ans[0] = images[count][0:ind]
        ans[1]= images[count][ind+1:]

    return ans



def main():
    
    args = get_args()

    # Root window
    global root
    root = Tk()
    load_path(args.path)
    imgtk = load_img(count)
    tex = extract_meta()

    # Put it in the display window
    global label
    label = Label(root, text = tex[1]+"\nfrom "+tex[0]+"\n"+columns[count]+" x "+rows[count]+" ("+pixels[count]+" pixels)\nImage type: "+filetypes[count]+"\nFile size: "+str(os.lstat(images[count]).st_size)+" bytes", compound = RIGHT, image=imgtk)
    label.pack()


    frame = Frame()
    frame.pack()

    btn_previous = Button(
        master = frame,
        text = "Previous",
        underline = 0
    )
    btn_previous.grid(row = 0, column = 0)
    btn_previous.bind('<ButtonRelease-1>', prev_img)

    btn_metadata = Button(
        master = frame,
        text = "Metadata",
        underline = 0
    )
    btn_metadata.grid(row = 0, column = 1)
    btn_metadata.bind('<ButtonRelease-1>', meta)

    btn_affine = Button(
        master = frame,
        text = "AffineT",
        underline = 0
    )
    btn_affine.grid(row = 0, column = 2)
    btn_affine.bind('<ButtonRelease-1>', affine_trans)

    btn_next = Button(
        master = frame,
        text = "Next",
        underline = 0
    )
    btn_next.grid(row = 0, column = 3)
    btn_next.bind('<ButtonRelease-1>', next_img)

    root.bind('<n>', next_img)
    root.bind('<m>', meta)
    root.bind("<p>", prev_img)
    root.bind("<q>", quit_img)
    root.bind("<b>", blur_img)

    root.mainloop() # Start the GUI

if __name__ == "__main__":
    main()
