import mysql.connector

cnx = mysql.connector.connect(user='root', database='mothbase2', password='123(sql)')

cursor = cnx.cursor()
query = 'SELECT species_id FROM mothbase2.species WHERE species_id IN '+ \
        '(SELECT species_id FROM mothbase2.specimen WHERE sample_id in ' +\
        '(SELECT sample_id FROM mothbase2.samples WHERE month(date) = 9)) ORDER BY taxon1_id, taxon2_id, name'
# query = 'SELECT species_id FROM mothbase2.species WHERE species_id IN '+ \
#         '(SELECT  distinct species_id FROM specimen WHERE sample_id IN '+ \
#         '(SELECT sample_id FROM samples WHERE stand_id>=7 AND stand_id<=15 '+ \
#         'OR stand_id=1 '+ \
#         'OR stand_id>=23 AND stand_id<=34 '+ \
#         'OR stand_id>=52 AND stand_id<=128 '+ \
#         'OR stand_id>=154 And stand_id<=165)) ORDER BY taxon1_id, taxon2_id, name'

cursor.execute(query)
rows = cursor.fetchall()
fileName = "/Users/asya/python/PythonMySQL/septemberKerzhList.txt"
# fileName = "/Users/asya/python/PythonMySQL/kerzhList.txt"
taxon1 = 0
taxon2 = 0
number = 1
with open(fileName, 'w') as file:
    for elem in rows:
        query = 'SELECT taxon1_id,taxon2_id, name FROM species WHERE species_id= %s'
        cursor.execute(query, (elem))
        sist = cursor.fetchall()
        taxon1_id = sist[0][0]
        taxon2_id = sist[0][1]
        name = sist[0][2]
        if taxon1_id != taxon1:
            query = 'SELECT name FROM taxons1 WHERE taxon1_id= %s'
            cursor.execute(query, (taxon1_id,))
            superFamily = cursor.fetchall()
            file.write("\nSuperfamily {}".format(superFamily[0][0]))
            taxon1 = taxon1_id
        if taxon2_id != taxon2:
            query = 'SELECT name FROM taxons2 WHERE taxon2_id= %s'
            cursor.execute(query, (taxon2_id,))
            family = cursor.fetchall()
            file.write("\n    Family {}".format(family[0][0]))
            taxon2 = taxon2_id

        file.write("\n       {}. {}\n".format(number,name))
        number += 1
        query = 'SELECT stand_id FROM samples WHERE sample_id IN (SELECT sample_id FROM specimen WHERE species_id= %s)'
        cursor.execute(query, (elem))
        stands = cursor.fetchall()
        descript = set()
        for stand in stands:
            query = 'SELECT place FROM stands WHERE stand_id= %s'
            cursor.execute(query, (stand))
            place = cursor.fetchall()
            acronimBiotop = place[0][0]
            descript.add(acronimBiotop)
        for elem in descript:
            file.write(elem + '\n')
