# 🧠 BF Image Interpreter

A small experimental toolchain that converts images into BF code and renders them back as grayscale images using a custom interpreter.

---

## 🖼️ What this project does

This project treats images as a stream of grayscale pixel values encoded in BF.

It can:

- Convert PNG images → `.bf` files  
- Decode `.bf` files → grayscale images  
- Render pixel data from BF output  
- Use fixed height (64px) with auto-scaled width  

---

## ⚙️ How it works

### 🧠 Encoding (converter.py)

1. Load image (example: `cat.png`)
2. Convert to grayscale (0–255)
3. Resize to height = 64
4. Scale width proportionally
5. Convert pixels into BF code
6. Save output as:

NAME(WIDTH).bf

---

### 🖼️ Decoding (interpreter.py)

1. Execute BF code
2. Each `.` outputs one pixel value
3. Collect pixel stream
4. Reshape into:

WIDTH × 64 image

5. Render grayscale image  

---

## 🧠 BF format used

This is a custom BF-based image format, not standard BF.

| Command | Meaning |
|--------|--------|
| `+` | increase pixel value |
| `-` | decrease pixel value |
| `.` | output pixel value |
| `>` | move pointer right |
| `<` | move pointer left |

Pixel values:

0   = black  
255 = white  

---

## ▶️ How to use

### 1. Convert image → BF

python converter.py cat.png

Or drag & drop PNG onto converter.py (Windows)

---

### 2. Or use batch file

Double-click:

run.bat

---

## 📁 Output format rules

64×64 image → NAME.bf  
Other sizes → NAME(WIDTH).bf  

Example:

cat.png → cat.bf  
dog.png → dog(32).bf  

---

## 🖼️ Example

-.>.<.>.<..>.<.>.<......>.<...>..<...>.<.>...<.
<p align="center">
  <img src="smile.png" width="150"
  style="image-rendering: pixelated; image-rendering: crisp-edges;" />
</p>

---

## 📦 Requirements

pip install pillow

---

## 📝Notes

don't try input(,) does nothing  
loops([ ]) do work
