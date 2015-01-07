run()
{
	count=0
	for pair in ${pairs}
	do
		width=`echo $pair | cut -d',' -f1`
		height=`echo $pair | cut -d',' -f2`
		#if [ $count -eq 12 ]; then
		#	wait
		#	count=0
		#fi

		echo "training for w${width} x h${height}"
		python train_matrix_predictor.py $width $height &
		count=$(($count + 1))
	done

	wait
}

pairs=""
for width in `seq 2 5`
do
	for height in `seq 2 4`
	do
		pairs="${pairs} ${width},${height}"
	done
done

pairs="2,2 2,3 2,4 2,5 2,6 2,7"
run
pairs="3,2 3,3 3,4"
run
pairs="4,2 4,3"
run
pairs="5,2"
run
pairs="6,2"
run
pairs="7,2"
run
