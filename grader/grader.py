import os

WINDOWS = True

def ex(cmd):
	if WINDOWS:
		cmd = cmd.replace("/", "\\")
	os.system(cmd)

SOLUTION_FILE = "main.cpp"
PROBLEM_CODE = "tower"

TEMP_FILE = "tmp.txt"
OUT_FILE = "main.exe" if WINDOWS else "./main.exe"

# clean up
ex("rm -rf %s %s" % (TEMP_FILE, OUT_FILE))

# compile
ex("g++ -std=c++11 -O2 -o %s %s" % (OUT_FILE, SOLUTION_FILE))

def eval_testcase(infile, outfile):
	print(" Evaluating testcase")
	print(" \"%s\" < %s > %s" % (OUT_FILE, infile, TEMP_FILE))
	ex("%s < %s > %s" % (OUT_FILE, infile, TEMP_FILE))
	with open(outfile) as f:
		solution_output = f.read()
	with open(TEMP_FILE) as f:
		your_output = f.read()
	ok = solution_output == your_output
	print(" AC" if ok else " WA")
	return ok

def eval_subtask(input_files):
	print("Evaluating subtask")
	results = [eval_testcase(f % "input", f % "output") for f in input_files]
	return [False for r in results if r == False] == []

# cancer interactive
if PROBLEM_CODE == "tower":
	inputs = ["../testcases/tower/input.%02d" % i for i in range(1, 11)]
	outputs = ["../testcases/tower/output.%02d" % i for i in range(1, 11)]
	for i in range(0, 10):
		ex("%s < %s > %s" % (OUT_FILE, inputs[i], TEMP_FILE))
		ex("\"../testcases/checker.py\" %s %s %s" % (inputs[i], outputs[i], TEMP_FILE))
# normal problems
else:
	# test problem
	if PROBLEM_CODE == "rack":
		subtasks = [["../testcases/rack/%s.test_0%d_0%d" % ("%s", i, j) for j in range(1,6)] for i in range(1, 4)]
		points = [20, 20, 60]

	for i, (p, files) in enumerate(zip(points,subtasks)):
		if eval_subtask(files):
			print("You solved subtask %d for %d points" % (i+1, p))
		else:
			print("You failed subtask %d for 0 points" % (i+1))
