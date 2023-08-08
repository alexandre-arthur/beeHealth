import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GlobalFiguresBees import *
from GlobalClassRepresentation import *
from classRepresentation import *
from PIL import ImageTk, Image
import winsound

class ToolTip:
    # Create a tooltip when the mouse hover on a button
    def __init__(self,widget,text=None):
    # Create a tooltip when the mouse hover on a button

        def on_enter(event):
            # Function when the mouse enter the button

            # Create the tooltip
            self.tooltip=tk.Toplevel()
            self.tooltip.overrideredirect(True)

            # Place the tooltip
            self.tooltip.geometry(f'+{event.x_root-900}+{self.widget.winfo_rooty()+10}')
            self.tooltip.background='white'

            # Create the text in the tooltip
            self.label=tk.Label(self.tooltip,text=self.text, height=2, width=100)
            self.label.config(font=("Arial", 10))
            self.label.configure(wraplength=800, justify="left", background='white', borderwidth=1, relief="solid")
            self.label.pack(side='right')

        def on_leave(event):
            # Function when the mouse leave the button
            self.tooltip.destroy()

        # Global variables
        self.widget=widget
        self.text=text

        # Bind the function to the button
        self.widget.bind('<Enter>',on_enter)
        self.widget.bind('<Leave>',on_leave)


def newwindow():
    # Global varibles for the intern function
    #global audio
    #global sr
    #global bgcolor
    # set the background color to light grey
    bgcolor = "#D3D3D3"

    # First example on startup
    FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
    PATH_NAME = 'Audio\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
    #PATH_NAME = 'Representation\BeeDataset\OnlyBees\Ionian_mode_C.wav'

    # Create the window
    root = tk.Tk()
    root.configure(background=bgcolor)
    root.state('zoomed')

    # Create the title

    titleFrame = changeTitleFrame(root, FILE_NAME, bgcolor)
    titleFrame.grid(row=1, column=1)

    # Open the os file browser and change the audio studied accordingly
    def browseFiles():
        global audio
        global sr
        global PATH_NAME
        newSoundFile = tk.filedialog.askopenfilename(
            initialdir = "Audio\BeeDataset\\",
            title = "Select a File",
            filetypes = (("wav files", "*.wav"), ("None", ""))
        )

        # Check if "Cancel" wasn't clicked
        if newSoundFile != "":
            audio, sr = getaudiofromfile(newSoundFile)
            PATH_NAME = newSoundFile

            # Change the audio studied and goes back to FFT
            fft = FFTclass()
            fft.changeto(audio, sr, fig, canva)

            # Change the title
            filename = newSoundFile
            filename = filename.split('/', 100)[-1] # Only get the file name and no the path
            titleFrame.destroy()
            changeTitleFrame(root, filename, bgcolor)
            titleFrame.grid(row=1, column=1)

    # Add a menu bar up right
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)

    # menu to open a new file
    filemenu.add_command(label="Open audio file...", command=browseFiles, accelerator="Ctrl+O")
    root.bind_all("<Control-o>", lambda event: browseFiles())

    # menu to open a window with every mode shown
    filemenu.add_command(label="Detailed window", command=showAllRepresentation)

    # menu to open a new intialized window
    filemenu.add_command(label="New window", command=newwindow, accelerator="Ctrl+N")
    root.bind_all("<Control-n>", lambda event: newwindow())

    # menu to quit the app
    filemenu.add_command(label="Quit", command=root.destroy, accelerator="Ctrl+W")
    root.bind_all("<Control-w>", lambda event: root.destroy())
    
    # Add the file sub category with all the button above
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    mainFrame, fig, canva = createGraphFrame(root, PATH_NAME, bgColor=bgcolor)
    
    mainFrame.grid(row=2, column=1)

    def addImageButton(root, imagePath : str, buttonFunction, bgColor : str = "#FFFFFF", width : int = 200, height : int = 200, borderWidth : int = 0):
        imageFrame = tk.Frame(root)
        imageFrame.configure(background=bgColor)
        img = Image.open(imagePath)
        img = img.resize((140, 110), Image.ANTIALIAS)
        new_img = ImageTk.PhotoImage(img)
        image = tk.Button(imageFrame, image=new_img, background=bgColor, width=width, height=height, borderwidth=borderWidth, relief="sunken", command=buttonFunction)
        image.image = new_img  # Store a reference to avoid garbage collection
        image.pack()

        return imageFrame

    # Create the frame with an image
    imagePath = r"Representation\\GlobalRepresentation\\Images\\Cartoon-Bee.png"
    buttonFunction = lambda : winsound.PlaySound(PATH_NAME, winsound.SND_FILENAME)
    imageFrame = addImageButton(root, imagePath, buttonFunction, bgColor=bgcolor, borderWidth=0, width = 140, height = 50)

    imageFrame.grid(row=1, column=2)


    # Frame below with the buttons
    changemodeframe = tk.Frame(root, bg="white")

    global audio
    audio, sr = rosa.load(PATH_NAME)

    # generic function to create buttons
    def create_button(mode, row, column):
        global audio
        button = tk.Button(changemodeframe, text=mode.getTitle(), width=20, height=2, command=lambda: mode.changeto(audio, sr, fig, canva))
        button.grid(row=row, column=column)
        ToolTip(button, mode.description)

    # Creating the buttons
    existingmode = GlobalClassRepresentation().getAllModes()
    for index, mode in enumerate(existingmode):
        create_button(mode, row=index+1, column=1)

    # Put everything together
    changemodeframe.grid(row=2, column=2)

    root.title(FILE_NAME)
    root.title("Beehealth - Representation")
    # launch the app
    root.mainloop()




def changeTitleFrame(root, text : str, bgColor : str = "#FFFFFF", fgColor : str = "#000000", font : (str, int) = ("Arial", 15)):
    # Create a new frame to display the title
    # @arguments : - root : the root of the window
    #              - text : The title to display
    #              - bgColor : The background color of the frame (default : black)
    #              - fgColor : The foreground color of the frame (default : white)
    # @return : - titleFrame : The frame with the title on it

    # Create a new frame
    titleFrame = tk.Frame(root)
    titleFrame.configure(background=bgColor)

    # Add the title on it
    title = tk.Label(titleFrame, text=text, font=font, background=bgColor, fg=fgColor)
    title.pack()
    
    return titleFrame

def createGraphFrame(root, filePath, bgColor : str = "#FFFFFF"):
    # Create the frame with the graphs
    mainFrame = tk.Frame(root)
    mainFrame.configure(background=bgColor)

    # Inside frame to get the plot
    plotframe = tk.Frame(mainFrame, bg=bgColor)

    # Configure the plt to go on the frame
    fig, canva = addPlotToFrame(plotframe, filePath, bgColor, width=root.winfo_screenwidth()-20*7)

    plotframe.pack(side=tk.BOTTOM, fill=tk.BOTH)

    # Pack the frame with the graph
    mainFrame.configure(background=bgColor)

    return mainFrame, fig, canva

def addPlotToFrame(frame, pathName : str, bgColor : str = "#FFFFFF", width : int = 1000, height : int = 500):
    # Configure the plt to go on the frame
    fig = plt.Figure()
    fig.set_facecolor(bgColor)
    ax = fig.add_subplot(111)
    canva = FigureCanvasTkAgg(fig, frame)

    # Increase the width of the graph
    canva.get_tk_widget().configure(width=width, height=height, background=bgColor)
    canva.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    # Put the default graph
    audio, sampleRate = getaudiofromfile(pathName)
    wave = Waveclass()
    wave.plotfct(audio, sampleRate, ax)

    return fig, canva



if __name__ == "__main__":
    newwindow()