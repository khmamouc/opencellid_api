SHELL := /usr/bin/env bash

.DEFAULT_GOAL := help

##
## Useful commands
## -----
##

.PHONY: help
help: ## Makefile help
	 @egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:	## Build and run project with compose
	 docker-compose up -d --build

.PHONY: up
up:	## Run project with compose
	 docker-compose up --remove-orphans

.PHONY: clean
clean: ## Clean Reset project containers and volumes with compose
	 docker-compose down -v --remove-orphans | true
	 docker-compose rm -f | true
	 docker volume rm opencellid_db | true

.PHONY: test
test:	## Run project tests
	 docker-compose -f docker-compose.yml -f docker-compose.test.yml exec db sh -c " \
		pg_restore --jobs 4 --if-exists --verbose --clean --no-acl -U cell_user -d test_db -Fc docker-entrypoint-initdb.d/testdb.dump"
	 docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm web pytest

.PHONY: format
format:  ## Format project code.
	 docker-compose run --rm web isort app tests scripts
	 docker-compose run --rm web black app tests scripts

.PHONY: check_lint
check_lint:  ## Check lint
	 docker-compose run --rm web mypy --strict app tests
	 docker-compose run --rm web flakehell lint app tests

.PHONY: feed_db
feed_db: ## insert data in the principal
	 docker-compose run --rm web python scripts/feed_db.py --csv_file "data/270.csv"
	# docker-compose run --rm web python scripts/feed_db.py --csv_file "data/208.csv"