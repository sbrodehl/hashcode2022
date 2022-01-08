SOLVER=lp

ifdef DEBUG
DEBUGSTR = --debug
else
DEBUGSTR =
endif

all: A B C D E

zip:
	zip -r output/submission.zip . --exclude @.exclude.lst

A: zip
	python main.py input/a_an_example.in.txt --output output/a_an_example.out.txt --solver $(SOLVER) $(DEBUGSTR)

B: zip
	python main.py input/b_basic.in.txt --output output/b_basic.out.txt --solver $(SOLVER) $(DEBUGSTR)

C: zip
	python main.py input/c_coarse.in.txt --output output/c_coarse.out.txt --solver $(SOLVER) $(DEBUGSTR)

D: zip
	python main.py input/d_difficult.in.txt --output output/d_difficult.out.txt --solver $(SOLVER) $(DEBUGSTR)

E: zip
	python main.py input/e_elaborate.in.txt --output output/e_elaborate.out.txt --solver $(SOLVER) $(DEBUGSTR)
