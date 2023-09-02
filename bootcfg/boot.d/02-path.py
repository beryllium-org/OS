# Add /lib to path
from sys import path as syspath

syspath.append("/LjinuxRoot/lib")
del syspath
systemprints(1, "System path updated")
