#/bin/bash
for file in *.html;do
	tmp=`awk -F'=' '/name="description"/ {print $3}' $file`
	tmp=${tmp%????}
	tmp=${tmp:1}
	#removed formatting chars
	imid=${file%?????}
	details=`cat $file | awk -F'"' '/ name="title"/ {print $4}'`
	name=`echo $details | awk -F'[)(]' '{print $1'}`
	year=`echo $details | awk -F'[)(]' '{print $2'}`
	director=`echo $tmp | awk -F'. With ' '{print $1}'`
	director2=`echo $director | cut -d' ' -f3-`
	cast=`echo $tmp |awk -F'. With ' '{print $2}'`
	cast2=`echo $cast | awk -F'.' '{$NF="";$(NF-1)="";print $0}'`
	rating=`cat $file | awk -F':' '/ratingValue/ {print $2; exit}'`
	echo "$imid,\"$name\",$year,\"$director2\",$rating" >> dt.txt

done
