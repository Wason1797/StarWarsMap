

route_name = 'Rimma Trade Route'

raw_planets = "Abregado-rae[1] - Dentaal[1] - Giju[1] - Ghorman[1] - Vanik[1] - Thyferra[1] - Tauber[1] - Yag'Dhul[1] - Sukkult[1] - Wroona[1] - " +\
    "Tregillis[1] - Vandelhelm[1] - Woostri[1] - Daemen[1] - Alakatha[1] - Lanthe[1] - Vondarc[1] - Medth[1] - Tshindral III[1] - Sullust[1] - Eriadu[1] - " +\
    "Clak'dor VII[1] - Triton[1] - Praesitlyn/Sluis Van[1] - Denab[1] - Tarabba Prime[1] - Adarlon[1] - Karideph[1]"

planets = [planet.strip('[1]') for planet in raw_planets.split(' - ')]

print(planets)

# junctions = []
