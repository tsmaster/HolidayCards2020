import csv

import makeCard
import drawback

with open("addresses.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter='\t')
    for rowNum, row in enumerate(tsvreader):
        print(rowNum, row)
        name = row[0]
        addr1 = row[1]
        addr2 = row[2]
        city = row[3]
        state = row[4]
        zipcode = row[5]
        country = row[6]
        seed = row[7].upper()

        nameParts = name.split()
        firstPart = nameParts[0][:3]
        lastPart = nameParts[-1][:3]
        shortName = firstPart.lower()+lastPart

        print (shortName)
        print (name)
        print (seed)
        cityLine = city + ", " + state + " " + zipcode
        if addr2:
            lines = [name.upper(),
                     addr1.upper(),
                     addr2.upper(),
                     cityLine.upper()]
        else:
            lines = [name.upper(),
                     addr1.upper(),
                     cityLine.upper()]

        badSeeds = ['ECHO',
                    'ULAFOL',
                    'JWMO']
        #if seed in badSeeds:
        #    continue

        makeCard.makeCard(seed, shortName)
        # TODO make fronts
        drawback.makeCard(lines, shortName+"_bk", seed)
                     
