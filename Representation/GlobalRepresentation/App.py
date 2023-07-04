import tkinter as tk
import matplotlib.pyplot as plt
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import GlobalFiguresBees as figs
from classRepresentation import * 

root = tk.Tk()
mainframe = tk.Frame(root, background="Blue")

fig = plt.Figure()
ax = fig.add_subplot(111)
canva = FigureCanvasTkAgg(fig, mainframe)
canva.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

fft = FFTclass()
chromafeature = ChromaFeatureclass()
chromatogram = Chromatogramclass()
mfcc = MFCCclass()

# First example on startup
FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
audio, sr = figs.getaudiofromfile(PATH_NAME)
fft.plotfct(audio, sr, ax)

mainframe.pack()

# Frame below with the buttons
changemodeframe = tk.Frame()

button = tk.Button(changemodeframe, text="FFT", command=lambda : fft.changeto(audio, sr, fig, canva))
button.grid(row=1, column=1)

button = tk.Button(changemodeframe, text="MFCC", command=lambda : mfcc.changeto(audio, sr, fig, canva))
button.grid(row=1, column=2)

button = tk.Button(changemodeframe, text="chromatogram", command=lambda : chromatogram.changeto(audio, sr, fig, canva))
button.grid(row=1, column=3)

button = tk.Button(changemodeframe, text="Chroma feature", command=lambda : chromafeature.changeto(audio, sr, fig, canva))
button.grid(row=1, column=4)


# Frame to choose the audio to study

def browseFiles():
    global audio
    global sr
    filename = tk.filedialog.askopenfilename(
        initialdir = "Representation\BeeDataset\\",
        title = "Select a File",
        filetypes = (("wav files", "*.wav"), ("None", ""))
    )

    if filename != "":
        audio, sr = figs.getaudiofromfile(filename)

        fft.changeto(audio, sr, fig, canva)
        filename = filename.split('/', 100)[-1] # Only get the file name and no the path
        root.title(filename)
      
button_explore = tk.Button(changemodeframe,
                        text = "Browse Files",
                        command = browseFiles)
button_explore.grid(row=1, column=5, padx=20)


changemodeframe.pack()
root.title(FILE_NAME)
root.mainloop()
