.DEFAULT_GOAL := help

help: ## ⁉️ - Display help comments for each make command
	@grep -E '^[0-9a-zA-Z_-]+:.*? .*$$'  \
		$(MAKEFILE_LIST)  \
		| awk 'BEGIN { FS=":.*?## " }; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'  \
		| sort

clean:  ## 🧹 Clean up the project
	python3 setup.py clean --all
	rm -rf dist

dist:  ## 🔨 Create tar.gz and wheel files for pypi	python3 setup.py clean --all
	python3 setup.py sdist
	python3 setup.py bdist_wheel

pypi:  ## 📦 Upload package to PyPi
	twine upload --repository wagtail-hallo dist/*

lint-server:  ## Lint the server code with flakes8
	flake8 wagtail_hallo

lint-client:  ## Lint the client code with eslint
	npm run lint

lint: lint-server lint-client

format-server:  ## Format the server code with black
	black wagtail_hallo

format-client:  ## Format the client code with prettier
	npm run format

format: format-server format-client

test-server:  ## Run the Python tests
	python testmanage.py test

test-client:  ## Run the JavaScript tests
	npm run test

test: test-server test-client