SOLVER=example

ifdef DEBUG
DEBUGSTR = --debug
else
DEBUGSTR =
endif

all: example

zip:
	zip -r output/submission.zip . --exclude @.exclude.lst

example: zip
	python main.py input/a_example.in --output output/a_example.out --solver $(SOLVER) $(DEBUGSTR)
