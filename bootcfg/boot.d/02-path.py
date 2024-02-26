# Add /lib to path
from sys import path as syspath

syspath.append("/" + pv[0]["root"] + "/lib")
del syspath
systemprints(1, "System path updated")
