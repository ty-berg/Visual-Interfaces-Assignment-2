import cv2
import numpy as np
from matplotlib import pyplot as plt
import os


#calculating color differentials
fig = plt.figure(figsize=(60,40))
channels = [0,1,2]
sizes=[32,32,32]
ranges = [0,256,0,256,0,256]

rows = 40
cols = 5

position = 1

folder_dir = "/Users/tylerberg/Desktop/Visual Interfaces Assignment 2/images"
top={}
total_score = 0
for image in sorted(os.listdir(folder_dir)):
    # check if the image ends with ppm
    if (image.endswith(".ppm")):
        input_path = os.path.join(folder_dir, image)
        q = cv2.imread(input_path)
        q = cv2.cvtColor(q, cv2.COLOR_BGR2RGB)
        histQ = cv2.calcHist([q], channels, None, sizes, ranges)
        for img in os.listdir(folder_dir):
            if(img.endswith(".ppm")):
                input_path = os.path.join(folder_dir, img)
                t = cv2.imread(input_path, cv2.COLOR_BGR2RGB)
                t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                if img != image:
                    histT = cv2.calcHist([t], channels, None, sizes, ranges)
                    subtraction = histQ - histT
                    sum = 0
                    for i in subtraction:
                        for j in i:
                            for x in j:
                                sum = sum + np.absolute(x)
                    norm = sum/(2*60*89)
                    top[img]=norm
        top = sorted(top.items(),key=lambda item: item[1])
        total=0
        best = []
        for key in top:
            best.append(int((str(key[0])[1:3])))
            total = total + 1
            if total == 3:
                break
        num = 0
        score = 0
        ax = fig.add_subplot(rows, cols, position)
        ax.set_title(image[1:3])
        plt.imshow(q)
        plt.axis('off')
        position = position + 1
        file = open('Crowd.txt', 'r')
        for line in file:
            num = num + 1
            if num == int(image[1:3]):
                n = 0
                index = 0
                for i in line.split():
                    n = n+1
                    if n in best:
                        bindex = best.index(n)
                        fname = best[bindex]
                        if fname < 10:
                            fname = "i0" + str(fname) + ".ppm"
                        else:
                            fname = "i" + str(fname) + ".ppm"
                        path = os.path.join(folder_dir,fname)
                        t = cv2.imread(path)
                        t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                        ax = fig.add_subplot(rows,cols,position)
                        ax.set_title((path)[len(path)-6:len(path)-4] + " Crowd: " + i)
                        plt.imshow(t)
                        plt.axis('off')
                        position = position + 1
                        index = index + 1
                        score = score + int(i)
                break
        file.close()
        ax = fig.add_subplot(rows,cols,position)
        ax.set_title("Score: " + str(score), y = .01)
        plt.axis('off')
        if position < 200:
            position = position + 1
        total_score = total_score + score
        top = {}
ax = fig.add_subplot(rows,cols,position)
ax.set_title("Score: " + str(score), y = .01)
plt.axis('off')
plt.subplots_adjust(left=.42,bottom=.1,right=.54,top=.88,wspace=0, hspace=.5)
plt.title("Total Score: " + str(total_score), x=-2, y=60.5, fontsize=50)
plt.savefig("ScoresColors.pdf", format="pdf")
              
#calculating texture differentials
fig = plt.figure(figsize=(60,40))

rows = 40
cols = 5

position = 1

folder_dir = "/Users/tylerberg/Desktop/Visual Interfaces Assignment 2/images"
top={}
total_score = 0
for image in sorted(os.listdir(folder_dir)):
    # check if the image ends with ppm
    if (image.endswith(".ppm")):
        input_path = os.path.join(folder_dir, image)
        q = cv2.imread(input_path)
        for i in range(60):
            for j in range(89):
                q[i,j] = np.sum(q[i,j])/3
        lapQ = cv2.Laplacian(q,cv2.CV_16S,3)
        lapQ = np.uint8(np.absolute(lapQ))
        histQ = cv2.calcHist([lapQ], [0], None, [138], [0,256])
        for img in os.listdir(folder_dir):
            if(img.endswith(".ppm")):
                input_path = os.path.join(folder_dir, img)
                t = cv2.imread(input_path)
                for i in range(60):
                    for j in range(89):
                        t[i,j] = np.sum(t[i,j])/3
                if img != image:
                    lapT = cv2.Laplacian(t,cv2.CV_16S,3)
                    lapT = np.uint8(np.absolute(lapT))
                    histT = cv2.calcHist([lapT],[0],None,[138],[0,256])
                    subtraction = histQ - histT
                    sum = 0
                    for i in subtraction:
                        for j in i:
                            sum = sum + np.absolute(j)
                    norm = sum/(2*60*89)
                    top[img]=norm
        top = sorted(top.items(),key=lambda item: item[1])
        total=0
        best = []
        for key in top:
            best.append(int((str(key[0])[1:3])))
            total = total + 1
            if total == 3:
                break
        num = 0
        score = 0
        file = open('Crowd.txt', 'r')
        for line in file:
            num = num + 1
            if num == int(image[1:3]):
                n = 0
                index = 0
                fname = "i" + image[1:3] + ".ppm"
                path = os.path.join(folder_dir,fname)
                q = cv2.imread(path)
                q = cv2.cvtColor(q, cv2.COLOR_BGR2RGB)
                ax = fig.add_subplot(rows, cols, position)
                ax.set_title(image[1:3])
                plt.imshow(q)
                plt.axis('off')
                position = position + 1
                for i in line.split():
                    n = n+1
                    if n in best:
                        bindex = best.index(n)
                        fname = best[bindex]
                        if fname < 10:
                            fname = "i0" + str(fname) + ".ppm"
                        else:
                            fname = "i" + str(fname) + ".ppm"
                        path = os.path.join(folder_dir,fname)
                        t = cv2.imread(path)
                        t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                        ax = fig.add_subplot(rows,cols,position)
                        ax.set_title((path)[len(path)-6:len(path)-4] + " Crowd: " + i)
                        plt.imshow(t)
                        plt.axis('off')
                        position = position + 1
                        index = index + 1
                        score = score + int(i)
                break
        file.close()
        ax = fig.add_subplot(rows,cols,position)
        ax.set_title("Score: " + str(score), y = .01)
        plt.axis('off')
        if position < 200:
            position = position + 1
        total_score = total_score + score
        top = {}
ax = fig.add_subplot(rows,cols,position)
ax.set_title("Score: " + str(score), y = .01)
plt.axis('off')
plt.subplots_adjust(left=.42,bottom=.1,right=.54,top=.88,wspace=0, hspace=.5)
plt.title("Total Score: " + str(total_score), x=-2, y=60.5, fontsize=50)
plt.savefig("ScoresTexture.pdf", format="pdf")


#calculating shape differentials
fig = plt.figure(figsize=(60,40))

rows = 40
cols = 5

position = 1

folder_dir = "/Users/tylerberg/Desktop/Visual Interfaces Assignment 2/images"
top={}
total_score = 0
for image in sorted(os.listdir(folder_dir)):
    # check if the image ends with ppm
    if (image.endswith(".ppm")):
        input_path = os.path.join(folder_dir, image)
        q = cv2.imread(input_path)
        for i in range(60):
            for j in range(89):
                if np.sum(q[i,j])/3 > 55:
                    q[i,j] = [255,255,255]
                else:
                    q[i,j] = [0,0,0]
        for img in os.listdir(folder_dir):
            if(img.endswith(".ppm")):
                input_path = os.path.join(folder_dir, img)
                t = cv2.imread(input_path)
                for i in range(60):
                    for j in range(89):
                        if np.sum(t[i,j])/3 > 55:
                            t[i,j] = [255,255,255]
                        else:
                            t[i,j] = [0,0,0]
                sum = 0
                if img != image:
                    for row in range(60):
                        for col in range(89):
                            if q[row][col][0] != t[row][col][0]:
                                sum += 1
                    norm = sum/(60*89)
                    top[img]=norm
        top = sorted(top.items(),key=lambda item: item[1])
        total=0
        best = []
        for key in top:
            best.append(int((str(key[0])[1:3])))
            total = total + 1
            if total == 3:
                break
        num = 0
        score = 0
        file = open('Crowd.txt', 'r')
        for line in file:
            num = num + 1
            if num == int(image[1:3]):
                n = 0
                index = 0
                fname = "i" + image[1:3] + ".ppm"
                path = os.path.join(folder_dir,fname)
                q = cv2.imread(path)
                q = cv2.cvtColor(q, cv2.COLOR_BGR2RGB)
                ax = fig.add_subplot(rows, cols, position)
                ax.set_title(image[1:3])
                plt.imshow(q)
                plt.axis('off')
                position = position + 1
                for i in line.split():
                    n = n+1
                    if n in best:
                        bindex = best.index(n)
                        fname = best[bindex]
                        if fname < 10:
                            fname = "i0" + str(fname) + ".ppm"
                        else:
                            fname = "i" + str(fname) + ".ppm"
                        path = os.path.join(folder_dir,fname)
                        t = cv2.imread(path)
                        t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                        ax = fig.add_subplot(rows,cols,position)
                        ax.set_title((path)[len(path)-6:len(path)-4] + " Crowd: " + i)
                        plt.imshow(t)
                        plt.axis('off')
                        position = position + 1
                        index = index + 1
                        score = score + int(i)
                break
        file.close()
        ax = fig.add_subplot(rows,cols,position)
        ax.set_title("Score: " + str(score), y = .01)
        plt.axis('off')
        if position < 200:
            position = position + 1
        total_score = total_score + score
        top = {}
ax = fig.add_subplot(rows,cols,position)
ax.set_title("Score: " + str(score), y = .01)
plt.axis('off')
plt.subplots_adjust(left=.42,bottom=.1,right=.54,top=.88,wspace=0, hspace=.5)
plt.title("Total Score: " + str(total_score), x=-2, y=60.5, fontsize=50)
plt.savefig("ScoresShape.pdf", format="pdf")

#calculating symmetry
fig = plt.figure(figsize=(60,40))

rows = 40
cols = 5

position = 1

folder_dir = "/Users/tylerberg/Desktop/Visual Interfaces Assignment 2/images"
top={}
total_score = 0
for image in sorted(os.listdir(folder_dir)):
    # check if the image ends with ppm
    if (image.endswith(".ppm")):
        input_path = os.path.join(folder_dir, image)
        q = cv2.imread(input_path)
        for i in range(60):
            for j in range(89):
                if np.sum(q[i,j])/3 > 40:
                    q[i,j] = [255,255,255]
                else:
                    q[i,j] = [0,0,0]
        distQ = 0
        for i in range(60):
            for j in range(44):
                if q[i,j][0]!=q[59-i,88-j][0]:
                    distQ += 1
        distQ = distQ/(60*44)
        for img in os.listdir(folder_dir):
            if(img.endswith(".ppm")):
                input_path = os.path.join(folder_dir, img)
                t = cv2.imread(input_path)
                for i in range(60):
                    for j in range(89):
                        #46
                        if np.sum(t[i,j])/3 > 40:
                            t[i,j] = [255,255,255]
                        else:
                            t[i,j] = [0,0,0]
                distT = 0
                for i in range(60):
                    for j in range(44):
                        if t[i,j][0]!=t[59-i,88-j][0]:
                            distT += 1
                distT = distT/(60*44)
                sum = 0
                if img != image:
                    top[img]=np.absolute(distQ-distT)
        top = sorted(top.items(),key=lambda item: item[1])
        total=0
        best = []
        for key in top:
            best.append(int((str(key[0])[1:3])))
            total = total + 1
            if total == 3:
                break
        num = 0
        score = 0
        file = open('Crowd.txt', 'r')
        for line in file:
            num = num + 1
            if num == int(image[1:3]):
                n = 0
                index = 0
                fname = "i" + image[1:3] + ".ppm"
                path = os.path.join(folder_dir,fname)
                q = cv2.imread(path)
                q = cv2.cvtColor(q, cv2.COLOR_BGR2RGB)
                ax = fig.add_subplot(rows, cols, position)
                ax.set_title(image[1:3])
                plt.imshow(q)
                plt.axis('off')
                position = position + 1
                for i in line.split():
                    n = n+1
                    if n in best:
                        bindex = best.index(n)
                        fname = best[bindex]
                        if fname < 10:
                            fname = "i0" + str(fname) + ".ppm"
                        else:
                            fname = "i" + str(fname) + ".ppm"
                        path = os.path.join(folder_dir,fname)
                        t = cv2.imread(path)
                        t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                        ax = fig.add_subplot(rows,cols,position)
                        ax.set_title((path)[len(path)-6:len(path)-4] + " Crowd: " + i)
                        plt.imshow(t)
                        plt.axis('off')
                        position = position + 1
                        index = index + 1
                        score = score + int(i)
                break
        file.close()
        ax = fig.add_subplot(rows,cols,position)
        ax.set_title("Score: " + str(score), y = .01)
        plt.axis('off')
        if position < 200:
            position = position + 1
        total_score = total_score + score
        top = {}
ax = fig.add_subplot(rows,cols,position)
ax.set_title("Score: " + str(score), y = .01)
plt.axis('off')
plt.subplots_adjust(left=.42,bottom=.1,right=.54,top=.88,wspace=0, hspace=.5)
plt.title("Total Score: " + str(total_score), x=-2, y=60.5, fontsize=50)
plt.savefig("ScoresSymmetry.pdf", format="pdf")


#calculating total differentials
#creating plot figure for displaying images
fig = plt.figure(figsize=(60,40))
#channels 0, 1, and 2 refer to the red, green, and blue pixel values respectively
channels = [0,1,2]
#bin sizes for histogram adjusted to optimize total score
#blue size is lowest since humans don't distinguish between blues as much as reds and greens
sizes=[32,32,12]
#ranges to capture all RGB values
ranges = [0,256,0,256,0,256]

#rows and columns for plot of queries and targets
rows = 40
cols = 5

position = 1

#folder for images
folder_dir = "/Users/tylerberg/Desktop/Visual Interfaces Assignment 2/images"
top={}
total_score = 0
for image in sorted(os.listdir(folder_dir)):
    # check if the image ends with ppm
    if (image.endswith(".ppm")):
        input_path = os.path.join(folder_dir, image)
        q = cv2.imread(input_path)
        #convert from BGR to RGB for correct display
        q = cv2.cvtColor(q, cv2.COLOR_BGR2RGB)
        #color
        #calculate 3D histogram using channels, sizes, and ranges detailed above
        #learned about calcHist() from: https://docs.opencv.org/4.x/d6/dc7/group__imgproc__hist.html#ga4b2b5fd75503ff9e6844cc4dcdaed35d
        #also learned about 3D histograms from: https://en.wikipedia.org/wiki/Color_histogram#Example_1
        histQ = cv2.calcHist([q], channels, None, sizes, ranges)
        #texture
        #loop through pixels and convert to grayscale by dividing sum of RGB by 3
        for i in range(60):
            for j in range(89):
                q[i,j] = np.sum(q[i,j])/3
        #used OpenCV Laplacian function using a depth of signed 16 bit to prevent overflow
        #kernel size of 3 to use the correct matrix detailed in the assignment
        #learned about Laplacian from: https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gad78703e4c8fe703d479c1860d76429e6
        lapQ = cv2.Laplacian(q,cv2.CV_16S,3)
        #convert back to 8 bit unsigned with absolute values of laplacian
        lapQ = np.uint8(np.absolute(lapQ))        
        histLapQ = cv2.calcHist([lapQ], [0], None, [138], [0,256])
        #shape
        #copy image
        qShape = q.copy()
        #loop through pixels and convert to binary by converting pixel values over 55 to 255 and all others to 0
        for row in range(60):
            for col in range(89):
                if qShape[row,col][0] > 55:
                    qShape[row,col] = [255,255,255]
                else:
                    qShape[row,col] = [0,0,0]
        #symmetry
        distQ = 0
        #loop through all pixels and convert to binary by converting pixel values over 46 to 255 and all others to 0
        for row in range(60):
            for col in range(89):
                if q[row,col][0] > 46:
                    q[row,col] = [255,255,255]
                else:
                    q[row,col] = [0,0,0]
        #loop through right and left half of image and compare the mirrored pixels
        for i in range(60):
            for j in range(44):
                if q[i,j][0]==q[59-i,88-j][0]:
                    distQ += 1
        #normalize
        distQ = distQ/(60*44)
        #loop thorugh all images in the images folder
        for img in os.listdir(folder_dir):
            #find .ppm images in folder
            if(img.endswith(".ppm")):
                #get query target image path
                input_path = os.path.join(folder_dir, img)
                t = cv2.imread(input_path, cv2.COLOR_BGR2RGB)
                #convert image from BGR to RGB for correct display
                t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                if img != image:
                    #color
                    #calculate 3D histogram using channels, sizes, and ranges detailed above
                    histT = cv2.calcHist([t], channels, None, sizes, ranges)
                    #subtract the target histogram from the query histogram
                    subtraction = histQ - histT
                    sum = 0
                    #loop through differences and sum the absolute values
                    for i in subtraction:
                        for j in i:
                            for x in j:
                                sum = sum + np.absolute(x)
                    #normalize
                    normColor = sum/(2*60*89)
                    #32 28 28 12
                    norm = .32*normColor
                    #texture
                    #loop through pixels and convert to grayscale by dividing sum of RGB by 3
                    for i in range(60):
                        for j in range(89):
                            t[i,j] = np.sum(t[i,j])/3
                    #used OpenCV Laplacian function using a depth of signed 16 bit to prevent overflow
                    #kernel size of 3 to use the correct matrix detailed in the assignment
                    lapT = cv2.Laplacian(t,cv2.CV_16S,3)
                    #convert back to 8 bit unsigned with absolute values of laplacian
                    lapT = np.uint8(np.absolute(lapT))
                    #calculate a 1D histogram on the laplacian values with channel 0 and bin size 138
                    histLapT = cv2.calcHist([lapT], [0], None, [138], [0,256])
                    #subtract the target histogram from the query histogram
                    subtraction = histLapQ - histLapT
                    sum = 0
                    #loop through differences and sum the absolute values
                    for i in subtraction:
                        for j in i:
                            sum = sum + np.absolute(j)
                    #normalize
                    normText = sum/(2*60*89)
                    norm += .28*normText
                    #shape
                    #copy image
                    tShape = t.copy()
                    sum = 0
                    #loop through pixels and convert to binary by converting pixel values over 55 to 255 and all others to 0
                    for row in range(60):
                        for col in range(89):
                            if tShape[row,col][0]>55:
                                tShape[row,col] = [255,255,255]
                            else:
                                tShape[row,col] = [0,0,0]
                    #loop through binary pixels and compare them with a target image
                    for row in range(60):
                        for col in range(89):
                            #if different add 1 to the sum
                            if qShape[row][col][0] != tShape[row][col][0]:
                                sum += 1
                    #normalize
                    normShape = sum/(60*89)
                    norm += .28*normShape
                    #symmetry
                    distT = 0
                    #loop through all pixels and convert to binary by converting pixel values over 46 to 255 and all others to 0
                    for row in range(60):
                        for col in range(89):
                            if t[row,col][0]>46:
                                t[row,col] = [255,255,255]
                            else:
                                t[row,col] = [0,0,0]
                    #loop through right and left half of image and compare the mirrored pixels
                    for i in range(60):
                        for j in range(44):
                            if t[i,j][0]==t[59-i,88-j][0]:
                                distT += 1
                    #normalize
                    distT = distT/(60*44)
                    normSym = np.absolute(distQ - distT)
                    norm += .12*normSym
                    top[img]=norm
        #sort the dictionary in descending order
        top = sorted(top.items(),key=lambda item: item[1])
        total=0
        best = []
        #add first three images from dictionary to a list
        for key in top:
            best.append(int((str(key[0])[1:3])))
            total = total + 1
            if total == 3:
                break
        num = 0
        score = 0
        file = open('Crowd.txt', 'r')
        #loop through the txt file line by line
        for line in file:
            num = num + 1
            #find the line for the query image
            if num == int(image[1:3]):
                n = 0
                index = 0
                fname = "i" + image[1:3] + ".ppm"
                path = os.path.join(folder_dir,fname)
                q = cv2.imread(path)
                q = cv2.cvtColor(q, cv2.COLOR_BGR2RGB)
                #add query image to plot
                ax = fig.add_subplot(rows, cols, position)
                #label image
                ax.set_title(image[1:3])
                plt.imshow(q)
                plt.axis('off')
                position = position + 1
                #loop through each word in the line
                for i in line.split():
                    n = n+1
                    #find top 3 target images from the list generated earlier
                    if n in best:
                        bindex = best.index(n)
                        fname = best[bindex]
                        if fname < 10:
                            fname = "i0" + str(fname) + ".ppm"
                        else:
                            fname = "i" + str(fname) + ".ppm"
                        path = os.path.join(folder_dir,fname)
                        t = cv2.imread(path)
                        t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
                        #add the target images to the plot
                        ax = fig.add_subplot(rows,cols,position)
                        #label the images
                        ax.set_title((path)[len(path)-6:len(path)-4] + " Crowd: " + i)
                        plt.imshow(t)
                        plt.axis('off')
                        position = position + 1
                        index = index + 1
                        #add votes from txt file to score for row
                        score = score + int(i)
                break
        file.close()
        #add last image of row to plot
        ax = fig.add_subplot(rows,cols,position)
        #add score for row
        ax.set_title("Score: " + str(score), y = .01)
        plt.axis('off')
        if position < 200:
            position = position + 1
        #add row score to total score
        total_score = total_score + score
        top = {}
#add final image to plot
ax = fig.add_subplot(rows,cols,position)
#add score for final row
ax.set_title("Score: " + str(score), y = .01)
plt.axis('off')
plt.subplots_adjust(left=.42,bottom=.1,right=.54,top=.88,wspace=0, hspace=.5)
#add total score
plt.title("Total Score: " + str(total_score), x=-2, y=60.5, fontsize=50)
#save as PDF
plt.savefig("ScoresTotal.pdf", format="pdf")


    


            










