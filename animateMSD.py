from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsOpacityEffect, QLabel
from PyQt5.QtCore import QPropertyAnimation, QPoint, QEasingCurve, QSequentialAnimationGroup
from PyQt5.QtGui import QPixmap
from scipy.signal import argrelextrema
from numpy import greater, less, linspace
import sys
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class AnimationWidget(QWidget):
    def __init__(self, m, k, b, x0, v0, t, solverOutput):
        super().__init__()

        self.minimaTimeIndices = []
        self.maximaTimeIndices = []
        x0input = int(100 * x0)

        self.createWall()
        self.createZeroPoint()

        self.resize(600, 600)
        self.child = QWidget(self)
        self.child.setStyleSheet("background-color:red;border-radius:15px;")
        self.child.resize(100, 100)
        self.child.move(QPoint(x0input + 300, 300))

        self.animationGroup = QSequentialAnimationGroup()
        
        output = solverOutput
        self.minima = self.findMinima(output, t)
        self.maxima = self.findMaxima(output, t)
        startingDirectionResult = self.determineStartingDirection(output)

        # plot = plt.plot(t, output)
        # plt.show()

        self.createAnimations(self.minima, self.maxima, self.minimaTimeIndices, self.maximaTimeIndices, startingDirectionResult, t, x0input)
        
    def deleteMass(self):
        self.child.deleteLater()
    
    def startAnimation(self):
        self.animationGroup.start()

    def findMinima(self, solverOutput, t):
        #argrelextrema returns the indices of all local min/max (depending on what is specified, here I used "less" from numpy) in an array. 
        #The first list comprehension creates an array of the values specified by those indices, thus giving the values of the local minima.
        #The second list comprehension turns the array into a list
        #The findMaxima function works the exact same way, but with np.greater
        indices = argrelextrema(solverOutput, less)

        minimaArray = [solverOutput[i] for i in indices]
        minima = [100 * i for i in minimaArray[0]]

        timeIndicesArray = [i for i in indices]
        self.minimaTimeIndices = [i for i in timeIndicesArray[0]]

        return minima
    
    def findMaxima(self, solverOutput, t):
        indices = argrelextrema(solverOutput, greater)

        maximaArray = [solverOutput[i] for i in indices]
        maxima = [100 * i for i in maximaArray[0]]

        timeIndicesArray = [i for i in indices]
        self.maximaTimeIndices = [i for i in timeIndicesArray[0]]
        return maxima

    def determineStartingDirection(self, solverOutput):
        minimaIndices = argrelextrema(solverOutput, less)
        firstMinima = minimaIndices[0][0]
        maximaIndices = argrelextrema(solverOutput, greater)
        firstMaxima = maximaIndices[0][0]
        
        #This determines whether a maxima or minima appears first in the position output.
        # If a maxima appears first, it returns True; if a minima is first then it returns False
        if firstMaxima < firstMinima:
            return True
        elif firstMinima < firstMaxima:
            return False 
        
    def createAnimations(self, minima, maxima, minimaTimeIndices, maximaTimeIndices, direction, t, x0input):
        offset = 300 #horizontal offset to place block roughly in the middle of the screen
        if direction == True: #Means that the mass is moving in the +x direction, and the first peak will be a maxima
            for i in range(len(minima)):  #I used the length of minima here because in the True case it will either be 1 shorter or the same length as maxima
                a = 1
                b = 0
                timeRange1 = int((t[maximaTimeIndices[0]] - t[0]) * 1000) #Multiplied by 1000 to convert to milliseconds for .setDuration()
                timeRange2 = int(abs((t[minimaTimeIndices[0]] - t[maximaTimeIndices[0]])) * 1000)

        elif direction == False: #Means that the mass is moving in the -x direction, and the first peak will be a minima
            a = 0
            b = 1
            timeRange1 = int((t[minimaTimeIndices[0]] - t[0]) * 1000) #Multiplied by 1000 to convert to milliseconds for .setDuration()
            timeRange2 = int(abs((t[maximaTimeIndices[0]] - t[minimaTimeIndices[0]])) * 1000)

            for i in range(len(maxima)):
                animation1 = QPropertyAnimation(self.child, b"pos")
                animation1.setEasingCurve(QEasingCurve.InOutCubic) 

                animation2 = QPropertyAnimation(self.child, b"pos")
                animation2.setEasingCurve(QEasingCurve.InOutCubic)

                animationHold = [None, None]
                animationHold[a] = animation1
                animationHold[b] = animation2 

                if i != 0:
                    # animation1.setStartValue(QPoint(x0input + offset, 300))
                    #Divided by 1000 to convert to milliseconds for .setDuration
                    timeRange1 = int((abs(t[minimaTimeIndices[i]] - t[maximaTimeIndices[i-1]])) * 1000)
                    timeRange2 = int((abs(t[maximaTimeIndices[i]] - t[minimaTimeIndices[i]])) * 1000)  

                endValue1 = int(minima[i] + offset)
                animation1.setEndValue(QPoint(endValue1, 300))
                animation1.setDuration(timeRange1)

                endValue2 = int(maxima[i] + offset)
                animation2.setEndValue(QPoint(endValue2, 300))
                animation2.setDuration(timeRange2)

                self.animationGroup.addAnimation(animationHold[0])
                self.animationGroup.addAnimation(animationHold[1])
 
                # print("minima[{}]= ".format(i), minima[i])
                # print("maxima[{}]= ".format(i), maxima[i])

    def createWall(self):
        wall = QWidget(self)
        wall.setStyleSheet("background-color:black;")
        wall.resize(10, 600)
        wall.move(QPoint(90, 0))

        springAndDamperLabel = QLabel(self)
        SDImage = QPixmap('SpringAndDamper.png')
        springAndDamperLabel.setPixmap(SDImage)
        springAndDamperLabel.resize(SDImage.width(), SDImage.height())
        springAndDamperLabel.move(QPoint(100, 250)) 
    
    def createZeroPoint(self):
        zeroLabel = QLabel("x=0", self)
        zeroLabel.move(QPoint(285, 195))
        for i in range(20):
            wall = QWidget(self)
            wall.setStyleSheet("background-color:gray;")
            wall.resize(1, 20)
            effect = QGraphicsOpacityEffect(wall)
            effect.setOpacity(0.7)
            spacing = 10
            yPoint = 30 * i
            wall.move(QPoint(300, yPoint))
                
                

    def ODEsolver(self, m, k, b, x0, v0, t):
        
        def dSdx(x, S):
            x, v = S
            return [v,
                    (-b*v + k*(-x))/m]

        S0 = (x0, v0)
        #time analyzed, from [first input] seconds
        #to [second input] seconds, with [third input] number of points

        sol = odeint(dSdx, y0=S0, t=t, tfirst=True)
        sol_x = sol.T[0] #horizontal position
        sol_v = sol.T[1] #velocity
        sol_a = ((-b*sol_v + k*(-sol_x))/m) #acceleration

        return sol_x



if __name__ == '__main__':
    def ODEsolver(m, k, b, x0, v0, t):
        
        def dSdx(x, S):
            x, v = S
            return [v,
                    (-b*v + k*(-x))/m]

        S0 = (x0, v0)
        #time analyzed, from [first input] seconds
        #to [second input] seconds, with [third input] number of points

        sol = odeint(dSdx, y0=S0, t=t, tfirst=True)
        sol_x = sol.T[0] #horizontal position
        sol_v = sol.T[1] #velocity
        sol_a = ((-b*sol_v + k*(-sol_x))/m) #acceleration

        return sol_x
    
    m = .1
    k = 25
    b = 0.1
    x0 = 1
    v0 = 0
    t = linspace(0, 10, 1000)
    output = ODEsolver(m, k, b, x0, v0, t)
    app = QApplication(sys.argv)
    window = AnimationWidget(m, k, b, x0, v0, t, output)
    window.show()
    window.startAnimation()
    sys.exit(app.exec_())

    
