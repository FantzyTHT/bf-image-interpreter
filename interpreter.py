import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import math

# =========================
# Brainfuck Interpreter
# =========================

def brainfuck(code):
    tape = [0] * 30000
    ptr = 0
    pc = 0
    output = []

    loop_map = {}
    stack = []

    # Build loop map
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if not stack:
                raise ValueError(f"Unmatched ] at position {i}")

            j = stack.pop()
            loop_map[i] = j
            loop_map[j] = i

    if stack:
        raise ValueError("Unmatched [")

    while pc < len(code):
        c = code[pc]

        if c == '>':
            ptr += 1
            if ptr >= len(tape):
                tape.append(0)

        elif c == '<':
            ptr = max(0, ptr - 1)

        elif c == '+':
            tape[ptr] = (tape[ptr] + 1) % 256

        elif c == '-':
            tape[ptr] = (tape[ptr] - 1) % 256

        elif c == '.':
            output.append(tape[ptr])

        elif c == '[':
            if tape[ptr] == 0:
                pc = loop_map[pc]

        elif c == ']':
            if tape[ptr] != 0:
                pc = loop_map[pc]

        pc += 1

    return output

# =========================
# GUI Functions
# =========================

def open_file():
    filename = filedialog.askopenfilename(
        filetypes=[
            ("Brainfuck Files", "*.bf"),
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if not filename:
        return

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

        code_text.delete("1.0", tk.END)
        code_text.insert("1.0", code)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_code():
    try:
        code = code_text.get("1.0", tk.END)

        data = brainfuck(code)

        if len(data) == 0:
            messagebox.showerror(
                "Error",
                "Program produced no output."
            )
            return

        if auto_square_var.get():
            size = math.ceil(math.sqrt(len(data)))
            width = size
            height = size
        else:
            width = int(width_entry.get())
            height = int(height_entry.get())

            if width <= 0 or height <= 0:
                raise ValueError("Width and height must be greater than 0.")

        expected = width * height

        if len(data) < expected:
            data.extend([0] * (expected - len(data)))
        else:
            data = data[:expected]

        arr = np.array(data, dtype=np.uint8).reshape((height, width))

        img = Image.fromarray(arr, mode="L")

        # Scale small images up
        scale = max(1, min(512 // max(width, height), 20))

        img = img.resize(
            (width * scale, height * scale),
            Image.Resampling.NEAREST
        )

        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_label.image = photo

        info_label.config(
            text=f"Pixels: {len(data)} | Image: {width} × {height}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def save_image():
    try:
        if not hasattr(image_label, "image"):
            messagebox.showerror(
                "Error",
                "No image has been generated yet."
            )
            return

        code = code_text.get("1.0", tk.END)
        data = brainfuck(code)

        if auto_square_var.get():
            size = math.ceil(math.sqrt(len(data)))
            width = size
            height = size
        else:
            width = int(width_entry.get())
            height = int(height_entry.get())

        expected = width * height

        if len(data) < expected:
            data.extend([0] * (expected - len(data)))
        else:
            data = data[:expected]

        arr = np.array(data, dtype=np.uint8).reshape((height, width))

        img = Image.fromarray(arr, mode="L")

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png")
            ]
        )

        if filename:
            img.save(filename)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# =========================
# GUI
# =========================

root = tk.Tk()
root.title("Brainfuck Image Viewer")
root.geometry("900x800")

top_frame = tk.Frame(root)
top_frame.pack(fill="x", padx=5, pady=5)

open_btn = tk.Button(
    top_frame,
    text="Open .bf",
    command=open_file
)
open_btn.pack(side="left", padx=2)

run_btn = tk.Button(
    top_frame,
    text="Run",
    command=run_code
)
run_btn.pack(side="left", padx=2)

save_btn = tk.Button(
    top_frame,
    text="Save PNG",
    command=save_image
)
save_btn.pack(side="left", padx=2)

tk.Label(top_frame, text="Width").pack(side="left", padx=(15, 2))

width_entry = tk.Entry(top_frame, width=6)
width_entry.insert(0, "64")
width_entry.pack(side="left")

tk.Label(top_frame, text="Height").pack(side="left", padx=(10, 2))

height_entry = tk.Entry(top_frame, width=6)
height_entry.insert(0, "64")
height_entry.pack(side="left")

auto_square_var = tk.BooleanVar()

auto_square_checkbox = tk.Checkbutton(
    top_frame,
    text="Auto Square",
    variable=auto_square_var
)
auto_square_checkbox.pack(side="left", padx=10)

code_text = tk.Text(
    root,
    width=100,
    height=20,
    font=("Consolas", 10)
)
code_text.pack(
    fill="both",
    expand=False,
    padx=5,
    pady=5
)

info_label = tk.Label(
    root,
    text="No image generated"
)
info_label.pack(pady=5)

image_label = tk.Label(root)
image_label.pack(expand=True)

root.mainloop()