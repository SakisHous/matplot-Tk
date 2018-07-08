# matplot-Tk
General purpose graphical user interface of matplotlib, numpy modules in Python

The first approach is the implemention of matplotlib and numpy in graphical user interface using Tkinter. The scope of this
project is an application which visualize and store data real time data from different kind sensors.

The v0.01 simply demonstrates the plotting of pre-aquired data stored with sqlite3.


sensorDHT.db:       This file has measured data from Arduino using DHT22 sensor. It's only for testing purpose of the main window.
                    The purpose is to read and plot the in real time, saving them in a archive

tkDB.py:            This contains two class. The GUI class and the DATA class. The first one implement the appearance of 
                    the GUI and the other plot the data.

schemaDB.py:        This contains a class with two staticmethods which return a list of tables and a list of fields each.

serial_Comm_GUI.py: It is a standalone serial monitor GUI, like Arduino's one. It is seperated from the above descripted scripts.
                    It will be added in the future in the main application.
