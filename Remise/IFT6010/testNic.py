# -*- coding: utf-8 -*-

from editDistance import *

x = "Sa srait cool de srtr"
y = "Ca serait cool de sortir."

#x = ["Sa", "srait", "cool", "de", "srtr"]
#y = ["Ça", "serait", "cool", "de", "sortir", "."]

x = ["La", "di", "stance", "devrait", "être", "cinq", "."]
y = ["La", "distance", "devrait", "être", "cinq", "."]

x = "La di stance devrait être cinq. La di stance devrait être cinq. La di stance devrait être cinq. La di stance devrait être cinq. La di stance devrait être cinq. La di stance devrait être cinq."
y = "La distance devrait être cinq. La distance devrait être cinq. La distance devrait être cinq. La distance devrait être cinq. La distance devrait être cinq. La distance devrait être cinq."


print
print editDistance(x, y)