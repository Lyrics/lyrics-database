.PHONY: all run clean

all: testsuite run

testsuite:
	autom4te --language=autotest -o testsuite testsuite.at

run:
	./testsuite ROOT_DIR=${PWD}/../database/

clean:
	rm -rf testsuite testsuite.log testsuite.dir
