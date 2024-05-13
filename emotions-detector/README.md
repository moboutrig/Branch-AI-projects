
## Emotion Detector
This application **detects the emotion on a face** from a **webcam** video stream.

Emotion detection is one of the most researched topics in the modern-day machine learning arena. The ability to accurately detect and identify an emotion opens up numerous doors for Advanced Human Computer Interaction. 
The facial emotions that can be detected and classified by this system are **Happy, Sad, Angry, Surprise, Fear, Disgust and Neutral**.

## Usage
First, access the project and install dependencies : 
```
cd path/to/emotion-detector
pip install -r requirements.txt
```

and run the *main.py* file :

**Windows/Linux**
```
python3 src/main.py
```
**Linux only (or Unix-Like OS)**
```
bash run.sh
```

Once the program has started, your **webcam** will light up and a window will open.
Stand in front of the webcam and check that the program detects your face. A **blue rectangle will appear around detected faces**. Facial recognition is relatively imprecise, so blue squares may appear briefly on the screen, but this has no major impact on the results obtained.

When a face is detected, you'll see the **detected emotion** at the bottom left of the screen, as well as a percentage corresponding to the **certainty of the result according to the AI**.

![App Screenshot](screenshots/Screenshot%20from%202024-02-24%2018-18-16.png)

![App Screenshot](screenshots/Screenshot%20from%202024-02-24%2018-21-13.png)


