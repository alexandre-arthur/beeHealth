import tkinter as tk
import matplotlib.pyplot as plt
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GlobalFiguresBees import * 
from classRepresentation import * 


def newwindow():
    root = tk.Tk()
    mainframe = tk.Frame(root, background="Blue")

    def browseFiles():
        global audio
        global sr
        filename = tk.filedialog.askopenfilename(
            initialdir = "Representation\BeeDataset\\",
            title = "Select a File",
            filetypes = (("wav files", "*.wav"), ("None", ""))
        )

        if filename != "":
            audio, sr = getaudiofromfile(filename)

            fft.changeto(audio, sr, fig, canva)
            filename = filename.split('/', 100)[-1] # Only get the file name and no the path
            root.title(filename)

    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open audio file...", command=browseFiles, accelerator="Ctrl+O")
    root.bind_all("<Control-o>", lambda event: browseFiles())

    filemenu.add_command(label="Detailed window", command=showAllRepresentation)

    filemenu.add_command(label="New window", command=newwindow, accelerator="Ctrl+N")
    root.bind_all("<Control-n>", lambda event: newwindow())

    filemenu.add_command(label="Quit", command=root.destroy, accelerator="Ctrl+W")
    root.bind_all("<Control-w>", lambda event: root.destroy())
    
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    fig = plt.Figure()
    ax = fig.add_subplot(111)
    canva = FigureCanvasTkAgg(fig, mainframe)
    canva.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    wave = Waveclass()
    fft = FFTclass()
    chromafeature = ChromaFeatureclass()
    chromatogram = Chromatogramclass()
    mfcc = MFCCclass()

    # First example on startup
    FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
    PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
    audio, sr = getaudiofromfile(PATH_NAME)
    fft.plotfct(audio, sr, ax)

    mainframe.pack()

    # Frame below with the buttons
    changemodeframe = tk.Frame(root, bg="white")

    button = tk.Button(changemodeframe, text="Wave", command=lambda : wave.changeto(audio, sr, fig, canva))
    button.grid(row=1, column=1)

    button = tk.Button(changemodeframe, text="FFT", command=lambda : fft.changeto(audio, sr, fig, canva))
    button.grid(row=1, column=2)

    button = tk.Button(changemodeframe, text="MFCC", command=lambda : mfcc.changeto(audio, sr, fig, canva))
    button.grid(row=1, column=3)

    button = tk.Button(changemodeframe, text="chromatogram", command=lambda : chromatogram.changeto(audio, sr, fig, canva))
    button.grid(row=1, column=4)

    button = tk.Button(changemodeframe, text="Chroma feature", command=lambda : chromafeature.changeto(audio, sr, fig, canva))
    button.grid(row=1, column=5)

    changemodeframe.pack()
    root.title(FILE_NAME)
    root.mainloop()

if __name__ == "__main__":
    newwindow()