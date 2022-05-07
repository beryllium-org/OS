ljinux.farland.public[2] -= 1
y = -ljinux.farland.public[2]
while y <= ljinux.farland.public[2]:
    x = -ljinux.farland.public[2]
    while x <= ljinux.farland.public[2]:
        if (x * 2 + y * 2) < (ljinux.farland.public[2] * ljinux.farland.public[2] + ljinux.farland.public[2] * 0.8):
            ljinux.farland.oled.pixel(ljinux.farland.public[0] + x, ljinux.farland.public[1] + y, ljinux.farland.public[3])
        x += 1
    y += 1
del x, y
