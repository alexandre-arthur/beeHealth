from scipy import signal

# Suppress all the freq at a notch_freq
def notch_filter(y_pure, samp_freq : int, notch_freq : int) :
    # Create/view notch filter
    # Frequency to be removed from signal (Hz)
    quality_factor = 30.0  # Quality factor
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)

    # apply notch filter to signal
    y_notched = signal.filtfilt(b_notch, a_notch, y_pure)
    return y_notched

# Delete the sepecific frequency from a sound data and add a low pass filter at maxFrquency
def sounddata_filter(data, sample_rate : int, maxFrequency : int = None, freq_filter : list | int = None):
    if maxFrequency != None :
            CUT_OFF_FREQUENCY = maxFrequency
            FILTER_ORDER = 8
            sos = signal.butter(FILTER_ORDER, CUT_OFF_FREQUENCY, 'lp', fs=sample_rate, output='sos') # Window
            filtered = signal.sosfilt(sos, data) # Filter
            data = filtered
    if freq_filter != None:
        if isinstance(freq_filter, int) : 
            data = notch_filter(data, sample_rate, freq_filter)
        elif isinstance(freq_filter, list)  :
            for freq in freq_filter :
                data = notch_filter(data, sample_rate, freq)
        else :
            raise Exception('freq filter must be an int or a list but is ' + str(type(freq_filter)) + ".")
    return data