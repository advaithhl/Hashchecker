# Usage:
# make			# Build source and wheel into 'dist' directory
# make clean	# Remove built wheel and source

all: sdist bdist
	@printf "\n+ Build succeeded!\n"

sdist:
	python3 setup.py sdist

bdist:
	python3 setup.py bdist_wheel

clean:
	rm -rf build dist hashchecker.egg-info
