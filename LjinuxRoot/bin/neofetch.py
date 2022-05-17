global uptimee

neofetch_time = int(uptimee + time.monotonic())

uptimestr = ""

hours = neofetch_time // 3600  # Take out the hours
neofetch_time -= hours * 3600
minutes = neofetch_time // 60  # Take out the minutes
neofetch_time -= minutes * 60

if hours > 0:
    uptimestr += str(hours) + " hours, "
if minutes > 0:
    uptimestr += str(minutes) + " minutes, "
if neofetch_time > 0:
    uptimestr += str(neofetch_time) + " seconds"
else:
    uptimestr = uptimestr[:-2]
del hours, minutes, neofetch_time

Ccpu = f"{platform} ({len(cpus)}) @ {trunc(cpu.frequency / 1000000)}Mhz"

gc.collect()
gc.collect()

Rram = f"{trunc(abs(configg['mem'] - gc.mem_free() / 1000))}KiB / {str(configg['mem'])}KiB"

print(
    f"""{colors.green_t}  ,----,{colors.endc}                     {colors.cyan_t}{ljinux.based.system_vars["USER"]}@{ljinux.based.system_vars["HOSTNAME"]} {colors.endc}
{colors.green_t}  ,----.|{colors.endc}      {colors.magenta_t},----._    {colors.endc}  ---------
{colors.green_t}  |LLL|l:{colors.endc}     {colors.magenta_t}.-- -.'j\   {colors.endc}  \033[31mOS{colors.endc}: \033[33mLjinux {ljinux.based.system_vars["VERSION"]}{colors.endc}
{colors.green_t}  :LLL:l|{colors.endc}     {colors.magenta_t}|JJJJ|jjj:  {colors.endc}  \033[31mHost{colors.endc}: {ljinux.based.system_vars["BOARD"]}  
{colors.green_t}  |LLL'l:{colors.endc}     {colors.magenta_t}:JJJJ;jjj|  {colors.endc}  \033[31mCircuitPython{colors.endc}: {ljinux.based.system_vars["IMPLEMENTATION"]}
{colors.green_t}  ;LLL;l'{colors.endc}     {colors.magenta_t}:JJJJ|jjj|  {colors.endc}  \033[31mUptime{colors.endc}: {uptimestr}
{colors.green_t}  'LLL|l|{colors.endc}     {colors.magenta_t}|JJJJ:jjj:  {colors.endc}  \033[31mPackages{colors.endc}: 0 ()
{colors.green_t}  |LLL|l|{colors.endc}     {colors.magenta_t}:JJJJ|jjj:  {colors.endc}  \033[31mShell{colors.endc}: \033[35mBased{colors.endc}
{colors.green_t}  'LLL:l;_____{colors.endc}{colors.magenta_t}|JJJJ;jjj|  {colors.endc}  \033[31mWM{colors.endc}: Farland
{colors.green_t}  |LLL|;.____{colors.endc}{colors.magenta_t};lJJJJ|jjj|  {colors.endc}  \033[31mTerminal{colors.endc}: TTYACM0
{colors.green_t}  ;LLL:{colors.endc} {colors.magenta_t}/JJJJ/\JJJJ/jjj:  {colors.endc}  \033[31mCPU{colors.endc}: {Ccpu}
{colors.green_t}  |LLL,{colors.endc}{colors.magenta_t}/JJ../jj`..-jjjj,  {colors.endc}  \033[31mMemory{colors.endc}: {Rram}
{colors.green_t}   ---'{colors.endc}{colors.magenta_t}\JJJJ\jjjjjjjjj;   {colors.endc}
{colors.green_t}        {colors.endc}{colors.magenta_t}\JJJJ\jjjjjj,'    {colors.endc}  {colors.black_t}███{colors.endc}{colors.red_t}███{colors.endc}{colors.green_t}███{colors.endc}{colors.yellow_t}███{colors.endc}{colors.blue_t}███{colors.endc}{colors.magenta_t}███{colors.endc}{colors.cyan_t}███{colors.endc}{colors.white_t}███{colors.endc}
{colors.magenta_t}         "---....--'      {colors.endc}  {colors.black_t}███{colors.endc}{colors.red_t}███{colors.endc}{colors.green_t}███{colors.endc}{colors.yellow_t}███{colors.endc}{colors.blue_t}███{colors.endc}{colors.magenta_t}███{colors.endc}{colors.cyan_t}███{colors.endc}{colors.white_t}███{colors.endc}
"""
)

del Rram, Ccpu
del uptimestr
