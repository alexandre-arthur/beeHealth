import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import GlobalFiguresBees as figs

def changeto_chromafeature():
    fig.clear()
    newax = fig.add_subplot(111)
    figs.plotfct_chromafeature(audio, sr, newax)
    canva.draw_idle()

def changeto_fft():
    fig.clear()
    newax = fig.add_subplot(111)
    figs.plotfct_FFT(audio, sr, newax)
    canva.draw_idle()

def changeto_mfcc():
    fig.clear()
    newax = fig.add_subplot(111)
    figs.plotfct_mfcc(audio, sr, newax)
    canva.draw_idle()

def changeto_chromatogram():
    fig.clear()
    newax = fig.add_subplot(111)
    figs.plotfct_chromatogram(audio, sr, newax)
    canva.draw_idle()


root = tk.Tk()
mainframe = tk.Frame(root, background="Blue")

fig = plt.Figure()
ax = fig.add_subplot(111)
canva = FigureCanvasTkAgg(fig, mainframe)
canva.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

FILE_NAME = 'Hive3_20_07_2017_QueenBee_H3_audio___06_20_00_21.wav'
PATH_NAME = 'Representation\BeeDataset\OnlyBees\QueenBee\\' + FILE_NAME
audio, sr = figs.getaudiofromfile(PATH_NAME)
figs.plotfct_FFT(audio, sr, ax)

mainframe.pack()

# Frame below with the buttons
changemodeframe = tk.Frame()

existingmode = ["fft", "mfcc", "chromatogram", "chromafeature"]

button = tk.Button(changemodeframe, text="FFT", command=changeto_fft)
button.grid(row=1, column=1)

button = tk.Button(changemodeframe, text="MFCC", command=changeto_mfcc)
button.grid(row=1, column=2)

button = tk.Button(changemodeframe, text="chromatogram", command=changeto_chromatogram)
button.grid(row=1, column=3)

button = tk.Button(changemodeframe, text="Chroma feature", command=changeto_chromafeature)
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
      

button_explore = tk.Button(changemodeframe,
                        text = "Browse Files",
                        command = browseFiles)
button_explore.grid(row=1, column=5, padx=20)


changemodeframe.pack()

root.mainloop()
