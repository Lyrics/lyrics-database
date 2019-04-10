.PHONY: all run clean

all: clean database-tests run

database-tests:
	@autom4te --language=autotest -o database-tests database-tests.at

run:
	@./database-tests ROOT_DIR=${PWD}/../database

clean:
	@rm -rf database-tests database-tests.log database-tests.dir
