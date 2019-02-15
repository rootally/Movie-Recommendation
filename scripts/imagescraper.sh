#!/bin/bash
while read -r line;do
	wget "https://www.imdb.com/title/tt$line" -O $line
	img_url=`cat "$line" | grep 'image_src' | awk '{print $3}' | cut -c 7- | rev | cut -c 3- | rev`
	wget $img_url -O $line.jpg
	mv $line webpages
done < titles.csv	
