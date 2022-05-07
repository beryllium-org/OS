x = ljinux.farland.public[2] - 1
top_l = None
top_r = None
bot_l = None
bot_r = None
y = 0
dx = 1
dy = 1
err = dx - (ljinux.farland.public[2] << 1)
while x >= y:
    ljinux.farland.oled.pixel(ljinux.farland.public[0] + x, ljinux.farland.public[1] + y, ljinux.farland.public[3])
    ljinux.farland.oled.pixel(ljinux.farland.public[0] + y, ljinux.farland.public[1] + x, ljinux.farland.public[3])
    ljinux.farland.oled.pixel(ljinux.farland.public[0] - y, ljinux.farland.public[1] + x, ljinux.farland.public[3])
    ljinux.farland.oled.pixel(ljinux.farland.public[0] - x, ljinux.farland.public[1] + y, ljinux.farland.public[3])
    ljinux.farland.oled.pixel(ljinux.farland.public[0] - x, ljinux.farland.public[1] - y, ljinux.farland.public[3])
    ljinux.farland.oled.pixel(ljinux.farland.public[0] - y, ljinux.farland.public[1] - x, ljinux.farland.public[3])
    ljinux.farland.oled.pixel(ljinux.farland.public[0] + y, ljinux.farland.public[1] - x, ljinux.farland.public[3])
    ljinux.farland.oled.pixel(ljinux.farland.public[0] + x, ljinux.farland.public[1] - y, ljinux.farland.public[3])
    if err <= 0:
        y += 1
        err += dy
        dy += 2
    if err > 0:
        x -= 1
        dx += 2
        err += dx - (ljinux.farland.public[2] << 1)
del x, y, top_l, top_r, bot_l, bot_r, err
ljinux.farland.public = []
