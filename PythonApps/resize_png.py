import tkinter as tk
from tkinter import messagebox
from PIL import Image
import io
import os

TARGET_SIZE = 45 * 1024  # 45 KB

def shrink_to_target(input_path, output_path, label):
    img = Image.open(input_path)
    fraction = 1.0

    while True:
        new_width = int(img.width * fraction)
        new_height = int(img.height * fraction)

        resized = img.resize((new_width, new_height), Image.LANCZOS)

        buffer = io.BytesIO()
        resized.save(buffer, format="PNG", optimize=True)
        size = buffer.tell()

        label.config(text=f"Trying {fraction:.2f} → {size/1024:.1f} KB")
        label.update()

        if size <= TARGET_SIZE:
            resized.save(output_path, optimize=True)
            label.config(text=f"Saved: {output_path} ({size/1024:.1f} KB)")
            return

        fraction *= 0.85

        if new_width < 10 or new_height < 10:
            label.config(text="Image became too small before reaching 45 KB.")
            return


def on_drop(event):
    file_path = event.data.strip("{}")

    if not file_path.lower().endswith(".png"):
        messagebox.showerror("Error", "Please drop a PNG file.")
        return

    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_compressed{ext}"

    status_label.config(text="Processing...")
    shrink_to_target(file_path, output_path, status_label)


# -----------------------------
# TkinterDnD ROOT (must be first)
# -----------------------------
try:
    import tkinterdnd2 as tkdnd
    root = tkdnd.TkinterDnD.Tk()
except ImportError:
    raise SystemExit("You must install tkinterdnd2: pip install tkinterdnd2")


# -----------------------------
# Modern UI Setup
# -----------------------------
root.title("PNG Compressor (<45 KB)")
root.geometry("500x300")
root.configure(bg="#ECECEC")

# Card container
card = tk.Frame(root, bg="white", bd=0, relief="flat")
card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=220)

title_label = tk.Label(
    card,
    text="PNG Compressor",
    font=("Segoe UI", 18, "bold"),
    bg="white",
    fg="#333"
)
title_label.pack(pady=(20, 10))

instructions = tk.Label(
    card,
    text="Drag and drop a PNG file below",
    font=("Segoe UI", 12),
    bg="white",
    fg="#555"
)
instructions.pack()

# Drop zone
drop_zone = tk.Label(
    card,
    text="Drop PNG Here",
    font=("Segoe UI", 14),
    bg="#F5F5F5",
    fg="#444",
    bd=2,
    relief="groove",
    width=30,
    height=3
)
drop_zone.pack(pady=15)

status_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 11),
    bg="white",
    fg="#333"
)
status_label.pack()


# Hover effect
def on_enter(e):
    drop_zone.config(bg="#E8E8E8")

def on_leave(e):
    drop_zone.config(bg="#F5F5F5")

drop_zone.bind("<Enter>", on_enter)
drop_zone.bind("<Leave>", on_leave)


# -----------------------------
# Drag-and-drop enablement
# -----------------------------
drop_zone.drop_target_register("*")
drop_zone.dnd_bind("<<Drop>>", on_drop)

root.mainloop()
