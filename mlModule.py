import numpy as np
from sklearn.naive_bayes import GaussianNB
import Leap, sys

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    angles = {'Thumb': 0, 'Index': 0, 'Middle': 0, 'Ring': 0, 'Pinky': 0}
    def on_frame(self, controller):
        pass
    def reset_values(self):
        self.angles = {'Thumb': 0, 'Index': 0, 'Middle': 0, 'Ring': 0, 'Pinky': 0}

def analyzeFrame( listenerObj, currentFrame, letter ):
    frame = currentFrame
    listenerObj.reset_values()
    for hand in frame.hands:
        palmNormal = hand.palm_normal

        #   Get fingers
        for finger in hand.fingers:
            fingerAngle = finger.direction.angle_to(palmNormal) * 57.2958
            listenerObj.angles[listenerObj.finger_names[finger.type]] = fingerAngle

    #   Print avg values
    #print (listenerObj.angles)
    return listenerObj.angles

def main():
    # read training set
    print "Reading training set... "
    features = np.loadtxt('training_set.txt', usecols=(0, 1, 2, 3, 4))
    values = np.loadtxt('training_set.txt', dtype='c', usecols=(5), unpack = True)

    # create classifier
    clf = GaussianNB()
    clf.fit(features, values)

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    # wait for prediction set
    print "Reading prediction set..."

    try:
        while True:
            print "Press ENTER to input coordinates:"
            tc = sys.stdin.readline()
            currentFrame = controller.frame()
            angles = analyzeFrame(listener, currentFrame, tc)
            print angles
            print(clf.predict([[angles['Thumb'],angles['Index'], angles['Middle'], angles['Ring'], angles['Pinky']]]))
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()