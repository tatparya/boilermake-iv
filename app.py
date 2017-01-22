import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture

class SampleListener(Leap.Listener):

    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    frameCount = 0

    avg_vals = { 'Thumb':0, 'Index':0, 'Middle':0, 'Ring':0, 'Pinky':0 }

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print("connected!")

    def resetValues(self):
        avg_vals = {'Thumb': 0, 'Index': 0, 'Middle': 0, 'Ring': 0, 'Pinky': 0}

    def on_frame(self, controller):
        # print "Frame available!"
        frame = controller.frame()
        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #     frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if( self.frameCount == 0 ):
            self.resetValues()

        #   Get hands
        for hand in frame.hands:
            handType = "LEFT" if  hand.is_left else "RIGHT"

            # print " %s, id, %d, position: %s" % (
            #     handType, hand.id, hand.palm_position
            # )

            palmNormal = hand.palm_normal

            #   Get fingers
            for finger in hand.fingers:
                # print " %s finger" % (
                #     self.finger_names[finger.type]
                # )
                fingerAngle = finger.direction.angle_to(palmNormal) * 57.2958
                self.avg_vals[self.finger_names[finger.type]] = (self.avg_vals[self.finger_names[finger.type]] + fingerAngle) / 2;

                #print "Angle from palm normal: %f" % (fingerAngle)

        self.frameCount += 1

        # print( self.frameCount )

        if(self.frameCount == 5):
            #   Print avg values
            print (self.avg_vals)
            self.frameCount = 0

def analyzeFrame( listenerObj, currentFrame ):
    print "Frame available!"
    frame = currentFrame
    # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
    #     frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

    #   Get hands
    for hand in frame.hands:
        handType = "LEFT" if  hand.is_left else "RIGHT"

        # print " %s, id, %d, position: %s" % (
        #     handType, hand.id, hand.palm_position
        # )

        palmNormal = hand.palm_normal

        #   Get fingers
        for finger in hand.fingers:
            # print " %s finger" % (
            #     listenerObj.finger_names[finger.type]
            # )
            fingerAngle = finger.direction.angle_to(palmNormal) * 57.2958
            listenerObj.avg_vals[listenerObj.finger_names[finger.type]] = fingerAngle

    #   Print avg values
    print (listenerObj.avg_vals)

def main():
    #	Create sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    #	Have sample listener receive events from the controller
    # controller.add_listener(listener)

    #	Infinite process
    # print ("Press Enter to quit...")
    # try:
    #     sys.stdin.readline()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     #	Remove sample listener when done
    #     controller.remove_listener(listener)

    c = "blah"

    while c != "$":
        print 'Please enter training character:'
        c = sys.stdin.readline()
        print ("You enetered %s" % (c))

        currentFrame = controller.frame()
        analyzeFrame(listener, currentFrame)

        # listener.on_frame( controller )

    controller.remove_listener(listener)

if __name__ == "__main__":
    main()
