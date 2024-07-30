## SETUP

1. To run the project, first create a virtual environment using this command:
`python -m venv myenv`

`myenv/Scripts/activate`

## INSTALLATION

Then, install these libraries by running the two commands given below:
1. pip install git+https://github.com/JaidedAI/EasyOCR.git
2. pip install ultralytics pandas opencv-python numpy scipy opencv-contrib-python filterpy flask


After that, there are 2 ways to run this project:
 
## TESTING

### WAY 1: MAKING DETECTIONS ON DEMO VIDEO, SAVING THE RESULTS, AND THEN LOADING THE INTERFACE AND TESTING IT:

1. First run the command `python main.py` to create a CSV file containing the detection results, OCR results etc on the video. This csv file is stored in the assets/results folder named as "test.csv"

2. Then run the command `python add_missing_data.py` to format and interpolate the "test.csv" file. This script will create a new file called "test_interpolated.csv" file stored in the assets/results folder as well.

3. Then run the command `python visualize.py`. This will take the "test_interpolated.csv" file and the input video (stored in "assets/demo.mp4") and overlay the results of the "test_interpolated.csv" file onto the video. It will store the resultant video in the "assets/results/out.mp4" location.

4. Then run the command `python interface.py` to launch the interface. It will ask for a list of license plates as inputs (for example: ATVET342,VETV25,VTGV35) and then you have to submit the list. After a few seconds, you will get the output video in the interface with full detections, highlighting authorized plates in "GREEN" and unauthorized plates in "RED".


### WAY 2: DIRECTLY RUNNING THE INTERFACE:
1. You can directly run the interface and test on the already saved video in the "assets/results/out.mp4" path. To do so, run the command `python interface.py` to launch the interface. It will ask for a list of license plates as inputs (for example: ATVET342,VETV25,VTGV35) and then you have to submit the list. After a few seconds, you will get the output video in the interface with full detections, highlighting authorized plates in "GREEN" and unauthorized plates in "RED".