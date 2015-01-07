all:
	cd ..; python -m compileall bingo2; find bingo2 -name *.pyc | xargs zip -m -r bingo2/bingo2.zip

clean:
	rm -f bingo2.zip
	find . -name '*.pyc' | xargs rm -f
