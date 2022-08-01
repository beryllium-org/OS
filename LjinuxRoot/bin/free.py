length = len(ljinux.based.user_vars["argj"])

if length < 1:
    flag = '-b'
else:
    flag = ljinux.based.user_vars["argj"].split()[1]

calc_cond = {
    """
        !IMPORTANT
            num: int MUST BE IN MEGABYTES
    
        -b : Unit Bytes
        -k : Kilobytes
        -m : Megabytes
        -g : Gigabytes
    """
    '-b': lambda num: num * (1024 ** 2),
    '-k': lambda num: num * 1024,
    '-m': lambda num: num / 1024,
    '-g': lambda num: num / (1024 ** 2)
}

total = calc_cond[flag](configg['mem'])
used = calc_cond[flag](gc.mem_free())
free = total - used

shared = None
buffers = None
cached = None

# Docs: print(f"{left_alignment : <20}{center_alignment : ^15}{right_alignment : >20}")

print(f"{' ' : <10}{'total' : <10}{'used' : ^10}{'free' : ^10}{'shared' : >5}{'buffers' : >5}{'cached' : >5}")

print(f"{'Mem' : <10}{total : <10}{used : ^10}{free : ^10}{shared : >5}{buffers : >5}{cached : >5}")

print(f"{'Swap' : <10}{'None' : <10}{'None' : ^10}{'None' : ^10}{'None' : >5}{'None' : >5}{'None' : >5}")

del flag, calc_cond, total, used, free, buffers, cached
