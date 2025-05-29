# %YourCuisineSelector%
import tkinter as tk
from tkinter import messagebox
import random
import math
import time

class CuisineWheel:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Cuisine Selector")
        self.root.geometry("400x500")

        # List of cuisines
        self.cuisines = [
            "Italian", "Chinese", "Mexican", "Indian", "Japanese",
            "Thai", "French", "Greek", "American", "Korean"
        ]
        self.num_segments = len(self.cuisines)
        self.angle_per_segment = 360 / self.num_segments
        self.current_angle = 0
        self.spinning = False

        # Colors for wheel segments (distinct for visibility)
        self.colors = [
            "#FF6347", "#FFD700", "#ADFF2F", "#20B2AA", "#9370DB",
            "#FF4500", "#00CED1", "#FF69B4", "#228B22", "#BA55D3"
        ]

        # GUI components
        self.label = tk.Label(root, text="What to eat today?", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack(pady=20)

        self.result_label = tk.Label(root, text="Cuisine: None", font=("Helvetica", 12, "bold"))
        self.result_label.pack(pady=10)

        self.spin_button = tk.Button(root, text="Spin and no regret!", command=self.start_spin, font=("Helvetica", 12))
        self.spin_button.pack(pady=10)

        # Draw initial wheel
        self.draw_wheel()

    def draw_wheel(self):
        self.canvas.delete("all")
        center_x, center_y = 150, 150
        radius = 120

        # Draw wheel segments
        for i in range(self.num_segments):
            start_angle = self.current_angle + i * self.angle_per_segment
            self.canvas.create_arc(
                center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                start=start_angle, extent=self.angle_per_segment, fill=self.colors[i], outline="black"
            )
            # Calculate text position
            text_angle = math.radians(start_angle + self.angle_per_segment / 2)
            text_x = center_x + (radius * 0.7) * math.cos(text_angle)
            text_y = center_y - (radius * 0.7) * math.sin(text_angle)
            # Rotate cuisine text to align with segments
            self.canvas.create_text(
                text_x, text_y, text=self.cuisines[i], font=("Helvetica", 10),
                angle=-(start_angle + self.angle_per_segment / 2)
            )

        # Draw pointer (triangle pointing down)
        self.canvas.create_polygon(
            [center_x - 10, center_y - radius - 10, center_x + 10, center_y - radius - 10, center_x, center_y - radius],
            fill="red", outline="black"
        )

    def start_spin(self):
        if self.spinning:
            return
        self.spinning = True
        self.spin_button.config(state="disabled")
        self.result_label.config(text="Cuisine: Spinning...")

        # Simulate spinning with random rotations
        total_rotations = random.randint(3, 6) * 360 + random.uniform(0, 360)
        steps = 50
        step_angle = total_rotations / steps
        current_step = 0

        def animate():
            nonlocal current_step
            if current_step < steps:
                self.current_angle = (self.current_angle + step_angle) % 360
                self.draw_wheel()
                current_step += 1
                self.root.after(50, animate)
            else:
                self.stop_spin()

        animate()

    def stop_spin(self):
        self.spinning = False
        self.spin_button.config(state="normal")

        # Calculate selected segment
        pointer_angle = (360 - self.current_angle) % 360
        selected_index = int(pointer_angle // self.angle_per_segment) % self.num_segments
        selected_cuisine = self.cuisines[selected_index]

        self.result_label.config(text=f"Cuisine: {selected_cuisine}")
        messagebox.showinfo("Result", f"Let's eat {selected_cuisine} cuisine today!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CuisineWheel(root)
    root.mainloop()


