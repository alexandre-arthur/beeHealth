from scipy import signal

def notchFilter(soundData, notchFreq : int, sampleRate : int = 44100, qualityFactor : float = 30.0) :
    # Delete a specific frequency from a sound data
    # @arguments : - soundData : sound data to filter
    #              - notchFreq : frequency to delete
    #              - sampleRate : sample rate of the sound data (default : 44100 >>> For Audio sounds)
    #              - qualityFactor : quality factor of the filter (default : 30.0)
    # @return : sound data without the frequency


    # Create the notch filter
    bNotch, aNotch = signal.iirnotch(notchFreq, qualityFactor, sampleRate)

    # apply notch filter to signal
    soundNotched = signal.filtfilt(bNotch, aNotch, soundData)
    return soundNotched


def soundDataFilter(data, sampleRate : int, maxFrequency : int = None, minFrequency : int = None, freqFilter : list | int = None, filterOrder : int = 8):
    # Filter a sound data with a low pass filter and a notch filter (specific frequency)
    # @arguments : - data : sound data to filter
    #              - sampleRate : sample rate of the sound data (default : 44100 >>> For Audio sounds)
    #              - maxFrequency : maximum frequency to keep (default : None >>> No filter)
    #              - minFrequency : minimum frequency to keep (default : None >>> No filter)
    #              - freqFilter : frequency to delete (default : None >>> No filter)
    # @return : sound data filtered
    # @raise : Exception if maxFrequency is not an int or a list


    # Low pass filter
    if maxFrequency != None :
        sos = signal.butter(filterOrder, maxFrequency, 'lp', fs=sampleRate, output='sos') # Window
        filtered = signal.sosfilt(sos, data) # Filter
        data = filtered

    # High pass filter
    if minFrequency != None :
        sos = signal.butter(filterOrder, minFrequency, 'hp', fs=sampleRate, output='sos') # Window
        filtered = signal.sosfilt(sos, data) # Filter
        data = filtered

    # Notch filter
    if freqFilter != None:
        if isinstance(freqFilter, int) : 
            data = notchFilter(data, sampleRate, freqFilter)
        elif isinstance(freqFilter, list) :
            # Delete multiple frequencies
            for freq in freqFilter :
                data = notchFilter(data, sampleRate, freq)
        else :
            raise Exception(f"freq filter must be an int or a list but is {str(type(freqFilter))}.")

    return data