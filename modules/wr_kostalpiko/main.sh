#!/bin/bash

#Auslesen eines Kostal Piko WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung.
. /var/www/html/openWB/openwb.conf

pvwatttmp=$(curl --connect-timeout 5 -s $wrkostalpikoip/api/dxs.json?dxsEntries=67109120'&'dxsEntries=251658753)

#aktuelle Ausgangsleistung am WR [W]
pvwatt=$(echo $pvwatttmp | jq '.dxsEntries[0].value' | sed 's/\..*$//')

if (( $pvwatt > 5 )); then
 pvwatt=$(echo "$pvwatt*-1" |bc)
fi   

echo $pvwatt

#zur weiteren verwendung im webinterface
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt

#Gesamtzählerstand am WR [kWh]
pvkwh=$(echo $pvwatttmp | jq '.dxsEntries[1].value' | sed 's/\..*$//')
#zur weiteren verwendung im webinterface
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh