import copy # allows to deeocopy a array
# read text document
f = open('2.txt', 'r')
text = []
for line in f:
    text.append(line[:-1])

## import all the data from the textfile
cons = int(text[0])
tsize = int(text[1])
fill = int(text[2])
distance = int(text[3])
dis = distance
gas_stations = []
route = []
beste_route = []
## add all the gas stations
for i in range(5, len(text)):
    b = text[i].split(' ')
    gas_stations.append([float(b[0]), float(b[-1])])

stations = copy.deepcopy(gas_stations)

def calc_range(cons, fill): ## calculates the range the car will drive with certain amount of fuel and consumption
    return fill / cons * 100

def calc_fuel(cons, dis): ## calculates the amount of fuel needed to get to a certain point
    return cons/ 100 * dis

def check_destination_in_range(cons, fill, distance): ## checks if destination is in range with the fuel that is in the car
    return True if calc_range(cons, fill) >= distance else False

def stations_in_range(cons, fill, gas_stations): ## return the gas stations in range
    dis = calc_range(cons, fill)
    return [station for station in gas_stations if station[0] < dis]

def fuel(gas_station, amount_of_fuel, fill, distance, gas_stations): ## does the actual fueling and and changes all the parameters
    distance -= gas_station[0]
    del gas_stations[:gas_stations.index(gas_station) + 1]
    for element in gas_stations:
        element[0] -= gas_station[0]
    fill -= calc_fuel(cons, gas_station[0]) - amount_of_fuel
    return (distance, fill, gas_stations)

def find_min_amount_of_stopping(cons, gas_stations, fill, distance): ## finds out the minimum amount of stops you have to do
    global stations, route, tsize
    stops = 0
    while check_destination_in_range(cons, fill, distance) == False:
        furthest_station = copy.deepcopy(stations_in_range(cons,fill, gas_stations)[-1])
        amount_of_fuel = tsize - (fill - calc_fuel(cons, furthest_station[0]))
        stops += 1
        distance, fill, gas_stations = fuel(furthest_station, amount_of_fuel, fill, distance, gas_stations)
        route.append([amount_of_fuel, stations[len(stations) - len(gas_stations) - 1]])
    return stops

def opt_money_spent(route, cons, dis, fill): ## function that optimizes the money you spent fueling up
    global tsize
    am = float(fill)
    route.append(0.0)
    for i in range(len(route) -1):
        if i == 0:
            am -= calc_fuel(cons, route[i][1][0])
        else:
            am -= calc_fuel(cons, route[i][1][0] - route[i - 1][1][0])
        if i == len(route) -2:
            route[i][0] = calc_fuel(cons, dis - route[i][1][0]) - am
            route[len(route) -1] += route[i][0] * route[i][1][1]
        else:
            if route[i][1][1] < route[i + 1][1][1]:
                #if the first gas station is cheaper, make the tank full
                route[i][0] = tsize - am
                am = tsize
            else:
                route[i][0] = calc_fuel(cons, route[i + 1][1][0] - route[i][1][0]) - am
                am += route[i][0]
            route[len(route) - 1] += route[i][0] * route[i][1][1]
    return route

def loop(gas_stations, r, fill, cons, tsize, distance, min_stops, b_fill, b_dis): ## brute force function
    c1 = copy.deepcopy(gas_stations)
    c2, c3, c4 = (r, fill, distance)
    global route, stations, beste_route
    for i in range(len(stations_in_range(cons,fill, gas_stations))):
        station = copy.deepcopy(gas_stations[i])
        route[r][1] = stations[len(stations) - len(gas_stations) + i]
        fuel_amount = tsize - (fill - station[0] / 100 * cons)
        route[r][0] = fuel_amount
        distance, fill, gas_stations = fuel(station, fuel_amount, fill, distance, gas_stations)
        if check_destination_in_range(cons, fill, distance) == True:
            new_route = copy.deepcopy(opt_money_spent(copy.deepcopy(route), cons, b_dis, b_fill))
            if beste_route == []:
                beste_route = copy.deepcopy(new_route)
            elif new_route[-1] < beste_route[-1]:
                beste_route = copy.deepcopy(new_route)
            gas_stations = copy.deepcopy(c1)
            r, fill, distance = (c2, c3, c4)
            continue
        elif r == min_stops -1 and min_stops != 1:
            gas_stations = copy.deepcopy(c1)
            r, fill, distance = (c2, c3, c4)
            continue
        elif distance / calc_range(cons, tsize) > min_stops - r and min_stops != 1:
            gas_stations = copy.deepcopy(c1)
            r, fill, distance = (c2, c3, c4)
            continue
        elif min_stops != 1:
            loop(gas_stations, r+1, fill, cons, tsize, distance, min_stops, b_fill, b_dis)
        gas_stations = copy.deepcopy(c1)
        r, fill, distance = (c2, c3, c4)
    return

def find_best_route(cons, gas_stations, fill, tsize, distance): ## manages all the function and calls them at the right time
    global route, beste_route, stations
    min_stops = find_min_amount_of_stopping(cons, gas_stations, fill, distance)
    gas_stations = copy.deepcopy(stations)
    loop(gas_stations, 0, fill, cons, tsize, distance, min_stops, fill, distance)
    return beste_route

if __name__ == '__main__':
    beste_route = find_best_route(cons, gas_stations, fill, tsize, distance)
    print(beste_route)

