a = """
from ulab.numpy import fft, ndarray, floor
from random import seed, random
from time import monotonic_ns, sleep, localtime
from math import fabs, exp
from gc import mem_free

lctoffset = localtime().tm_sec
dvm = 1000000000000 + mem_free()
p1 = fft.fft(ndarray([exp(lctoffset), monotonic_ns()]))[0]
a = fabs(float((p1[0] - p1[1]) / dvm) + (mem_free()/(dvm/1000)))
del p1
while a > 1:
    a /= 10
for i in range(0, 3):
    sleep(float("0." + str(int(str("%.10f" % a)[-i:][0]))))
p2 = fft.fft(ndarray([(a - dvm + int(str("%.10f" % a).replace('.',''))), (monotonic_ns() + lctoffset + dvm)]))[0]
del lctoffset
del a
b = fabs((p2[1] - p2[0]) / dvm)
b = int(str("%.10f" % b).replace('.',''))
seed(b)
del b
del dvm
del p2
rett = random()
"""
rett = 1
exec(a, locals())
print(str(rett))
