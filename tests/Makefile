.PHONY: all run run-mocks-fail run-mocks-pass clean

all: clean database-tests run

database-tests:
	@autom4te --language=autotest -o database-tests database-tests.at

run:
	@./database-tests ROOT_DIR=${PWD}/../database

run-mocks-pass:
	@./database-tests ROOT_DIR=${PWD}/mocks/pass/database

run-mocks-fail:
	@./database-tests ROOT_DIR=${PWD}/mocks/fail/database

clean:
	@rm -rf database-tests database-tests.log database-tests.dir
