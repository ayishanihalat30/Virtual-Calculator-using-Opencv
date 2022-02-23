import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import time
class Button:
    def __init__(self,pos,width,height,value):
        self.pos=pos
        self.width=width
        self.height=height
        self.value=value
    def draw(self,frame):
        cv.rectangle(frame,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(225,225,225),cv.FILLED)
        cv.rectangle(frame,self.pos,(self.pos[0]+self.width,self.pos[1]+self.height),(50,50,50),3)
        cv.putText(frame, self.value, (self.pos[0]+ 40,self.pos[1] + 60), cv.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
    def checkclick(self,i,j):
        if self.pos[0]<i<self.pos[0]+self.width and \
                self.pos[1]<j<self.pos[1]+self.height:
            cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),cv.FILLED)
            cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv.putText(frame, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv.FONT_HERSHEY_PLAIN, 5, (0, 0, 0),5)
            return True
        else:
            return False
vid=cv.VideoCapture(0)
vid.set(3,1280)
vid.set(4,720)
detector=HandDetector(detectionCon=0.8,maxHands=1)
#button crtn
buttonlistvalues=[['7','8','9','*'],
                  ['4','5','6','-'],
                  ['1','2','3','+'],
                  ['0','/','.','=']]
buttonlist=[]
for i in range(4):
    for j in range(4):
        ipos=i*100+800
        jpos=j*100+150
        buttonlist.append(Button((ipos,jpos),100,100,buttonlistvalues[j][i]))
myeqn=' '
delaycounter=0
while True:
    ret,frame=vid.read()
    frame=cv.flip(frame,1)
    hands,frame=detector.findHands(frame,flipType=False)
    cv.rectangle(frame,(800,50),(800+400,70+100) , (225, 225, 225), cv.FILLED)
    cv.rectangle(frame, (800,50),(800+400,70+100) , (50, 50, 50), 3)

    #draw all button
    for button in buttonlist:
        button.draw(frame)


    #check for hand
    if hands:
       lmList= hands[0]['lmList']
       length,_,frame=detector.findDistance(lmList[8],lmList[12],frame)
       print(length)
       i,j=lmList[8]
       if length<50:
          for x,button in enumerate(buttonlist):
              if button.checkclick(i,j) and delaycounter==0:
                  myvalue=buttonlistvalues[int(x%4)][int(x/4)]
                  if myvalue== "=":
                      myeqn=str(eval(myeqn))
                  else:
                      myeqn+=myvalue
                  delaycounter=1
    #avoiding duplicates
    if delaycounter!=0:
        delaycounter +=1
        if delaycounter > 10:
            delaycounter = 0
    #displaying the result
    cv.putText(frame, myeqn, (810, 120), cv.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)
    #Image show
    cv.imshow('image',frame)
    key=cv.waitKey(1)
    if key==ord('c'):
        myeqn=' '
    if key == ord('k'):
        break