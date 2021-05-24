##  main.py
#   description: main function of program
#           contains the GUI and several
#           tabs for different features
#   author: David Kim
#   last modified: 2021-05-16

from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import dollar_cost_avg

class DCAWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title('Dollar Cost Average Visualizer')
        self.window.geometry("950x700")

        tabControl = ttk.Notebook(self.window)
        self.dca_tab = ttk.Frame(tabControl)
        self.ftw_tab = ttk.Frame(tabControl)
        self.kr_tab = ttk.Frame(tabControl)

        tabControl.add(self.dca_tab, text ='dollar cost averaging')
        tabControl.add(self.ftw_tab, text ='fifty two week average')
        tabControl.add(self.kr_tab, text ='key ratios')
        tabControl.pack(expand = 1, fill ="both")

        self.ticker = StringVar()
        self.ticker.set("VFV.TO")
        self.start_date = StringVar()
        self.start_date.set("2015-01-01")
        self.end_date = StringVar()
        self.end_date.set("2020-01-01")

        self.data_array = []
        self.colors = ['b','g','r','c','m','y','k','w']

        self.set_up_grid_layout_dca()
        self.set_up_inputs_dca()
        self.update_plot()


    # Setup layout in window
    # left frame: contains the plot
    # right frame: contains inputs and buttons
    def set_up_grid_layout_dca(self):
        self.left_frame = Frame(self.dca_tab, width=510, height= 680, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=5, pady=5)
        self.left_frame.grid_propagate(0)

        self.right_frame = Frame(self.dca_tab, width=400, height=680, bg='grey')
        self.right_frame.grid(row=0, column=1, padx=5, pady=5)
        self.right_frame.grid_propagate(0)

    def set_up_inputs_dca(self):
        label1 = Label(self.right_frame, text = "Enter a ticker symbol:")
        label1.grid(column = 0, row = 1)
        nameEntered = Entry(self.right_frame, width = 15, textvariable = self.ticker)
        nameEntered.grid(column = 0, row = 2,padx=5,pady=5)

        label2 = Label(self.right_frame, text = "Enter a start date (yyyy-mm-dd):")
        label2.grid(column = 0, row = 3)
        startDateEntered = Entry(self.right_frame, width = 15, textvariable = self.start_date)
        startDateEntered.grid(column = 0, row = 4,padx=5,pady=5)

        label3 = Label(self.right_frame, text = "Enter a end date (yyyy-mm-dd):")
        label3.grid(column = 1, row = 3)
        endDateEntered = Entry(self.right_frame, width = 15, textvariable = self.end_date)
        endDateEntered.grid(column = 1, row = 4,padx=5,pady=5)

        # button that displays the plot
        plot_button = Button(master = self.right_frame, command = self.update_plot,height = 2, width = 10,text = "Plot")
        plot_button.grid(column=0,row=5,padx=5,pady=5, sticky='nswe')

        clear_button = Button(master = self.right_frame, command = self.clear_enteries,height = 2, width = 10,text = "Clear Enteries")
        clear_button.grid(column=0,row=6,padx=5,pady=5, sticky='nswe')

    # plotting the graph in frame
    def update_plot(self):

        analyz_flag = 0                      #Check if the ticker has already been analyzed
        for p in self.data_array:
            if self.ticker.get() == p[2]:
                analyz_flag = 1

        if not analyz_flag:                  #If ticker has not been anaylzed then analyze it
            package = dollar_cost_avg.getInfoMonthly(self.ticker.get(),self.start_date.get(),self.end_date.get())
            if package is not None:
                self.data_array.append(package)
        
        # the figure that will contain the plot
        fig1 = Figure(figsize = (5, 5),dpi = 100)
        plt1 = fig1.add_subplot(111)
    
        line = FigureCanvasTkAgg(fig1, self.left_frame)
        line.get_tk_widget().grid(row=1,column=0,padx=5,pady=5, sticky='nswe')

        color_counter = 0
        for d in self.data_array:
            amounts = d[0]
            dates = d[1]
            name = d[2]
            plt1.plot(dates,amounts,color=self.colors[color_counter],marker='o',label=name)
            plt1.set_xticks([dates[0],dates[int((len(dates)-1)/3)],dates[int(2*(len(dates)-1)/3)],dates[len(dates)-1]])
            color_counter += 1

        plt1.legend()
        plt1.set_title('Date vs Total Amount')

        toolbar = NavigationToolbar2Tk(line, self.left_frame)
        toolbar.grid(row=2,column=0,padx=5,pady=5,sticky='nswe')

    def clear_enteries(self):
        self.data_array = []


if __name__ == "__main__":
    dca_window = DCAWindow()
    dca_window.window.mainloop()