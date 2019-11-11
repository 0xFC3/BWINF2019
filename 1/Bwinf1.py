# read text document
f = open('blumen2.txt', 'r')
text = []
for line in f:
    text.append(line[:-1])

beet = [1,2,3,4,5,6,7,7,7] # defining random beet
best_beet = []
colours = {'blau': 1, 'gelb': 2, 'gruen': 3, 'orange': 4, 'rosa': 5, 'rot': 6, 'tuerkis': 7}

connections = ((1,2), (1,3), (2,3), (2,4), (2,5), (3,5), (3,6), (4,5), (4,7), (5, 6), (5,7), (5,8), (6,8), (7,8), (7,9), (8,9))

max_colours = int(text[0])

preferred = []
pre_out = []

for i in range(2, len(text)):
    c = text[i].split(' ')
    preferred.append((int(c[2]), (colours[c[0]], colours[c[1]])))
    pre_out.append((int(c[2]), c[0], c[1]))

# outputting the input
print('Der Kunde möchte ' + str(max_colours) + ' verschiedene Farben haben.')
print('Außerdem hat er folgende Lieblingskombinationen:')
[print(item) for item in pre_out]

def calc_points(beet, preferred): # method that calculates the points a beet gets
    global connections
    points = 0
    for connection in connections:
        for pref in preferred:
            if beet[connection[0] - 1] == pref[1][0] and beet[connection[1] - 1] == pref[1][1]:
                points += pref[0]
            if beet[connection[0] - 1] == pref[1][1] and beet[connection[1] - 1] == pref[1][0]:
                points += pref[0]
    return points
points = calc_points(beet, preferred)


def loop(col_count, colours_ava, colours_used, i): # recursive method
    d = colours_ava.copy()
    z = colours_used.copy()
    f = col_count
    global points, beet, preferred, best_beet, max_colours
    for e in range(len(colours_ava)):
        beet[i] = colours_ava[e]
        colours_used.add(colours_ava[e])
        dif = True
        for plant in beet[:i]:
            if colours_ava[e] == plant:
                dif = False
        if dif != False: col_count -= 1
        if max_colours == max_colours - col_count:
            colours_ava = list(colours_used).copy()
        if col_count == 8 - i:
            for plant in beet[:i + 1]:
                try:
                    del colours_ava[colours_ava.index(plant)]
                except: pass
        if i < 8:
            loop(col_count, colours_ava, colours_used, i+1)
        if i == 8:
            p = calc_points(beet, preferred)
            if p > points:
                points = p
                best_beet = beet.copy()
        colours_ava = d.copy()
        col_count = f
        colours_used = z.copy()
    return

def opt_beet(preferred): # method that controls the other methods
    global colours, beet, max_colours
    colours_ava = [1,2,3,4,5,6,7]
    col_count = max_colours
    loop(col_count, colours_ava, set([]), 0)
    return

def switch(ar, col): # method that maps colours to the numbers
    inv_map = {v: k for k, v in col.items()}
    for i in range(len(ar)):
        ar[i] = inv_map[ar[i]]
    return ar

if __name__ == '__main__':
    opt_beet(preferred)
    print('Dafür pflanze ich Zwiebeln folgendermaßen an:')
    print(best_beet)
    print(switch(best_beet, colours))
    print('Und die Punktezahl ist: ' + str(points))
