if ljinux.farland.public[5] == "border":
    if ljinux.farland.public[0] < ljinux.farland.public[2]:
        for i in range(ljinux.farland.public[0], ljinux.farland.public[2]):
            ljinux.farland.oled.pixel(i, ljinux.farland.public[1], ljinux.farland.public[4])
            ljinux.farland.oled.pixel(i, ljinux.farland.public[3], ljinux.farland.public[4])
    else:
        for i in range(ljinux.farland.public[2], ljinux.farland.public[0]):
            ljinux.farland.oled.pixel(i, ljinux.farland.public[1], ljinux.farland.public[4])
            ljinux.farland.oled.pixel(i, ljinux.farland.public[3], ljinux.farland.public[4])
    if ljinux.farland.public[1] < ljinux.farland.public[3]:
        for i in range(ljinux.farland.public[1], ljinux.farland.public[3]):
            ljinux.farland.oled.pixel(ljinux.farland.public[0], i, ljinux.farland.public[4])
            ljinux.farland.oled.pixel(ljinux.farland.public[2], i, ljinux.farland.public[4])
    else:
        for i in range(ljinux.farland.public[2], ljinux.farland.public[0]):
            ljinux.farland.oled.pixel(ljinux.farland.public[0], i, ljinux.farland.public[4])
            ljinux.farland.oled.pixel(ljinux.farland.public[2], i, ljinux.farland.public[4])
elif ljinux.farland.public[5] == "fill":
    if (ljinux.farland.public[0] < ljinux.farland.public[2]) and (ljinux.farland.public[1] < ljinux.farland.public[3]):
        for i in range(ljinux.farland.public[0], ljinux.farland.public[2]):
            for j in range(ljinux.farland.public[1], ljinux.farland.public[3]):
                ljinux.farland.oled.pixel(i, j, ljinux.farland.public[4])
    elif (ljinux.farland.public[0] < ljinux.farland.public[2]) and (ljinux.farland.public[3] > ljinux.farland.public[1]):
        for i in range(ljinux.farland.public[0], ljinux.farland.public[2]):
            for j in range(ljinux.farland.public[1], ljinux.farland.public[3], -1):
                ljinux.farland.oled.pixel(i, j, ljinux.farland.public[4])
    elif (ljinux.farland.public[0] > ljinux.farland.public[2]) and (ljinux.farland.public[3] < ljinux.farland.public[1]):
        for i in range(ljinux.farland.public[0], ljinux.farland.public[2], -1):
            for j in range(ljinux.farland.public[1], ljinux.farland.public[3]):
                ljinux.farland.oled.pixel(i, j, ljinux.farland.public[4])
    elif (ljinux.farland.public[0] > ljinux.farland.public[2]) and (ljinux.farland.public[3] > ljinux.farland.public[1]):
        for i in range(ljinux.farland.public[0], ljinux.farland.public[2], -1):
            for j in range(ljinux.farland.public[1], ljinux.farland.public[3], -1):
                ljinux.farland.oled.pixel(i, j, ljinux.farland.public[4])
    else:
        ljinux.based.error(1)
