.PHONY: test validate validate-openai

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate_suite.py

validate-openai:
	test -n "$(SKILL_VALIDATOR)" && test -f "$(SKILL_VALIDATOR)"
	test -n "$(PLUGIN_VALIDATOR)" && test -f "$(PLUGIN_VALIDATOR)"
	for skill in skills/*; do python3 "$(SKILL_VALIDATOR)" "$$skill"; done
	python3 "$(PLUGIN_VALIDATOR)" .
