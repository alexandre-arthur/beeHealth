import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GlobalFiguresBees import *
from classRepresentation import *
from PIL import ImageTk, Image
import winsound

class ToolTip:
    def __init__(self,widget,text=None):

        def on_enter(event):
            self.tooltip=tk.Toplevel()
            self.tooltip.overrideredirect(True)
            width = 150
            print(str(self.widget.winfo_rooty()) + "    " + str(event.y_root))
            self.tooltip.geometry(f'+{event.x_root-900}+{self.widget.winfo_rooty()+10}')
            self.tooltip.background='white'

            self.label=tk.Label(self.tooltip,text=self.text, height=2, width=100)
            self.label.config(font=("Arial", 10))
            self.label.configure(wraplength=800, justify="left", background='white', borderwidth=1, relief="solid")
            self.label.pack(side='right')

        def on_leave(event):
            self.tooltip.destroy()

        self.widget=widget
        self.text=text

        self.widget.bind('<Enter>',on_enter)
        self.widget.bind('<Leave>',on_leave)

def newwindow():
    # Global varibles for the intern function
    global audio
    global sr
    global bgcolor
    # set the background color to light grey
    bgcolor = "#D3D3D3"

    # First example on startup
    FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
    PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
    #PATH_NAME = 'Representation\BeeDataset\OnlyBees\Ionian_mode_C.wav'

    # Create the window
    root = tk.Tk()
    root.configure(background=bgcolor)
    root.state('zoomed')



    # Create the title
    def titleshow(text):
        global bgcolor
        global titleframe
        titleframe = tk.Frame(root)
        titleframe.configure(background=bgcolor)
        title = tk.Label(titleframe, text=text, font=("Arial", 15), background=bgcolor, fg="black")
        title.pack()
        titleframe.grid(row=1, column=1)

    titleshow(FILE_NAME)



    # Open the os file browser and change the audio studied accordingly
    def browseFiles():
        global audio
        global sr
        global PATH_NAME
        PATH_NAME = tk.filedialog.askopenfilename(
            initialdir = "Representation\BeeDataset\\",
            title = "Select a File",
            filetypes = (("wav files", "*.wav"), ("None", ""))
        )

        # Check if "Cancel" wasn't clicked
        if PATH_NAME != "":
            audio, sr = getaudiofromfile(PATH_NAME)

            # Change the audio studied and goes back to FFT
            fft.changeto(audio, sr, fig, canva)
            PATH_NAME = filename
            filename = filename.split('/', 100)[-1] # Only get the file name and no the path
            titleframe.destroy()
            titleshow(filename)

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



    # Create the frame with the graphs
    mainframe = tk.Frame(root)
    mainframe.configure(background=bgcolor)

    # Configure the plt to go on the frame
    plotframe = tk.Frame(mainframe, bg=bgcolor)
    fig = plt.Figure()
    fig.set_facecolor(bgcolor)
    ax = fig.add_subplot(111)
    canva = FigureCanvasTkAgg(fig, plotframe)
    # Increase the width of the graph and the width of the frame
    canva.get_tk_widget().configure(width=root.winfo_screenwidth()-20*7, height=500, background=bgcolor)
    canva.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)


    #Get the current screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    #Print the screen size
    print("Screen width:", screen_width)
    print("Screen height:", screen_height)

    plotframe.pack(side=tk.BOTTOM, fill=tk.BOTH)

    # Call all the different modes
    wave = Waveclass()
    fft = FFTclass()
    chromafeature = ChromaFeatureclass()
    spectrogram = Spectrogramclass()
    mfcc = MFCCclass()
    mfccdelta = MFCCdeltaclass()
    spectralcentroid = spectralcentroidclass()
    zcr = ZCRClass()
    constantq = ConstantQclass()
    variableq = VariableQclass()
    energynormalized = EnergyNormalizedclass()
    bandwidth = Bandwidthclass()
    spectralcontrast = SpectralContrastclass()
    spectralflatness = SpectralFlatnessclass()
    spectralrolloff = SpectralRolloffclass()
    tonalCentroid = TonalCentroidclass()

    audio, sr = getaudiofromfile(PATH_NAME)
    wave.plotfct(audio, sr, ax)

    # Pack the frame with the graph
    mainframe.grid(row=2, column=1)
    mainframe.configure(background=bgcolor)



    # Create the frame with an image
    imageframe = tk.Frame(root)
    imageframe.configure(background=bgcolor)
    imagepath = "Representation\GlobalRepresentation\Cartoon-Bee.png"
    img = Image.open(imagepath)
    img = img.resize((140,110), Image.ANTIALIAS)
    new_img = ImageTk.PhotoImage(img)
    sound = lambda : winsound.PlaySound(PATH_NAME, winsound.SND_FILENAME)
    image = tk.Button(imageframe, image = new_img, background=bgcolor, width=140, height=50, borderwidth=0, relief="sunken", command=sound)
    image.pack()
    imageframe.grid(row=1, column=2)



    # Frame below with the buttons
    changemodeframe = tk.Frame(root, bg="white")

    # generic function to create buttons
    def create_button(mode, row, column):
        button = tk.Button(changemodeframe, text=mode.text, width=20, height=2, command=lambda: mode.changeto(audio, sr, fig, canva))
        button.grid(row=row, column=column)
        ToolTip(button, mode.description)

    # mode with which we can study an audio file
    #existingmode = [wave, fft, chromafeature, spectrogram, mfcc, mfccdelta, spectralcentroid, zcr, constantq, variableq, energynormalized, bandwidth, spectralflatness, spectralrolloff, tonalCentroid]
    existingmode = [wave, fft, bandwidth, zcr, spectralflatness, spectralrolloff, spectrogram, chromafeature, energynormalized, mfcc, mfccdelta, constantq, variableq, spectralcontrast, tonalCentroid]
    # Creating the buttons
    for index, mode in enumerate(existingmode):
        create_button(mode, row=index+1, column=1)

    # Put everything together
    changemodeframe.grid(row=2, column=2)



    root.title(FILE_NAME)
    root.title("Beehealth - Representation")
    # launch the app
    root.mainloop()

if __name__ == "__main__":
    newwindow()