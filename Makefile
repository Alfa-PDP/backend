create_network:
	@docker network create alfa-bank-pdp-backend-network 2>/dev/null || echo "alfa-bank-pdp-backend-network is up-to-date"

.PHONY: up
up: create_network ## up services
	@docker-compose -f infra/docker-compose.yaml up --build

.PHONY: logs
logs: ## tail logs services
	@docker-compose -f infra/docker-compose.yaml logs -n 1000 -f

.PHONY: down
down: ## down services
	@docker-compose -f infra/docker-compose.yaml down

.PHONY: uninstall
uninstall: ## uninstall all services
	@docker-compose -f infra/docker-compose.yaml down --remove-orphans --volumes

.PHONY: help
help: ## help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

