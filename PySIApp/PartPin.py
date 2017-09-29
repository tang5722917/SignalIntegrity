'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from ProjectFile import PartPinConfiguration

# pinOrientation is 't','b','l','r'
# coordinates are relative to part
class PartPin(PartPinConfiguration):
    def __init__(self,pinNumber,pinConnectPoint,pinOrientation,pinNumberVisible=True,pinVisible=True, pinNumberingMatters=True):
        PartPinConfiguration.__init__(self)
        self.SetValue('Number', pinNumber)
        self.SetValue('ConnectionPoint', str(pinConnectPoint))
        self.SetValue('Orientation', pinOrientation)
        self.SetValue('NumberVisible', pinNumberVisible)
        self.SetValue('Visible', pinVisible)
        self.SetValue('NumberingMatters', pinNumberingMatters)
    def DrawPin(self,canvas,grid,partOrigin,color,connected):
        pinConnectionPoint=eval(self.GetValue('ConnectionPoint'))
        startx=(pinConnectionPoint[0]+partOrigin[0])*grid
        starty=(pinConnectionPoint[1]+partOrigin[1])*grid
        endx=startx
        endy=starty
        textGrid=16
        pinOrientation=self.GetValue('Orientation')
        if pinOrientation == 't':
            endy=endy+grid
            textx=startx+textGrid/2
            texty=starty+textGrid/2
        elif pinOrientation == 'b':
            endy=endy-grid
            textx=startx+textGrid/2
            texty=starty-textGrid/2
        elif pinOrientation == 'l':
            endx=endx+grid
            textx=startx+textGrid/2
            texty=starty-textGrid/2
        elif pinOrientation =='r':
            endx=endx-grid
            textx=startx-textGrid/2
            texty=starty-textGrid/2
        if self.GetValue('Visible'):
            canvas.create_line(startx,starty,endx,endy,fill=color)
        if not connected:
            size=max(1,grid/8)
            canvas.create_line(startx-size,starty-size,startx+size,starty+size,fill='red',width=2)
            canvas.create_line(startx+size,starty-size,startx-size,starty+size,fill='red',width=2)
        # comment this in for editing book
        #if self.pinNumberingMatters:
        #    self.pinNumberVisible=True
        if self.GetValue('NumberVisible'):
            canvas.create_text(textx,texty,text=str(self.GetValue('Number')),fill=color)