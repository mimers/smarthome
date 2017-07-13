#!/bin/bash

night_light=29

last_status=`gpio read $night_light`

while [[ 1 ]]; do
	current=`gpio read $night_light`
	if [[ $last_status == '0' && $current == '1' ]]; then
		curl "http://home.joker.li:3568/light/set/00:15:85:10:79:54?val=S1$"
	fi
	if [[ $last_status == 1 && $current == 0 ]]; then
		curl "http://home.joker.li:3568/light/set/00:15:85:10:79:54?val=S0$"
	fi
	last_status=$current
	sleep 1
done

