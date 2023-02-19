# MSDApplication
Application for the analysis and visualization of a mass-spring-damper (MSD) system.

This application produces a user interface that allows the user to easily manipulate key variables and initial conditions of a simulated mass-spring-damper system. When run, the program uses the selected variable values to solve the system of differential equations that describe the MSD system. It then presents vital system attributes such as settling time and  natural frequency, as well as graphs that visualize the system's behavior.

This application is built entirely in Python using the PyQt and pyqtgraph libraries for the GUI, and the numpy and scipy libraries for ODE analysis as well as miscellaneous math. It it entirely contained within 'main.py' and can be run from there.
