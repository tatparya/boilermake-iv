import numpy as np
from sklearn.naive_bayes import GaussianNB
import Leap, sys
import os

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky', 'TI', 'IM', 'MR', 'RP']
    angles = {'Thumb': 0, 'Index': 0, 'Middle': 0, 'Ring': 0, 'Pinky': 0, 'TI': 0, 'IM': 0, 'MR': 0, 'RP': 0}
    def on_frame(self, controller):
        pass
    def reset_values(self):
        self.angles = {'Thumb': 0, 'Index': 0, 'Middle': 0, 'Ring': 0, 'Pinky': 0, 'TI': 0, 'IM': 0, 'MR': 0, 'RP': 0}

def analyzeFrame( listenerObj, currentFrame, letter ):
    frame = currentFrame
    listenerObj.reset_values()
    for hand in frame.hands:
        palmNormal = hand.palm_normal
        prevFingerDirection = Leap.Vector(0, 0, 0)
        #   Get fingers
        for finger in hand.fingers:
            fingerAngle = finger.direction.angle_to(palmNormal) * 57.2958
            listenerObj.angles[listenerObj.finger_names[finger.type]] = fingerAngle
            if (finger.type == 1):
                listenerObj.angles['TI'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
            if (finger.type == 2):
                listenerObj.angles['IM'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
            if (finger.type == 3):
                listenerObj.angles['MR'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
            if (finger.type == 4):
                listenerObj.angles['RP'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
            prevFingerDirection = finger.direction

    #   Print avg values
    #print (listenerObj.angles)
    return listenerObj.angles

def main():
    # read training set
    print "Reading training set... "
    features = np.loadtxt('training_set.txt', usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8), delimiter='\t')
    values = np.loadtxt('training_set.txt', dtype='c', usecols=(9), unpack = True, delimiter='\t')

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
            p=(clf.predict([[angles['Thumb'],angles['Index'], angles['Middle'], angles['Ring'], angles['Pinky'], angles['TI'], angles['IM'],angles['MR'], angles['RP']]]))
            if( p == "1" ):
                print( "I love Purdue" )
                os.system("say I love Purdue")
            else:
                print (p)
                os.system("say %s"%(p[0]))
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()