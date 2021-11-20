for i in *.txt
do
	sed -i '' -e 's/NNN/______/' -e 's/xnn/___/' $i
done

