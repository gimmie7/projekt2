import itertools

# [Name, P, S, Q, I]

# TODO bis 18.5.2018
# install pip more-itertools
# Restliche Geräte messen
# Skript schreiben um Median zu berechnen
# Einzelne Geräte in CSV erfassen mit folgender Struktur: 'Gerätename', Median(P), Median(S), Median(Q), Median(I)
# Geräte: Wasserkocher, Toaster, Haarfön, Stabmixer, Heizlüfter, Ventilator
# Messung auslösen: "welche Geräte sind jetzt gerade angeschlossen". Z.B. in start.py
# Bei jeder Messung Geräte aus csv einlesen, Kombinationen erstellen und die am nächsten liegende Kombination ausgeben, siehe Code unten
# Alle Geräte am Schluss sortiert ausgeben

devices = [
        ['Toaster', 740, 740, 0, 3.3],
        ['Wasserkocher', 1860, 1860, 0, 8.2],
        ['Heizlüfter', 1150, 1151, 15, 5]
]

total = ['Total', 3600, 3700, 15, 16]

device = [] # the nearest combination
val = 10000000 # the nearest value to total

for l in range(1, len(devices) + 1):
    for x in itertools.combinations(devices, l):
        p = s = q = i = 0
        print(x)
        for y in x:
            p = p + y[1]
            s = s + y[2]
            q = q + y[3]
            i = i + y[4]
        print('P={}, S={}, Q={}, I={}'.format(p,s,q,i))

        total_x = abs(total[1]-p) + abs(total[2]-s) + abs(total[3]-q) + abs(total[4]-i)
        if total_x < val:
            device = x
            val = total_x
        #print(x)
        #print(sum)
# return res
print(device)
print(val)
# print(res)