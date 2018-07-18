#!/bin/env python
import sqlite3 as sql
import cx_Oracle

connection = cx_Oracle.connect('cms_trk_r/1A3C5E7G:FIN@cms_omds_adg')
cursor = connection.cursor()

#start_time = "2018-07-09 21:15:00"
#stop_time = "2018-07-10 06:00:00"

start_time = "2018-07-18 00:43:39"
stop_time = "2018-07-18 10:59:00"

option = "PixelBarrel"

query = """
    with IDs as ( select id, substr(alias,instr(alias,'/',-1)+1) as part from CMS_TRK_DCS_PVSS_COND.aliases, CMS_TRK_DCS_PVSS_COND.dp_name2id
    where (substr(alias,instr(alias,'/',-1)+1) like '""" + str(option + "%%" + "PF") + """'
    or substr(alias,instr(alias,'/',-1)+1) like '""" + str(option + "%%" + "PN") + """'
    or substr(alias,instr(alias,'/',-1)+1) like '""" + str(option + "%%" + "MF") + """'
    or substr(alias,instr(alias,'/',-1)+1) like '""" + str(option + "%%" + "MN") + """')
    and rtrim(CMS_TRK_DCS_PVSS_COND.aliases.dpe_name,'.') = CMS_TRK_DCS_PVSS_COND.dp_name2id.dpname)
    select part, value_converted, change_date from CMS_TRK_DCS_PVSS_COND.tkplcreadsensor, IDs where IDs.id = CMS_TRK_DCS_PVSS_COND.tkplcreadsensor.DPID and CMS_TRK_DCS_PVSS_COND.tkplcreadsensor.change_date >= to_timestamp('""" + str(start_time) + """', 'RRRR-MM-DD HH24:MI:SS.FF') AND CMS_TRK_DCS_PVSS_COND.tkplcreadsensor.change_date < to_timestamp('""" + str(stop_time) + """', 'RRRR-MM-DD HH24:MI:SS.FF') order by part, CMS_TRK_DCS_PVSS_COND.tkplcreadsensor.change_date
"""

print "start executing query ..."
cursor.execute(query)
result = cursor.fetchall()
print "finish query execution!"

outputFile = "temperatureFromDB.txt"
fcur = open(outputFile, "w+")

print "writing output..."


for i in xrange(len(result)):

    alias = result[i][0]

    alias = alias.replace("PixelBarrel", "BPix")

    fcur.write(alias + "   " + str(result[i][1]) + "   " + str(result[i][2]) + "\n")

print "finish output!"

fcur.close()
connection.close()
