SHELL := /bin/bash

.PHONY: help test validate
help:
	@echo "Targets:"
	@echo "  make test      - run basic smoke tests"
	@echo "  make validate  - check environment tools"

test:
	bash scripts/log_parse.sh --file examples/logs/nginx_access.log --top 3 || true
	bash scripts/io_check.sh --cmd "printf 'foo\n'" --expected "foo"

validate:
	bash scripts/validate_env.sh
