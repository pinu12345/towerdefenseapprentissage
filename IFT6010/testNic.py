# -*- coding: utf-8 -*-

from editDistance import *

x = "Sa srait cool de srtr"
y = "Ca serait cool de sortir."

#x = ["Sa", "srait", "cool", "de", "srtr"]
#y = ["�a", "serait", "cool", "de", "sortir", "."]

x = ["La", "di", "stance", "devrait", "�tre", "cinq", "."]
y = ["La", "distance", "devrait", "�tre", "cinq", "."]

x = "La di stance devrait �tre cinq. La di stance devrait �tre cinq. La di stance devrait �tre cinq. La di stance devrait �tre cinq. La di stance devrait �tre cinq. La di stance devrait �tre cinq."
y = "La distance devrait �tre cinq. La distance devrait �tre cinq. La distance devrait �tre cinq. La distance devrait �tre cinq. La distance devrait �tre cinq. La distance devrait �tre cinq."


print
print editDistance(x, y)