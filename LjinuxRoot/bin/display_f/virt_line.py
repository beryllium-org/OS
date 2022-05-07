virt_l_tab = []
dx = abs(ljinux.farland.public[2] - ljinux.farland.public[0])
dy = abs(ljinux.farland.public[3] - ljinux.farland.public[1])
x, y = ljinux.farland.public[0], ljinux.farland.public[1]
sx = -1 if ljinux.farland.public[0] > ljinux.farland.public[2] else 1
sy = -1 if ljinux.farland.public[1] > ljinux.farland.public[3] else 1
if dx > dy:
    err = dx / 2.0
    while x != ljinux.farland.public[2]:
        virt_l_tab.append([int(x), int(y)])
        err -= dy
        if err < 0:
            y += sy
            err += dx
        x += sx
else:
    err = dy / 2.0
    while y != ljinux.farland.public[3]:
        virt_l_tab.append([int(x), int(y)])
        err -= dx
        if err < 0:
            x += sx
            err += dy
        y += sy
    virt_l_tab.append([int(x), int(y)])
ljinux.based.user_vars["return"] = virt_l_tab
del virt_l_tab, dx, dy, x, y, sx, sy, err
