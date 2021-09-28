Goka Tharun Kumar --- ASSIGNMENT --- Dimensionless technologies

--- Used Python notebook and script

--- Used Libraries OpenCV, PIL, Numpy, OS

--- Algorithm:

step1: Reading Background and Threat images using OpenCV
step2: Converting read images to RGB Space
step3: Creating a white backgrounded empty image using Numpy of size same as Background Image
step3: Getting Pixels which are having other than white color from Threat images (which is nothing but getting pixels of a threat object)
step4: Finding contours of the threat object in Threat image (no of contours will be more than one since differnet colors are there in a threat object)
step5: Filling contours of the threat object with single color (white)
step6: Finding contours of the threat object from step5 (no of contours will be only 1)
step7: Getting Bounding box of the object using contours found in step6
step8: Cropping threat object from the Threat image
step9: Pasting the cropped threat object on white backgrounded empty image created in step3
step10: Rotating the white backgrounded image (which also now contain a threat object) with 45 degrees
step11: After rotating there will be some Black colored portions in an image so filling those black colored portions with White color (using findcountors and fillPoly of opencv)
step12: Now adding two images Background image, and image processed from step11 using "alpha*overlay + (1-alpha)*output + gamma"
step13: Saving the output of step12


--- Can also be done in an advanced and intelligent way using ML

step1: Labelling some threat objects (segmentation-mask)
step2: Labelling some Baggages (segmentation-mask)
step3: Build a Image segmentation model to detect the contours of threat object
step4: Build a Image segmentation model to detect the contours borders of Baggage
step5: Analyse the contours of Baggage and we can place the threat object at required choice of place on Baggage


--- Drawback of OpenCV Algo: There is no gaurantee for given every threat object will be correctly placed inside the Baggage
--- Can be overcomed using ML.

