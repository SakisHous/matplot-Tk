from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import Menu, ttk
import sqlite3 as lite
from tkDB import schemaDB

DEBUG = False


class Data:
    """
        In this class, we open a tk backend and open the database which contains the measured data
    """
    # For the purpose of plotting them we store in a list
    humidity = []
    temp = []
    timestamp = []
    filename = 'sensorDHT.db'

    def __init__(self, root):
        self.root = root

        self.fig = Figure(figsize=(12, 8), facecolor='cyan')
        self.axes = self.fig.add_subplot(111)


        self.axes.set_title("DHT22 sensor")
        self.axes.set_facecolor(color="cyan")
        #self.axes.set_frame_on(False)

        # the member function which open the database and read the data
        self.open_file()

        # flatten list of lists retrieving minimum value
        minY = min([y for y in Data.humidity])

        yUpperLimit = 50

        # flatten list of lists retrieving max value within defined limit
        maxY = max([y for y in Data.humidity if y < yUpperLimit])

        # dynamic limits
        self.axes.set_ylim(minY, maxY)
        self.axes.set_xlim(min(Data.timestamp), max(Data.timestamp))

        t0, = self.axes.plot(Data.timestamp, Data.humidity, color='purple')

        self.axes.set_ylabel('Humidity %')
        self.axes.set_xlabel('Time (sec)')

        self.axes.grid(linestyle='--')

        self.root.protocol('WM_DELETE_WINDOW', self.destroywindow)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def current_table(self):
        tables = schemaDB.SchemaDB.tables(Data.filename)
        print(tables)
        # TODO: A panel or an option menu button which gives information from database

    def destroywindow(self):
        self.root.quit()
        self.root.destroy()

    def open_file(self):
        # we read the humidity sensor measurements
        try:
            conn = lite.connect(self.filename)
            curs = conn.cursor()
            # SQL command to take all the measured data
            sql = "select * from sensorDHT;"
            curs.execute(sql)
            records = curs.fetchall()
            for rec in records:
                print(rec[0], rec[1], rec[2])
                Data.humidity.append(float(rec[0]))

        except lite.Error:
            print(lite.Error)

        if DEBUG:
            print(Data.humidity)
            print(len(Data.humidity))

        Data.timestamp = [5 * x for x in range(1, len(Data.humidity) + 1)]

        # Print the time values
        if DEBUG:
            print(Data.timestamp)


class GUI:

    def __init__(self, root):
        self.root = root
        root.title('Sensor')
        root.geometry('800x600+100+100')
        self.create_widgets()
        self.data = Data(self.root)

    def create_widgets(self):
        self.label1 = tk.Frame(root)
        self.label1.pack(side='top', fill='both', expand=1)

        # δημιουργώ την μπάρα του μενού
        menuBar = Menu(self.root)
        menuBar.configure(font='Consolas 10')
        self.root.config(menu=menuBar)

        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New")
        fileMenu.add_command(label="Save")
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit")
        menuBar.add_cascade(label="File", menu=fileMenu)

        self.f1 = tk.Frame(self.root)
        self.f1.pack(side='top', fill='y', expand=1)
        self.style_widgets()

        btn = ttk.Button(self.f1, text="Update",  style='raised.TButton')
        btn.pack(side='left', fill='y', expand=1)
        btn.bind('<1>', self.update_graph)

        opt = tk.StringVar()
        opt.set('Humidity')
        menu_btn = ttk.OptionMenu(self.f1, opt, 'Humidity', 'Humidity', 'Temperature', 'Accelerometer', 'Gyroscope',
                        style = 'raised.TMenubutton')
        menu_btn.pack(side='left', fill='y', expand=1)

    def update_graph(self, event):
        self.data.axes.clear()
        self.data.canvas.draw()
        self.data.axes.grid(linestyle='--')

    def style_widgets(self):
        """
            This method configures the style of the top widgets
        """
        s = ttk.Style(self.root)
        s.theme_use('clam')
        s.configure('.', borderwidth=1, font=('Consolas', 11))


root = tk.Tk()
gui = GUI(root)
root.mainloop()