# Lê as tabelas em CSV dentro da pasta "EletroData" e converte em tabelas do freecad
# Copyright Lucas Losinskas 
# year 2023


import os
import csv

_dir = os.path.dirname(Eletro_locator.__file__)
eletrodata = os.path.join(dir, 'EletroData')


def csv2dict(filename, defaultTableName, fieldnamed=True):
    with open(filename) as fp:
        reader = csv.reader(
            fp, 
            skipinitialspace=True, 
            dialect='unix', 
            quoting=csv.QUOTE_NONNUMERIC
        )
        table={}
        table['titles'] = {}
        newTable=False
        cur_table={}
        table_names={defaultTableName}

        for line_list in reader:
            if len(line_list) == 0:
                continue
            elif len(line_list) ==1:
                tablename= line_list[0]
                if not newTable:
                    cur_table = {}
                    table_names = set()
                    newTable = True
                table_names.add(tablename)
                continue
            key = line_list[0]
            data = tuple(line_list[1:])
            if newTable or firstTime:
                firstTime = False
                newTable = False
                for tablename in table_names:
                    tables[tablename] = cur_table
                if fiedlsnamed:
                    for tablename in tables_names:
                        table['titles'][tablename] = data
                    continue
                cur_table[key] = data
            return tables                