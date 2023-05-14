ljinux.api.setvar("output")
x = 0
y = 0

for i in ljinux.based.user_vars["input"]:
    if len(i) > x:
        x = len(i)
    del i
y = len(ljinux.based.user_vars["input"])

# Prepare the string array
ljinux.based.user_vars["output"] = [[""] * x] * y

# Gather the maximum of every vertical collumn.
maxes = [0] * x
for i in range(x):
    for j in range(y):
        if ljinux.based.user_vars["input"][j][i] > maxes[i]:
            pass
        del j
    del i

del h, w
ljinux.api.setvar("input")
