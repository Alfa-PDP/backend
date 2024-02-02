create_network:
	@docker network create alfa-bank-pdp-backend-network 2>/dev/null || echo "alfa-bank-pdp-backend-network is up-to-date"

create_test_network:
	@docker network create test-alfa-bank-pdp-backend-network 2>/dev/null || echo "test-alfa-bank-pdp-backend-network is up-to-date"

.PHONY: up
up: create_network ## up services
	@docker-compose -f infra/docker-compose.local.yaml -f infra/docker-compose.override.yaml up --build
.PHONY: logs
logs: ## tail logs services
	@docker-compose -f infra/docker-compose.local.yaml -f infra/docker-compose.override.yaml logs -n 1000 -f

.PHONY: down
down: ## down services
	@docker-compose -f infra/docker-compose.local.yaml -f infra/docker-compose.override.yaml down

.PHONY: uninstall
uninstall: ## uninstall all services
	@docker-compose -f infra/docker-compose.local.yaml -f infra/docker-compose.override.yaml --remove-orphans --volumes

.PHONY: run-tests
run-tests: create_test_network ## run and uninstall tests
	@docker-compose -p test-alfa-bank-pdp-backend-api -f infra/docker-compose.test.yaml down --remove-orphans --volumes
	@docker-compose -p test-alfa-bank-pdp-backend-api -f infra/docker-compose.test.yaml up --build --abort-on-container-exit

.PHONY: create-test-data
create-test-data:
	@python3 -m src.testdata.main


.PHONY: help
help: ## help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
