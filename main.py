from PyQt5.QtWidgets import (QApplication, QLabel, QGridLayout, QGroupBox, 
                             QWidget, QSlider, QLineEdit, QPushButton, 
                            QHBoxLayout, QTabWidget, QComboBox, QTextEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from numpy import linspace, pi, inf, sqrt
import sys
from scipy.integrate import odeint, solve_ivp
from animateMSD import AnimationWidget

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()

        #Building the main tab
        self.GraphGroupBox()
        x = []
        y = []
        self.positionLine1 = self.positionGraph.plot(x, y)
        self.velocityLine1 = self.velocityGraph.plot(x, y)
        self.accelerationLine1 = self.accelerationGraph.plot(x, y)
        self.energyLine1 = self.energyGraph.plot(x, y, pen='g', name='Kinetic Energy')
        self.energyLine2 = self.energyGraph.plot(x, y, pen='r', name='Potential Energy')
        self.energyLine3 = self.energyGraph.plot(x, y, pen='b', name='Total Energy')

        self.systemAttributesGroupBox()
        self.systemVariablesGroupBox()
        self.initialConditionsGroupBox()

        tabwidget = QTabWidget()
        MainLayout = QGridLayout()

        w1 = QWidget()
        t1 = QGridLayout()
        t1.addWidget(self.GraphGroupBox, 0, 0, 1, 2)
        t1.addWidget(self.systemVariablesGroupBox, 2, 0)
        t1.addWidget(self.systemAttributesGroupBox, 1, 0, 1, 2)
        t1.addWidget(self.initialConditionsGroupBox, 2, 1)
        w1.setLayout(t1)
        tabwidget.addTab(w1,"Main")
        #END MAIN TAB
        

        #Building the ODE tab
        self.createODEintGroupBox()
        self.createSolveIVPGroupBox()
        self.ODEintGroupBox.setEnabled(True)
        self.solveIVPGroupBox.setDisabled(True)
        solverLabel = QLabel("Solver")
        self.solverComboBox = QComboBox()
        self.solverComboBox.insertItem(0, "odeint")
        self.solverComboBox.insertItem(1, "solve_ivp")
        self.solverComboBox.currentIndexChanged.connect(self.enableODEWidgets)
        defaultSettingsButton = QPushButton()
        defaultSettingsButton.setText("Default Settings")
        defaultSettingsButton.pressed.connect(self.defaultSettingsButtonPressed)
        w2 = QWidget()
        t2 = QGridLayout()
        topLayout = QHBoxLayout()
        t2.addLayout(topLayout, 0, 0)
        topLayout.addWidget(solverLabel)
        topLayout.addWidget(self.solverComboBox)
        topLayout.addWidget(defaultSettingsButton)
        topLayout.addStretch(1)
        t2.addWidget(self.ODEintGroupBox, 1, 0)
        t2.addWidget(self.solveIVPGroupBox, 1, 1)
        t2.setColumnStretch(0, 1)
        t2.setColumnStretch(1, 1)
        bottomlayout = QHBoxLayout()
        bottomLabel = QTextEdit()
        bottomLabel.setPlainText("Note: Setting Step Size options to ""0"" will leave the values to be determined automatically by the solver.")
        bottomLabel.setReadOnly(True)
        bottomlayout.addWidget(bottomLabel)
        t2.addLayout(bottomlayout, 2, 0, 1, 2)
        t2.setRowStretch(0,1)
        t2.setRowStretch(1,3)
        t2.setRowStretch(2,1)
        t2.setRowStretch(3,10)
        w2.setLayout(t2)
        tabwidget.addTab(w2, "ODE Options")
        #END ODE TAB


        #Building the animation tab
        w3 = QWidget()
        self.animation = None
    
        startAnimationButton = QPushButton("Start")
        startAnimationButton.pressed.connect(self.startAnimation)
        startAnimationButton.pressed.connect(self.startTimer)

        self.t3 = QGridLayout()
        self.t3.addWidget(startAnimationButton, 1, 1, 1, 1)

        self.timerLabel = QLabel("0.00")
        self.timerLabel.setFont(QFont("LCD", 36))
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.t3.addWidget(self.timerLabel, 0, 1)

        self.t3.setRowStretch(0, 5)
        self.t3.setRowStretch(1, 1)
        self.t3.setColumnStretch(0, 2)
        self.t3.setColumnStretch(1, 1)

        w3.setLayout(self.t3)
        tabwidget.addTab(w3, "Animation")
        #END ANIMATION TAB


        MainLayout.addWidget(tabwidget)
        self.setLayout(MainLayout)

        ########## END INIT FUNCTION ##########

    
    def createAnimationWidget(self):
        m = float(self.massInput.text())
        k = float(self.springInput.text())
        b = float(self.damperInput.text())
        x0 = float(self.xPosInput.text())
        v0 = float(self.velocityInput.text())
        t = linspace(0, float(self.ODEINTevalTimeInput.text()), 1000)
        solverOutput = self.horizontalPositions
        
        if self.animation != None:
            self.animation.deleteMass()

        self.animation = AnimationWidget(m, k, b, x0, v0, t, solverOutput) 
        self.t3.addWidget(self.animation, 0, 0, 1, 2)
        
    def startAnimation(self):
        self.animation.startAnimation()

    def GraphGroupBox(self):
        self.GraphGroupBox = QGroupBox(title="Graphs")

        self.positionGraph = pg.plot()
        self.positionGraph.showGrid(x=True, y=True)
        self.positionGraph.setLabel('left', 'Horizontal Position', units='x')
        self.positionGraph.setLabel('bottom', 'Time', units='s')

        self.velocityGraph = pg.plot()
        self.velocityGraph.showGrid(x=True, y=True)
        self.velocityGraph.setLabel('left', 'Velocity', units='m/s')
        self.velocityGraph.setLabel('bottom', 'Time', units='s')

        self.accelerationGraph = pg.plot()
        self.accelerationGraph.showGrid(x=True, y=True)
        self.accelerationGraph.setLabel('left', 'Acceleration', units='m/s^2')
        self.accelerationGraph.setLabel('bottom', 'Time', units='s')

        self.energyGraph = pg.plot()
        self.energyGraph.showGrid(x=True, y=True)
        self.energyGraph.setLabel('left', 'Energy', units='J')
        self.energyGraph.setLabel('bottom', 'Time', units='s')
        self.energyGraph.addLegend(offset=(-1, 1))

        layout = QGridLayout()
        layout.addWidget(self.positionGraph, 0, 0)
        layout.addWidget(self.velocityGraph, 0, 1)
        layout.addWidget(self.accelerationGraph, 1, 0)
        layout.addWidget(self.energyGraph, 1, 1)
        self.GraphGroupBox.setLayout(layout)


    def systemAttributesGroupBox(self):
        self.systemAttributesGroupBox = QGroupBox(title="System Attributes")

        natFrequencyLabel = QLabel("Natural Frequency:")
        self.natFrequencyOutput = QLabel("")
        self.natFrequencyOutput.setStyleSheet("font-weight: bold")
        dampedNatFrequencyLabel = QLabel("Damped Natural Frequency:")
        self.dampedNatFrequencyOutput = QLabel("")
        self.dampedNatFrequencyOutput.setStyleSheet("font-weight: bold")
        settlingTimeLabel = QLabel("Settling Time (s):")
        self.settlingTimeOutput = QLabel("")
        self.settlingTimeOutput.setStyleSheet("font-weight: bold")

        startStopButton = QPushButton()
        buttonConnections = [self.ODEsolver, self.xSliderValue, self.velocitySliderValue, self.massSliderValue, self.springSliderValue, self.damperSliderValue, self.createAnimationWidget]
        startStopButton.setText("Run")
        for connection in buttonConnections:
            startStopButton.clicked.connect(connection)

        layout = QHBoxLayout()
        layout.addWidget(natFrequencyLabel)
        layout.addWidget(self.natFrequencyOutput)
        layout.addStretch(1)
        layout.addWidget(dampedNatFrequencyLabel)
        layout.addWidget(self.dampedNatFrequencyOutput)
        layout.addStretch(1)
        layout.addWidget(settlingTimeLabel)
        layout.addWidget(self.settlingTimeOutput)
        layout.addStretch(1)
        layout.addWidget(startStopButton)

        self.systemAttributesGroupBox.setLayout(layout)


    def systemVariablesGroupBox(self):
        self.systemVariablesGroupBox = QGroupBox(title="System Variables")

        self.massSlider = QSlider(Qt.Orientation.Horizontal)
        self.massLabel = QLabel("Mass of Weight (kg):")
        self.massLabel.setBuddy(self.massSlider)
        self.massInput = QLineEdit()
        self.massInput.setText("1.25")
        self.massSlider.setMinimum(10)
        self.massSlider.setMaximum(1000)
        self.massSlider.setValue(int(100 * float(self.massInput.text())))
        self.massSlider.valueChanged.connect(self.massInputValue)

        self.springSlider = QSlider(Qt.Orientation.Horizontal)
        self.springLabel = QLabel("Spring Constant, k (N/m):")
        self.springLabel.setBuddy(self.springSlider)
        self.springInput = QLineEdit()
        self.springInput.setText("25")
        self.springSlider.setMinimum(10)
        self.springSlider.setMaximum(10000)
        self.springSlider.setValue(int(100 * float(self.springInput.text())))
        self.springSlider.valueChanged.connect(self.springInputValue)

        self.damperSlider = QSlider(Qt.Orientation.Horizontal)
        self.damperLabel = QLabel("Damping Ratio, b:")
        self.damperLabel.setBuddy(self.damperSlider)
        self.damperInput = QLineEdit()
        self.damperInput.setText(".1")
        self.damperSlider.setMinimum(0)
        self.damperSlider.setMaximum(100)
        self.damperSlider.setValue(int(100 * float(self.damperInput.text())))
        self.damperSlider.valueChanged.connect(self.damperInputValue)

        layout = QGridLayout()
        layout.addWidget(self.massLabel, 4, 0)
        layout.addWidget(self.massSlider, 4, 1)
        layout.addWidget(self.massInput, 4, 2)
        layout.addWidget(self.damperLabel, 5, 0)
        layout.addWidget(self.damperSlider, 5, 1)
        layout.addWidget(self.damperInput, 5, 2)
        layout.addWidget(self.springLabel, 6, 0)
        layout.addWidget(self.springSlider, 6, 1)
        layout.addWidget(self.springInput, 6, 2)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 1)

        self.systemVariablesGroupBox.setLayout(layout)


    def initialConditionsGroupBox(self):
        self.initialConditionsGroupBox = QGroupBox(title="Initial Conditions")

        self.xPosSlider = QSlider(Qt.Orientation.Horizontal)
        self.xPosSlider.setMinimum(10)
        self.xPosSlider.setMaximum(200)
        self.xPosSlider.setSingleStep(10)

        xPosLabel = QLabel("Initial x Position (m):")
        xPosLabel.setBuddy(self.xPosSlider)
        self.xPosInput = QLineEdit()
        self.xPosInput.setText("1.0")

        self.xPosSlider.setValue(int(100 * float(self.xPosInput.text())))
        self.xPosSlider.valueChanged.connect(self.xInputValue)

        self.velocitySlider = QSlider(Qt.Orientation.Horizontal)
        self.velocityLabel = QLabel("Starting Velocity (m/s):")
        self.velocityLabel.setBuddy(self.velocitySlider)
        self.velocityInput = QLineEdit()
        self.velocityInput.setText("0")

        self.velocitySlider.setMinimum(0)
        self.velocitySlider.setMaximum(1000)
        self.velocitySlider.setSingleStep(10)
        
        self.velocitySlider.setValue(int(100 * float(self.velocityInput.text())))
        self.velocitySlider.valueChanged.connect(self.velocityInputValue)

        layout = QGridLayout()
        layout.addWidget(xPosLabel, 0, 0)
        layout.addWidget(self.xPosSlider, 0, 1)
        layout.addWidget(self.xPosInput, 0, 2)
        layout.addWidget(self.velocityLabel, 1, 0)
        layout.addWidget(self.velocitySlider, 1, 1)
        layout.addWidget(self.velocityInput, 1, 2)
        layout.setColumnStretch(0,2)
        layout.setColumnStretch(1,5)
        layout.setColumnStretch(2,1)

        self.initialConditionsGroupBox.setLayout(layout)

    def xSliderValue(self):
        self.xPosSlider.setValue(int(100 * float(self.xPosInput.text())))

    def xInputValue(self):
        self.xPosInput.setText(str(self.xPosSlider.value() / 100))

    def velocityInputValue(self):
        self.velocityInput.setText(str(self.velocitySlider.value() / 100))
    
    def velocitySliderValue(self):
        self.velocitySlider.setValue(int(100 * float(self.velocityInput.text())))

    def massInputValue(self):
        self.massInput.setText(str(self.massSlider.value() / 100))

    def springInputValue(self):
        self.springInput.setText(str(self.springSlider.value() / 100))

    def damperInputValue(self):
        self.damperInput.setText(str(self.damperSlider.value() / 100))

    def massSliderValue(self):
        self.massSlider.setValue(int(100 * float(self.massInput.text())))
    
    def springSliderValue(self):
        self.springSlider.setValue(int(100 * float(self.springInput.text())))
    
    def damperSliderValue(self):
        self.damperSlider.setValue(int(100 * float(self.damperInput.text())))

    
    
    def createODEintGroupBox(self):
        self.ODEintGroupBox = QGroupBox("odeint")
        layout = QGridLayout()

        firstStepSizeLabel = QLabel("First Step Size:")
        minStepSizeLabel = QLabel("Minimum Step Size:")
        maxStepSizeLabel = QLabel("Maximum Step Size:")
        evalTimeLabel = QLabel("Evaluation Time:")

        self.ODEINTfirstStepSizeInput = QLineEdit()
        self.ODEINTfirstStepSizeInput.setText("0")
        self.ODEINTminStepSizeInput = QLineEdit()
        self.ODEINTminStepSizeInput.setText("0")
        self.ODEINTmaxStepSizeInput = QLineEdit()
        self.ODEINTmaxStepSizeInput.setText("0")
        self.ODEINTevalTimeInput = QLineEdit()
        self.ODEINTevalTimeInput.setText("10")

        widgets = [firstStepSizeLabel, self.ODEINTfirstStepSizeInput, 
                   minStepSizeLabel, self.ODEINTminStepSizeInput,
                   maxStepSizeLabel, self.ODEINTmaxStepSizeInput,
                   evalTimeLabel, self.ODEINTevalTimeInput]
        
        i = 0
        j = 0
        for widget in widgets:
            if j == 2:
                j = 0
                i+=1
            layout.addWidget(widget, i, j)
            # widget.setEnabled(False)
            j+=1
        
        self.ODEintGroupBox.setLayout(layout)
            
    
    def createSolveIVPGroupBox(self):
        self.solveIVPGroupBox = QGroupBox("solve_ivp")
        layout = QGridLayout()

        solverLabel = QLabel("ODE Solver Method:")
        firstStepSizeLabel = QLabel("First Step Size:")
        maxStepSizeLabel = QLabel("Maximum Step Size:")
        evalTimeLabel = QLabel("Evaluation Time:")

        self.IVPSolverInput = QComboBox()
        self.IVPSolverInput.insertItem(0, "RK45")
        self.IVPSolverInput.insertItem(1, "RK23")
        self.IVPSolverInput.insertItem(2, "DOP853")
        self.IVPSolverInput.insertItem(3, "Radau")
        self.IVPSolverInput.insertItem(4, "BDF")

        self.solveIVPfirstStepSizeInput = QLineEdit()
        self.solveIVPfirstStepSizeInput.setText("0")
        self.solveIVPmaxStepSizeInput = QLineEdit()
        self.solveIVPmaxStepSizeInput.setText("0")
        self.solveIVPevalTimeInput = QLineEdit()
        self.solveIVPevalTimeInput.setText("10")

        widgets = [solverLabel, self.IVPSolverInput,
                   firstStepSizeLabel, self.solveIVPfirstStepSizeInput, 
                   maxStepSizeLabel, self.solveIVPmaxStepSizeInput,
                   evalTimeLabel, self.solveIVPevalTimeInput]
        
        i = 0
        j = 0
        for widget in widgets:
            if j ==2:
                j = 0
                i+=1
            layout.addWidget(widget, i, j)
            # widget.setEnabled(False)
            j+=1
        
        self.solveIVPGroupBox.setLayout(layout)
    
    def disableODEWidgets(self, currentIndex):
        boxes = {"odeint": self.ODEintGroupBox,
                "solve_ivp": self.solveIVPGroupBox}
        if currentIndex == "odeint":
            group = boxes["solve_ivp"]
        elif currentIndex=="solve_ivp":
            group = boxes["odeint"]
        
        group.setDisabled(True)
        # for widget in group.findChildren((QLineEdit, QComboBox)):
        #     widget.setEnabled(False)
            
    def enableODEWidgets(self):
        currentIndex = self.solverComboBox.currentText()
        boxes = {"odeint": self.ODEintGroupBox,
                "solve_ivp": self.solveIVPGroupBox}
        group = boxes[currentIndex]
        group.setEnabled(True)
        # for widget in group.findChildren((QLineEdit, QComboBox)):
        #     widget.setEnabled(True)
        self.disableODEWidgets(currentIndex)
        
    def defaultSettingsButtonPressed(self):

        #Reset the odeint options:
        self.ODEINTfirstStepSizeInput.setText("0")
        self.ODEINTminStepSizeInput.setText("0")
        self.ODEINTmaxStepSizeInput.setText("0")
        self.ODEINTevalTimeInput.setText("10")

        #Reset the solve_ivp options:
        self.IVPSolverInput.setCurrentText("RK45")
        self.solveIVPfirstStepSizeInput.setText("0")
        self.solveIVPmaxStepSizeInput.setText("0")
        self.solveIVPevalTimeInput.setText("10")

        self.solverComboBox.setCurrentText("odeint")
        self.enableODEWidgets()

    def updateTimer(self):
        currentTime = float(self.timerLabel.text())
        maxTime = float(self.ODEINTevalTimeInput.text())
        if currentTime != maxTime:
            nextTime = str("{:.2f}".format(currentTime + 0.01))
            self.timerLabel.setText(nextTime)
        else:
            self.timer.stop()

        self.ODEINTevalTimeInput.text()

    def startTimer(self):
        self.timer.start(10)
        self.timerLabel.setText("0.00")

    def ODEsolver(self):
        m = float(self.massInput.text())
        k = float(self.springInput.text())
        b = float(self.damperInput.text())
        x0 = float(self.xPosInput.text())
        v0 = float(self.velocityInput.text())

        def dSdx(x, S):
            x, v = S
            return [v,
                    (-b*v + k*(-x))/m]

        S0 = (x0, v0)
         #time analyzed, from [first input] seconds
        #to [second input] seconds, with [third input] number of points

        solverSelected = self.solverComboBox.currentText()
        if solverSelected == "odeint":

            firstStepSize = float(self.ODEINTfirstStepSizeInput.text())
            minStepSize = float(self.ODEINTminStepSizeInput.text())
            maxStepSize = float(self.ODEINTmaxStepSizeInput.text())
            evalTime = float(self.ODEINTevalTimeInput.text())
            if int(evalTime) == 0:
                evalTime = 10
                self.ODEINTevalTimeInput.setText("10")
            t = linspace(0, evalTime, 1000)

            sol = odeint(dSdx, y0=S0, t=t, tfirst=True, h0=firstStepSize, hmin=minStepSize, hmax=maxStepSize)
            sol_x = sol.T[0] #horizontal position
            sol_v = sol.T[1] #velocity
            sol_a = ((-b*sol_v + k*(-sol_x))/m) #acceleration

        elif solverSelected == "solve_ivp":
            methodSelected = self.IVPSolverInput.currentText()

            firstStepSize = float(self.solveIVPfirstStepSizeInput.text())
            if int(firstStepSize) == 0:
                firstStepSize = None

            maxStepSize = float(self.solveIVPmaxStepSizeInput.text())
            if int(maxStepSize) == 0:
                maxStepSize = inf

            evalTime = float(self.solveIVPevalTimeInput.text())
            if int(evalTime) == 0:
                evalTime = 10
                self.solveIVPevalTimeInput.setText("10")

            t = (0, evalTime)
            sol = solve_ivp(dSdx, y0=S0, t_span=t, method=methodSelected, first_step=firstStepSize, max_step=maxStepSize)
            sol_x = sol.y[0] #horizontal position
            sol_v = sol.y[1] #velocity
            sol_a = ((-b*sol_v + k*(-sol_x))/m) #acceleration 
            t = sol.t

        #Energy calcs:
        kineticEnergy = .5 * m * sol_v**2
        potentialEnergy = .5 * k * sol_x**2
        totalEnergy = kineticEnergy + potentialEnergy

        #Frequency and settling time calcs
        floatNaturalFrequency = (1 / (2 * pi)) * sqrt(k / m)
        floatDampedNaturalFrequency = floatNaturalFrequency * sqrt(1 - b**2)
        tau = 1/(b * floatNaturalFrequency)
        floatSettlingTime = 4 * tau

        self.positionLine1.setData(t, sol_x)
        self.velocityLine1.setData(t, sol_v)
        self.accelerationLine1.setData(t, sol_a)
        self.energyLine1.setData(t, kineticEnergy, pen='g', name='Kinetic Energy')
        self.energyLine2.setData(t, potentialEnergy, pen='r', name='Potential Energy')
        self.energyLine3.setData(t, totalEnergy, pen='b', name='Total Energy')

        naturalFrequency = "{:.5f}".format(floatNaturalFrequency)
        dampedNaturalFrequency = "{:.5f}".format(floatDampedNaturalFrequency)
        settlingTime = "{:.5f}".format(floatSettlingTime)
        self.natFrequencyOutput.setText(str(naturalFrequency))
        self.dampedNatFrequencyOutput.setText(str(dampedNaturalFrequency))
        self.settlingTimeOutput.setText(str(settlingTime))

        self.horizontalPositions = sol.T[0]
        return sol
    
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
