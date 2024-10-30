import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

with open('data.json', 'r') as f:
    text = json.load(f)

def point(c):
    font = "Courier"
    size = 40
    longest = max(text, key=len)
    print(longest)
    width, height = letter
    max_width = width - 50
    x = 30
    while c.stringWidth(longest, font, size) > max_width and size > 1:
        size -= 0.5
    return size

def write(name):
    c = canvas.Canvas(name, pagesize=letter)
    size = point(c)
    c.setFont("Courier", size)
    for i in range(len(text)):
        c.drawString(30, 750 - (i*size), text[i])
    c.save()

os.remove("output.pdf")
write("output.pdf")