.PHONY: all run

all: testsuite run

testsuite:
	autom4te --language=autotest -o testsuite testsuite.at

run:
	./testsuite ROOT_DIR=$(pwd)/../database

clean:
	rm -f ./testsuite
