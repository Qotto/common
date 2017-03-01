help:
	@echo "make requirements    - Updates requirements files"

requirements:
	# it's a hack for installing python modules from git submodules
	pip freeze|sed -e 's#.*/\([a-z]*\)\.git@.*#-e \1#' > requirements.txt
