import tkinter as tk
import time

class TimeTrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Tracker")
        self.geometry("300x200")

        self.start_time = None
        self.paused_time = 0
        self.is_paused = False
        self.is_finished = False

        self.target_work_hours = 12 * 60 * 60  # Target work hours in seconds

        self.elapsed_time_label = tk.Label(self, text="Elapsed Time: 00:00:00", font=("Arial", 16))
        self.elapsed_time_label.pack(pady=20)

        self.remaining_time_label = tk.Label(self, text="Remaining Time: 12:00:00", font=("Arial", 12))
        self.remaining_time_label.pack(pady=5)

        self.start_button = tk.Button(self, text="Start", command=self.start_timer)
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(self, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_button.pack(pady=10)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset_timer, state="disabled")
        self.reset_button.pack(pady=10)

        self.finish_button = tk.Button(self, text="Finish", command=self.finish_timer, state="disabled")
        self.finish_button.pack(pady=10)

    def start_timer(self):
        self.start_time = time.time()
        self.is_paused = False
        self.is_finished = False
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.finish_button.config(state="normal")
        self.update_time()

    def pause_timer(self):
        if not self.is_paused and not self.is_finished:
            self.paused_time += time.time() - self.start_time
            self.is_paused = True
            self.pause_button.config(text="Resume")
        else:
            self.start_time = time.time() - self.paused_time
            self.is_paused = False
            self.pause_button.config(text="Pause")
        self.update_time()

    def reset_timer(self):
        if not self.is_finished:
            self.start_time = None
            self.paused_time = 0
            self.is_paused = False
            self.elapsed_time_label.config(text="Elapsed Time: 00:00:00")
            self.remaining_time_label.config(text="Remaining Time: 12:00:00")
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled")
            self.reset_button.config(state="disabled")
            self.finish_button.config(state="disabled")

    def finish_timer(self):
        self.is_finished = True
        self.start_button.config(state="disabled")
        self.pause_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.finish_button.config(state="disabled")

        total_time = self.elapsed_time()
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = int(total_time % 60)

        with open("output.txt", "w") as f:
            f.write(f"Total Time Worked: {hours:02d}:{minutes:02d}:{seconds:02d} out of 12 hours")

    def elapsed_time(self):
        if self.start_time:
            return time.time() - self.start_time - self.paused_time
        else:
            return 0

    def update_time(self):
        if not self.is_paused and not self.is_finished:
            elapsed_time = self.elapsed_time()
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)

            self.elapsed_time_label.config(text=f"Elapsed Time: {hours:02d}:{minutes:02d}:{seconds:02d}")

            remaining_time = self.target_work_hours - elapsed_time
            remaining_hours = int(remaining_time // 3600)
            remaining_minutes = int((remaining_time % 3600) // 60)
            remaining_seconds = int(remaining_time % 60)
            self.remaining_time_label.config(text=f"Remaining Time: {remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}")

        self.after(1000, self.update_time)

if __name__ == "__main__":
    app = TimeTrackerGUI()
    app.mainloop()
