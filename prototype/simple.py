import numpy as np

class Frame:
    BUFFER_SIZES = [512, 1024, 2048]

    def __init__(self) -> None:
        self.samples = np.zeros(1) # change with actual buffer later

    def get_samples(self) -> np.ndarray:
        return self.samples[0]
    
    def update_samples(self, new_num: int) -> None:
        self.samples[0] = new_num

class Window:
    FRAME_WINDOW = 5
    def __init__(self) -> None:
        self.frames = [Frame() for _ in range(self.FRAME_WINDOW)]
        for f in range(self.FRAME_WINDOW):
            self.frames[f].update_samples(f)

        # Trackers
        self.writeIndex = 0
        self.newest_index = (self.writeIndex - 1) % self.FRAME_WINDOW
        self.frameRelations = [
            (self.newest_index - 4) % self.FRAME_WINDOW,  # 2nd past frame
            (self.newest_index - 3) % self.FRAME_WINDOW,  # 1st past frame
            (self.newest_index - 2) % self.FRAME_WINDOW,  # focus frame
            (self.newest_index - 1) % self.FRAME_WINDOW,  # 1st future frame
            self.newest_index                             # 2nd future frame
        ]

    def sync_trackers(self) -> None:
        loc_range = self.FRAME_WINDOW - 1
        self.writeIndex = (self.writeIndex + 1) % self.FRAME_WINDOW
        self.newest_index = (self.writeIndex - 1) % self.FRAME_WINDOW

        for i in range(loc_range):
            self.frameRelations[i] = (self.newest_index - (loc_range - i)) % self.FRAME_WINDOW

        self.frameRelations[loc_range] = self.newest_index

    def add_frame(self, new_frame) -> None:
        self.frames[self.writeIndex].update_samples(new_frame)
        self.sync_trackers()
        
    def get_frames(self) -> list[Frame]:
        return self.frames

    def print_trackers(self) -> None:
        print(f"        |  P 2  |  P 1  |  CUR  |  F 1  |  F 2  |")            
        print(f"Trackers|   ", end="")
        for t in self.frameRelations:
            print(f"{t}", end="   |   ")
        print("\n")

    def print_window(self):
        print(f"index   |   0   |   1   |   2   |   3   |   4   |")
        print(f"array", end="   |   ")
        for c in self.get_frames():
            print(f"{int(c.get_samples())}", end="   |   ")

        print("\n")


win = Window()
print(0%1024)
# print("---- raw array ----")
win.print_trackers()
win.print_window()

app_inp = input("\nnumber to append:- ")
while app_inp != "":
    win.add_frame(app_inp)
    win.print_trackers()
    win.print_window()
    app_inp = input("\nnumber to append:- ")
