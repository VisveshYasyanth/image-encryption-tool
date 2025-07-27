import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import random
import pickle

# --- Encryption & Decryption Logic ---

def encrypt_image_with_swap(img_path, output_path, key):
    img = Image.open(img_path)
    pixels = list(img.getdata())
    random.seed(key)
    swaps = []

    for _ in range(len(pixels) // 2):
        i, j = random.sample(range(len(pixels)), 2)
        pixels[i], pixels[j] = pixels[j], pixels[i]
        swaps.append((i, j))

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(pixels)
    new_img.save(output_path)

    with open(output_path + ".swp", "wb") as f:
        pickle.dump(swaps, f)

def decrypt_image_with_swap(img_path, output_path, key):
    img = Image.open(img_path)
    pixels = list(img.getdata())

    try:
        with open(img_path + ".swp", "rb") as f:
            swaps = pickle.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Swap file not found for decryption.")
        return

    for i, j in reversed(swaps):
        pixels[i], pixels[j] = pixels[j], pixels[i]

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(pixels)
    new_img.save(output_path)

def encrypt_image_with_math(img_path, output_path, key):
    img = Image.open(img_path)
    pixels = list(img.getdata())

    new_pixels = []
    for pixel in pixels:
        if isinstance(pixel, int):
            new_pixels.append(pixel ^ key)
        else:
            new_pixels.append(tuple(p ^ key for p in pixel))

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path)

decrypt_image_with_math = encrypt_image_with_math

# --- GUI Application ---

class ImageEncryptorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Encryption Tool")
        self.master.configure(bg="#111111")
        self.file_path = None

        tk.Label(master, text="Image Encryption Tool", font=("Lucida Handwriting", 22, "bold"),
                 fg="#cc6655", bg="#111111").pack(pady=10)

        tk.Button(master, text="Choose Image", command=self.choose_image,
                  bg="#333333", fg="#cc6655", font=("Century Gothic", 12)).pack(pady=5)

        tk.Label(master, text="Select Method:", bg="#111111", fg="#cc6655",
                 font=("Trebuchet MS", 12)).pack(pady=5)
        self.method_var = tk.StringVar(value='swap')
        ttk.Combobox(master, textvariable=self.method_var, values=["swap", "math"],
                     font=("Georgia", 11)).pack(pady=5)

        tk.Label(master, text="Enter Key:", bg="#111111", fg="#cc6655",
                 font=("Trebuchet MS", 12)).pack(pady=5)
        self.key_entry = tk.Entry(master, font=("Georgia", 11))
        self.key_entry.pack(pady=5)

        tk.Button(master, text="Encrypt Image", command=self.encrypt_image,
                  bg="#333333", fg="#cc6655", font=("Century Gothic", 12)).pack(pady=5)
        tk.Button(master, text="Decrypt Image", command=self.decrypt_image,
                  bg="#333333", fg="#cc6655", font=("Century Gothic", 12)).pack(pady=5)

        self.image_label = tk.Label(master, bg="#111111")
        self.image_label.pack(pady=10)

    def choose_image(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
        path = filedialog.askopenfilename(title="Select Image", filetypes=filetypes)
        if path:
            self.file_path = path
            img = Image.open(path)
            img.thumbnail((300, 300))
            self.tk_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_img)

    def encrypt_image(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please choose an image.")
            return
        method = self.method_var.get()
        try:
            key = int(self.key_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid numeric key.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", title="Save Encrypted Image")
        if output_path:
            if method == "swap":
                encrypt_image_with_swap(self.file_path, output_path, key)
            else:
                encrypt_image_with_math(self.file_path, output_path, key)
            messagebox.showinfo("Success", "Image encrypted and saved.")

    def decrypt_image(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please choose an image.")
            return
        method = self.method_var.get()
        try:
            key = int(self.key_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid numeric key.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", title="Save Decrypted Image")
        if output_path:
            if method == "swap":
                decrypt_image_with_swap(self.file_path, output_path, key)
            else:
                decrypt_image_with_math(self.file_path, output_path, key)
            messagebox.showinfo("Success", "Image decrypted and saved.")

# --- Run Application ---

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEncryptorApp(root)
    root.mainloop()
