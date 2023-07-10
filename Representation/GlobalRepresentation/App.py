import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GlobalFiguresBees import * 
from classRepresentation import * 


def newwindow():
    # Global varibles for the intern function
    global audio
    global sr

    # Create the window
    root = tk.Tk()

    # Create the frame with the graphs
    mainframe = tk.Frame(root)

    # Open the os file browser and change the audio studied accordingly
    def browseFiles():
        filename = tk.filedialog.askopenfilename(
            initialdir = "Representation\BeeDataset\\",
            title = "Select a File",
            filetypes = (("wav files", "*.wav"), ("None", ""))
        )

        # Check if "Cancel" wasn't clicked
        if filename != "":
            audio, sr = getaudiofromfile(filename)

            # Change the audio studied and goes back to FFT
            fft.changeto(audio, sr, fig, canva)
            filename = filename.split('/', 100)[-1] # Only get the file name and no the path
            root.title(filename)

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

    # Configure the plt to go on the frame
    fig = plt.Figure()
    ax = fig.add_subplot(111)
    canva = FigureCanvasTkAgg(fig, mainframe)
    canva.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    # Call all the different modes
    wave = Waveclass()
    fft = FFTclass()
    chromafeature = ChromaFeatureclass()
    spectrogram = Spectrogramclass()
    mfcc = MFCCclass()
    mfccdelta = MFCCdeltaclass()
    spectralcentroid = spectralcentroidclass()
    zcr = ZCRClass()

    # First example on startup
    FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
    PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
    PATH_NAME = 'Representation\BeeDataset\OnlyBees\Ionian_mode_C.wav'
    audio, sr = getaudiofromfile(PATH_NAME)
    wave.plotfct(audio, sr, ax)

    # Pack the frame with the graph
    mainframe.pack()

    # Frame below with the buttons
    changemodeframe = tk.Frame(root, bg="white")

    # generic function to create buttons
    def create_button(mode, row, column):
        button = tk.Button(changemodeframe, text=mode.text, command=lambda: mode.changeto(audio, sr, fig, canva))
        button.grid(row=row, column=column)

    # mode with which we can study an audio file
    existingmode = [wave, fft, chromafeature, spectrogram, mfcc, mfccdelta, spectralcentroid, zcr]

    # Creating the buttons
    for index, mode in enumerate(existingmode):
        create_button(mode, row=1, column=index+1)

    # Put everything together
    changemodeframe.pack()
    root.title(FILE_NAME)

    # launch the app
    root.mainloop()

if __name__ == "__main__":
    newwindow()