import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import copy


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor App")
        self.root.geometry("1200x600")
        self.root.config(bg="White")  # Set background to white

        self.original_image = None
        self.display_image = None
        self.tk_image = None
        self.cropped_image = None
        self.undo_stack = []
        self.redo_stack = []

        # UI Components
        self.canvas = tk.Canvas(root, bg="#9E9E9E", width=600, height=400)
        # Left side canvas for original image
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.cropped_canvas = tk.Canvas(
            root, bg="#9E9E9E", width=600, height=400)
        # Right side canvas for edited image
        self.cropped_canvas.grid(row=0, column=1, padx=10, pady=10)

        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.draw_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_crop)

        # Button styling
        button_frame = tk.Frame(root, bg="white")
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.create_button(button_frame, "Load Image", self.load_image)
        self.create_button(button_frame, "Save Image", self.save_image)
        self.create_button(button_frame, "Grayscale", self.to_grayscale)
        self.create_button(button_frame, "Blur", self.apply_blur)
        self.create_button(button_frame, "Undo", self.undo)
        self.create_button(button_frame, "Redo", self.redo)
        self.create_button(button_frame, "Rotate 90°", self.rotate_image)
        self.create_button(button_frame, "Crop", self.crop_image)

        # Resize Slider
        self.slider = tk.Scale(root, from_=10, to=300, orient=tk.HORIZONTAL,
                               label="Resize %", command=self.resize_image)
        self.slider.set(100)
        self.slider.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Keyboard shortcuts
        root.bind("<Control-s>", lambda e: self.save_image())
        root.bind("<Control-z>", lambda e: self.undo())
        root.bind("<Control-y>", lambda e: self.redo())
        root.bind("<Control-r>", lambda e: self.rotate_image())

        self.start_x = self.start_y = self.rect = None

    def create_button(self, frame, text, command):
        btn = tk.Button(frame, text=text, command=command, font=(
            'Arial', 12, 'bold'), bg="#1E90FF", fg="white", relief="raised", bd=5, height=2, width=12)
        btn.grid(row=0, column=frame.grid_size()[0], padx=5, pady=5)

    def update_canvas_with_image(self, img, canvas):
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(image_rgb)
        tk_img = ImageTk.PhotoImage(pil_img)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        canvas.image = tk_img  # Keep a reference to the image

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original_image = cv2.imread(path)
            self.display_image = self.original_image.copy()
            self.undo_stack.clear()
            self.update_canvas()

    def update_canvas(self):
        if self.display_image is not None:
            image = cv2.cvtColor(self.display_image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = image.resize((600, 400))
            self.tk_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def save_image(self):
        if self.cropped_image is not None:
            image_to_save = self.cropped_image
        elif self.display_image is not None:
            image_to_save = self.display_image
        else:
            messagebox.showwarning("No Image", "There is no image to save.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if path:
            cv2.imwrite(path, image_to_save)
            messagebox.showinfo("Saved", "Image saved successfully!")

    def start_crop(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)

    def draw_crop(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline='red')

    def end_crop(self, event):
        pass  # Crop coordinates are handled in the crop button action

    def crop_image(self):
        if self.display_image is None or not self.rect:
            return
        # Get the cropping coordinates
        x0, y0, x1, y1 = self.canvas.coords(self.rect)
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)

        # Ensure proper coordinates for cropping
        if x1 - x0 > 10 and y1 - y0 > 10:
            self.push_undo()
            self.cropped_image = self.display_image[y0:y1, x0:x1]
            self.update_canvas_with_image(
                self.cropped_image, self.cropped_canvas)

    def resize_image(self, value):
        if self.display_image is None:
            return
        scale = int(value) / 91.0
        w = int(self.display_image.shape[1] * scale)
        h = int(self.display_image.shape[0] * scale)
        resized = cv2.resize(self.display_image, (w, h))
        self.update_canvas_with_image(resized, self.cropped_canvas)

    def to_grayscale(self):
        if self.display_image is not None:
            self.push_undo()
            self.display_image = cv2.cvtColor(
                self.display_image, cv2.COLOR_BGR2GRAY)
            self.display_image = cv2.cvtColor(
                self.display_image, cv2.COLOR_GRAY2BGR)
            self.update_canvas_with_image(
                self.display_image, self.cropped_canvas)

    def apply_blur(self):
        if self.display_image is not None:
            self.push_undo()
            self.display_image = cv2.GaussianBlur(
                self.display_image, (15, 15), 0)
            self.update_canvas_with_image(
                self.display_image, self.cropped_canvas)

    def push_undo(self):
        if self.display_image is not None:
            self.undo_stack.append(copy.deepcopy(self.display_image))
            self.redo_stack.clear()

    def rotate_image(self):
        if self.display_image is not None:
            self.push_undo()
            self.display_image = cv2.rotate(
                self.display_image, cv2.ROTATE_90_CLOCKWISE)
            self.update_canvas_with_image(
                self.display_image, self.cropped_canvas)

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(copy.deepcopy(self.display_image))
            self.display_image = self.undo_stack.pop()
            self.update_canvas_with_image(
                self.display_image, self.cropped_canvas)

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(copy.deepcopy(self.display_image))
            self.display_image = self.redo_stack.pop()
            self.update_canvas_with_image(
                self.display_image, self.cropped_canvas)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
