#!/bin/bash

night_light=29

last_status=`gpio read $night_light`

while [[ 1 ]]; do
	if [[ $last_status == '0' && `gpio read $night_light` == '1' ]]; then
		curl "http://home.joker.li:3568/light/set/00:15:85:10:79:54?val=S1$"
	fi
	sleep 1
done

