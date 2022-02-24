SOLVER=greedy

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
	python main.py input/b_better_start_small.in.txt --output output/b_better_start_small.out.txt --solver $(SOLVER) $(DEBUGSTR)

C: zip
	python main.py input/c_collaboration.in.txt --output output/c_collaboration.out.txt --solver $(SOLVER) $(DEBUGSTR)

D: zip
	python main.py input/d_dense_schedule.in.txt --output output/d_dense_schedule.out.txt --solver $(SOLVER) $(DEBUGSTR)

E: zip
	python main.py input/e_exceptional_skills.in.txt --output output/e_exceptional_skills.out.txt --solver $(SOLVER) $(DEBUGSTR)

F: zip
	python main.py input/f_find_great_mentors.in.txt --output output/f_find_great_mentors.out.txt --solver $(SOLVER) $(DEBUGSTR)

