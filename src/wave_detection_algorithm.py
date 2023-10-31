import numpy as np
from scipy.signal import argrelextrema
from datetime import datetime
import pytz

def convert_to_kst(timestamp_ms):
    timestamp_utc = datetime.utcfromtimestamp(int(timestamp_ms) / 1000.0)
    kst = pytz.timezone('Asia/Seoul')
    timestamp_kst = timestamp_utc.replace(tzinfo=pytz.utc).astimezone(kst)
    return timestamp_kst

def find_peaks_and_troughs(data, order=5):
    peaks = argrelextrema(np.array(data), np.greater, order=order)[0]
    troughs = argrelextrema(np.array(data), np.less, order=order)[0]
    return peaks, troughs

def is_valid_elliott_wave(prices, peaks, troughs):
    if len(peaks) != 5 or len(troughs) != 3:
        return False
    if not(prices[troughs[0]] < prices[peaks[0]] < prices[troughs[1]] < prices[peaks[1]] < prices[troughs[2]] < prices[peaks[2]]):
        return False
    
    wave_1_length = prices[peaks[1]] - prices[troughs[0]]
    wave_3_length = prices[peaks[2]] - prices[troughs[1]]
    wave_5_length = prices[peaks[4]] - prices[troughs[2]]
    if wave_3_length < wave_1_length or wave_3_length < wave_5_length:
        return False
    if prices[troughs[2]] < prices[peaks[1]]:
        return False
    return True

def identify_elliott_waves(prices, peaks, troughs):
    valid_patterns = []
    
    num_peaks = len(peaks)
    num_troughs = len(troughs)
    
    if num_peaks < 5 or num_troughs < 3:
        return []
    
    for i in range(num_peaks - 4):
        for j in range(num_troughs - 2):
            selected_peaks = peaks[i:i+5]
            selected_troughs = troughs[j:j+3]
            if is_valid_elliott_wave(prices, selected_peaks, selected_troughs):
                valid_patterns.append((selected_peaks, selected_troughs))
                
    return valid_patterns

def describe_elliott_patterns(patterns, data, convert_to_kst):
    print("Patterns:", patterns)  # 디버그 코드 추가
    descriptions = []
    
    for peaks, troughs in patterns:
        pattern_description = (
            f"Elliott Wave Pattern Detected:\n"
            f"Wave 1: Peak at {convert_to_kst(data[peaks[0]][0])} and Trough at {convert_to_kst(data[troughs[0]][0])}\n"
            f"Wave 2: Peak at {convert_to_kst(data[peaks[1]][0])} and Trough at {convert_to_kst(data[troughs[1]][0])}\n"
            f"Wave 3: Peak at {convert_to_kst(data[peaks[2]][0])} and Trough at {convert_to_kst(data[troughs[2]][0])}\n"
            f"Wave 4: Peak at {convert_to_kst(data[peaks[3]][0])} and Trough at {convert_to_kst(data[troughs[2]][0])}\n"
            f"Wave 5: Peak at {convert_to_kst(data[peaks[4]][0])}"
        )
        descriptions.append(pattern_description)
    
    return "\n\n".join(descriptions)
