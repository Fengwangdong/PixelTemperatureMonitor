#!/bin/env python
import sqlite3 as sql
import cx_Oracle
import datetime

connection = cx_Oracle.connect('cms_trk_r/1A3C5E7G:FIN@cms_omds_adg')
cursor = connection.cursor()

start_time = "2018-07-18 00:12:00"
stop_time = "2018-07-18 10:59:00"

options = "PixelBarrel"

query = """
with cables as (
    select distinct substr(lal.alias,INSTR(lal.alias, '/', -1, 2)+1) as cable, id, cd from
    (select max(since) as cd, alias from  cms_trk_dcs_pvss_cond.aliases group by alias) md, cms_trk_dcs_pvss_cond.aliases lal
    join cms_trk_dcs_pvss_cond.dp_name2id on dpe_name=concat(dpname,'.')
    where md.alias=lal.alias and lal.since=cd
    and (lal.alias like '""" + str("%%" + options + "%%channel002%%") + """'
    or lal.alias like '""" + str("%%" + options + "%%channel003%%") + """')
),

it as (
    select dpid, max(change_date) as itime from cms_trk_dcs_pvss_cond.fwcaenchannel
    where change_date >= to_timestamp('""" + str(start_time) + """', 'RRRR-MM-DD HH24:MI:SS.FF')
    and change_date <= to_timestamp('""" + str(stop_time) + """','RRRR-MM-DD HH24:MI:SS.FF')
    and actual_Imon is not NULL
    group by dpid
)

select cable, actual_Imon, change_date from cms_trk_dcs_pvss_cond.fwcaenchannel, cables, it
where change_date >= to_timestamp('""" + str(start_time) + """', 'RRRR-MM-DD HH24:MI:SS.FF')
and change_date <= to_timestamp('""" + str(stop_time) + """','RRRR-MM-DD HH24:MI:SS.FF')
and actual_Imon is not NULL
and cms_trk_dcs_pvss_cond.fwcaenchannel.dpid = it.dpid
and it.dpid = cables.id
and change_date = it.itime
order by cable, change_date
"""

print "executing query ..."
cursor.execute(query)
result = cursor.fetchall()
print "finish query execution!"

outputFile = "currentsFromDB.txt"
fcur = open(outputFile, "w+")

print "writing output..."

for i in xrange(len(result)):

    if ("LAY1/" in result[i][0]) or ("LAY3/" in result[i][0]):
        continue

    if "LAY14/channel002" in result[i][0]:
        dpid = result[i][0].replace("LAY14/channel002","LAY1")

    if "LAY14/channel003" in result[i][0]:
        dpid = result[i][0].replace("LAY14/channel003","LAY4")

    if "LAY23/channel002" in result[i][0]:
        dpid = result[i][0].replace("LAY23/channel002","LAY3")

    if "LAY23/channel003" in result[i][0]:
        dpid = result[i][0].replace("LAY23/channel003","LAY2")

    fcur.write(dpid + "   " + str(result[i][1]) + "   " + str(result[i][2]) + "\n")

print "finish output!"

fcur.close()
connection.close()
