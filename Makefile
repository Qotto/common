help:
	@echo "make requirements    - Updates requirements files"

requirements:
	pip freeze > requirements.txt
