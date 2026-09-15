# WAV in → frames → features → plots → rough categories
# silence = grey
# voiced = blue
# sibilance = yellow
# plosive = red
# breath = purple
# transition = orange

import random as rand
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.io import wavfile

def dummy_func(n: int) -> None:
    """Calculates the average velocity of a moving object.

    Args:
        distance: The total distance traveled in meters.
        time: The total time taken in seconds. Must be greater than zero.

    Returns:
        The average velocity in meters per second.

    Raises:
        ValueError: If time is less than or equal to zero.
    """
    return None

class Frame:
    COLORS = ["white", "black", "red", "blue", "green", "orange", "purple", "brown", "pink", "gray", "olive", "cyan"]
    def __init__(self, buffer_size: int) -> None:
        self.samples = np.zeros(buffer_size)
        r_color = rand.randint(0, len(self.COLORS)-1)
        self.color = self.COLORS[r_color]

    def get_samples(self) -> np.ndarray:
        return self.samples

    def get_color(self) -> str:
        return self.color

    def update_samples(self, new_samples: np.ndarray) -> None:
        self.samples = np.copy(new_samples)

class Window:
    FRAME_SIZES = [512, 1024, 2048]
    WINDOW_FRAMES = 5
    def __init__(self, buffer_choice: int) -> None:
        self.buffer_choice = self.FRAME_SIZES[buffer_choice]
        self.frames = [Frame(self.buffer_choice) for _ in range(self.WINDOW_FRAMES)]

        # Trackers
        self.write_index = 0
        self.newest_index = (self.write_index - 1) % self.WINDOW_FRAMES
        self.frameRelations = [
            (self.newest_index - 4) % self.WINDOW_FRAMES,  # 2nd past frame
            (self.newest_index - 3) % self.WINDOW_FRAMES,  # 1st past frame
            (self.newest_index - 2) % self.WINDOW_FRAMES,  # focus frame
            (self.newest_index - 1) % self.WINDOW_FRAMES,  # 1st future frame
            self.newest_index                              # 2nd future frame
        ]

    def get_buffer_window(self):
        return self.buffer_choice, self.WINDOW_FRAMES
    
    def sync_trackers(self) -> None:
        loc_range = self.WINDOW_FRAMES - 1
        self.write_index = (self.write_index + 1) % self.WINDOW_FRAMES
        self.newest_index = (self.write_index - 1) % self.WINDOW_FRAMES

        for i in range(loc_range):
            self.frameRelations[i] = (self.newest_index - (loc_range - i)) % self.WINDOW_FRAMES

        self.frameRelations[loc_range] = self.newest_index

    def add_frame(self, new_frame: np.ndarray) -> int:
        # Adds (more accurately, updates) and syncs frame into window
        # Returns which frame is updated
        writing_to = self.write_index
        self.frames[writing_to].update_samples(new_frame)
        self.sync_trackers()

        # TODO: extract desired features/info from frames

        return writing_to
        
    def get_frames(self) -> list[Frame]:
        return self.frames

    def print_window(self) -> None:
        # print(f"index   |   0   |   1   |   2   |   3   |   4   |")
        print(f"Window Frames", end="   |   ")
        for c in self.get_frames():
            print(f"{c.get_samples()}", end="   |   ")

        print("\n")


# Test file
file_path = r"ASMR Historian-1816\becauseIts.wav"
sample_rate, audio = wavfile.read(file_path)

# If stereo, convert to mono, then int audio to float [-1,1]
if audio.ndim > 1:
    audio = audio.mean(axis=1)
if audio.dtype != np.float32 and audio.dtype != np.float64:
    audio = audio / np.max(np.abs(audio))


# Frames -> 1024 samples per frame
len_samples = np.shape(audio)[0]
time = np.arange(len_samples) / sample_rate

# prompt_input = "1"
# while prompt_input.strip() == "1":

win = Window(1)
frame_size, window_frames = win.get_buffer_window()
half_size = frame_size // 2

# stores "realtime" samples as they come in
passing_samples = np.zeros(frame_size, dtype=np.float32)
is_history_full = False
sample_tracker = 0
write_pos = 0

frame_colors = []

for i in range(len_samples):
    write_pos = sample_tracker % frame_size
    passing_samples[write_pos] = audio[i]

    sample_tracker += 1

    # store formed frame slices
    if sample_tracker >= frame_size and sample_tracker % half_size == 0:
        if sample_tracker % frame_size == 0:
            new_frame = win.add_frame(passing_samples)
            frame_colors.append(win.get_frames()[new_frame].get_color())
        else:
            curr_frame = np.append(passing_samples[half_size:], passing_samples[:half_size])
            new_frame = win.add_frame(curr_frame)
            frame_colors.append(win.get_frames()[new_frame].get_color())


win.print_window()

# prompt to stop/restart
# prompt_input = input("[1]   Start/Reset   |   [2]   End         |\n ---> ")

# VISUAL PLOTTING
# build line segments per hop
segments = []
segment_colors = []

for frame_idx, color in enumerate(frame_colors):
    start = frame_idx * half_size
    end = min(start + half_size, len(audio))

    if end - start < 2:
        break

    x = time[start:end]
    y = audio[start:end]

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    line_segments = np.concatenate([points[:-1], points[1:]], axis=1)

    segments.extend(line_segments)
    segment_colors.extend([color] * len(line_segments))

fig, ax = plt.subplots(figsize=(14, 4))

lc = LineCollection(segments, colors=segment_colors, linewidths=0.8)
ax.add_collection(lc)

ax.set_xlim(time[0], time[-1])
ax.set_ylim(np.min(audio), np.max(audio))

ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_title("Waveform colored by frame category")

plt.show()