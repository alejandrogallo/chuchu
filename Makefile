
CLEAN_FILES  ?=


CLEAN_FILES += \
$(shell find . -name *.pyc) \
$(wildcard test_* ) \



dev-install-local:
	python setup.py develop --user

test:
	python setup.py test

install-local:
	python setup.py install --user

doc:
	make -C doc/ html

update-gh-pages:
	@echo "Warning: Black magic in action"
	git push origin `git subtree split --prefix doc/build/html/ master`:gh-pages --force

clean: ## Remove build and temporary files
	@echo Cleaning up...
	@{ for file in $(CLEAN_FILES); do echo "  *  $$file"; done }
	@rm -rf $(CLEAN_FILES)


help: ## Prints help for targets with comments
	@$(or $(AWK),awk) ' \
		BEGIN {FS = ":.*?## "}; \
		/^## *<<HELP/,/^## *HELP/ { \
			help=$$1; \
			gsub("#","",help); \
			if (! match(help, "HELP")) \
				print help ; \
		}; \
		/^[a-zA-Z0-9_\-.]+:.*?## .*$$/{ \
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$2 ; \
		};' \
		$(MAKEFILE_LIST)

