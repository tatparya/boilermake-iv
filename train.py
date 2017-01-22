################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    angles = {'Thumb': 0, 'Index': 0, 'Middle': 0, 'Ring': 0, 'Pinky': 0, 'TI': 0, 'IM': 0, 'MR': 0, 'RP': 0}
    def on_frame(self, controller):
        frame = controller.frame()
        self.reset_values()
        for hand in frame.hands:
            palmNormal = hand.palm_normal
            prevFingerDirection = Leap.Vector(0,0,0)
            #   Get fingers
            for finger in hand.fingers:
                fingerAngle = finger.direction.angle_to(palmNormal) * 57.2958
                self.angles[self.finger_names[finger.type]] = fingerAngle
                if(finger.type == 1):
                    self.angles['TI'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
                if (finger.type == 2):
                    self.angles['IM'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
                if (finger.type == 3):
                    self.angles['MR'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
                if (finger.type == 4):
                    self.angles['RP'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
                prevFingerDirection = finger.direction

        # Print avg values
        # print (listenerObj.angles)
        print self.angles

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
                listenerObj.angles['TI'] = finger.direction.angle_to(prevFingerDirection)  * 57.2958
            if (finger.type == 2):
                listenerObj.angles['IM'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
            if (finger.type == 3):
                listenerObj.angles['MR'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
            if (finger.type == 4):
                listenerObj.angles['RP'] = finger.direction.angle_to(prevFingerDirection) * 57.2958
            prevFingerDirection = finger.direction

    #   Print avg values
    if len(frame.hands) != 0:
        print (listenerObj.angles)
        with open("training_set.txt", 'a') as feature_file:
            feature_file.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%s" % (listenerObj.angles['Thumb'], listenerObj.angles['Index'], listenerObj.angles['Middle'], listenerObj.angles['Ring'], listenerObj.angles['Pinky'], listenerObj.angles['TI'], listenerObj.angles['IM'], listenerObj.angles['MR'], listenerObj.angles['RP'], letter))


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        while True:
            print 'Please enter training character:'
            tc = sys.stdin.readline()
            currentFrame = controller.frame()
            analyzeFrame(listener, currentFrame, tc)
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
