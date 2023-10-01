import numpy as np
import matplotlib.pyplot as plt

def find_peaks_and_troughs(data):
    peaks = np.where((data[:-2] < data[1:-1]) & (data[1:-1] > data[2:]))[0] + 1
    troughs = np.where((data[:-2] > data[1:-1]) & (data[1:-1] < data[2:]))[0] + 1
    return peaks, troughs

def plot_waves(data, peaks, troughs):
    plt.figure(figsize=(15,7))
    plt.plot(data, '-o', label='Data')
    plt.plot(peaks, data[peaks], 'ro', label='Peaks')
    plt.plot(troughs, data[troughs], 'bo', label='Troughs')
    plt.legend()
    plt.title('Peaks and Troughs in Data')
    plt.show()

if __name__ == "__main__":
    import btcusdt_data

    all_data = btcusdt_data.main()
    prices = [float(item[4]) for item in all_data]

    peaks, troughs = find_peaks_and_troughs(prices)
    plot_waves(prices, peaks, troughs)
