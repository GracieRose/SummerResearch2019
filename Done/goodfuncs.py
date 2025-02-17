import sys
import csv
from success_by_problem import success_only
from simplified_programs import simp_success_only


def print_prog(program):
    for element in program:
        print element


def check_if_constant(instruction):

	is_constant = True

	instr_types = ["in", "autoconstructive", "boolean", "char", "code", "environment", "exec", "float", "genome", "gtm", "integer", "noop", "print", "return", "string", "vector", "zip"]

	for category in instr_types:
		if instruction.startswith(category):
			is_constant = False
			break

	return is_constant


def fix_strings(program):
	
	print program

	newprog = []
	stringy = False

	for item in program:
		if stringy:
			if item.endswith('"""'):
				stringy = False
			newprog[-1] = newprog[-1] + item

		elif item.startswith('"""'):
			stringy = True
			newprog.append(item)

		else:
			newprog.append(item)

	print
	print newprog

	return newprog




def get_funcs_list(organized_programs):
	"""Returns a list of all functions that may be of significance for one or more tags"""
	problems = ["all_programs", "number-io", "checksum", "collatz-numbers", "compare-string-lengths", "count-odds", "digits", "double-letters", "even-squares", "for-loop-index", "grade", "last-index-of-zero", "median", "mirror-image", "negative-to-zero", "pig-latin", "replace-space-with-newline", "scrabble-score", "small-or-large", "smallest", "string-differences", "string-lengths-backwards", "sum-of-squares", "super-anagrams", "syllables", "vector-average", "vectors-summed", "wallis-pi", "word-stats", "x-word-lines"]

	all_funcs = []

	#iterates through all problems to collect the most used functions for each category
	for prob in problems:

		if prob == "all_programs":
			programs = organized_programs[0]

		if prob == "number-io":
			programs = organized_programs[1]

		if prob == "checksum":
			programs = organized_programs[2]

		if prob == "collatz-numbers":
			programs = organized_programs[3]

		if prob == "compare-string-lengths":
			programs = organized_programs[4]

		if prob == "count-odds":
			programs = organized_programs[5]

		if prob == "digits":
			programs = organized_programs[6]

		if prob == "double-letters":
			programs = organized_programs[7]

		if prob == "even-squares":
			programs = organized_programs[8]

		if prob == "for-loop-index":
			programs = organized_programs[9]

		if prob == "grade":
			programs = organized_programs[10]

		if prob == "last-index-of-zero":
			programs = organized_programs[11]

		if prob == "median":
			programs = organized_programs[12]

		if prob == "mirror-image":
			programs = organized_programs[13]

		if prob == "negative-to-zero":
			programs = organized_programs[14]

		if prob == "pig-latin":
			programs = organized_programs[15]

		if prob == "replace-space-with-newline":
			programs = organized_programs[16]

		if prob == "scrabble-score":
			programs = organized_programs[17]

		if prob == "small-or-large":
			programs = organized_programs[18]

		if prob == "smallest":
			programs = organized_programs[19]

		if prob == "string-differences":
			programs = organized_programs[20]

		if prob == "string-lengths-backwards":
			programs = organized_programs[21]

		if prob == "sum-of-squares":
			programs = organized_programs[22]

		if prob == "super-anagrams":
			programs = organized_programs[23]

		if prob == "syllables":
			programs = organized_programs[24]

		if prob == "vector-average":
			programs = organized_programs[25]

		if prob == "vectors-summed":
			programs = organized_programs[26]

		if prob == "wallis-pi":
			programs = organized_programs[27]

		if prob == "word-stats":
			programs = organized_programs[28]

		if prob == "x-word-lines":
			programs = organized_programs[29]

		#the maximum amount of times a fxn can occur is once per program
		max_frequency = len(programs)
		freqs = {}

		#goes through each program that solved the problem
		for program in programs:

			#keeps track of if we have counted this fxn in this program yet
			this_run = []

			for func in program:
				#ACCOUNTS FOR CONSTANTS
				is_constant = check_if_constant(func)
				if (not is_constant) and not (func in this_run):
					this_run.append(func)
					if func in freqs:
						freqs[func] += 1
					else:
						freqs[func] = 1

		#if function appears more than 60% of the time, it may be of importance
		max_threshold = round(max_frequency * .6)
		if max_frequency > 0:

			#the program has this seperated structure in case we want to use the max_threshold
			for key in freqs:
				if (freqs[key] >= max_threshold):
					if not key in all_funcs:
						all_funcs.append(key)

	return all_funcs


def goodfuncs1():
	"""Calculates the frequency of each function that is returned by get_funcs_list for each tag, then
	writes that data to a CSV
	Frequency is calculated as number of programs that contain that function, not number of occurances of that function"""

	tags = {"I/O" : ["number-io", "checksum", "digits", "double-letters", "even-squares", "for-loop-index", "grade", "median", "negative-to-zero", "pig-latin", "replace-space-with-newline", "small-or-large", "smallest", "string-differences", "string-lengths-backwards", "syllables", "word-stats", "x-word-lines"],
			"arithmetic" : ["number-io", "checksum", "collatz-numbers", "count-odds", "digits", "even-squares", "for-loop-index", "replace-space-with-newline", "scrabble-score", "sum-of-squares", "syllables", "vector-average", "vectors-summed", "wallis-pi", "word-stats"],
			"comparison" : ["collatz-numbers", "compare-string-lengths", "double-letters", "grade", "last-index-of-zero", "median", "mirror-image", "negative-to-zero", "small-or-large", "smallest","string-differences", "super-anagrams"],
			"boolean" : ["compare-string-lengths", "mirror-image", "super-anagrams"],
			"string_handling" : ["checksum", "compare-string-lengths", "digits", "double-letters", "pig-latin", "replace-space-with-newline", "scrabble-score", "string-differences", "string-lengths-backwards", "super-anagrams", "syllables", "word-stats", "x-word-lines"],
			"vectors" : ["count-odds", "last-index-of-zero", "mirror-image", "negative-to-zero", "string-lengths-backwards", "vector-average", "vectors-summed"]}

	IO = []
	arithmetic = []
	comparison = []
	boolean = []
	string_handling = []
	vectors = []
	all_programs = []

	#l stands for location
	IOl = []
	arithmeticl = []
	comparisonl = []
	booleanl = []
	string_handlingl = []
	vectorsl = []
	all_programsl = []

	#keeps track of how many problems are in each category so that the averages can be calculated
	iocount = 0
	arithcount = 0
	compcount = 0
	boolcount = 0
	strcount = 0
	vectorcount = 0

	#ensures the user provides a csv file to write to
	if len(sys.argv) > 1:
	    destination = sys.argv[1]
	else:
	    print("please provide a destination file in the format <filename>.csv")
	    exit(1)

	destfile = open(destination, mode="w")
	destwriter = csv.writer(destfile)

	#a list of lists; a master list containing lists of programs broken down by problem they solve
	#organized_programs = success_only()
	organized_programs = simp_success_only()

	#I removed file from this list because no program with that tag has succeeded, providing no data
	problems = ["all_programs", "number-io", "checksum", "collatz-numbers", "compare-string-lengths", "count-odds", "digits", "double-letters", "even-squares", "for-loop-index", "grade", "last-index-of-zero", "median", "mirror-image", "negative-to-zero", "pig-latin", "replace-space-with-newline", "scrabble-score", "small-or-large", "smallest", "string-differences", "string-lengths-backwards", "sum-of-squares", "super-anagrams", "syllables", "vector-average", "vectors-summed", "wallis-pi", "word-stats", "x-word-lines"]

	#all functions that had a frequency of .6 or higher for at least one problem
	all_funcs = get_funcs_list(organized_programs)

	#gets the data for each of the above functions for each problem
	for prob in problems:

		if prob == "all_programs":
			programs = organized_programs[0]

		if prob == "number-io":
			programs = organized_programs[1]

		if prob == "checksum":
			programs = organized_programs[2]

		if prob == "collatz-numbers":
			programs = organized_programs[3]

		if prob == "compare-string-lengths":
			programs = organized_programs[4]

		if prob == "count-odds":
			programs = organized_programs[5]

		if prob == "digits":
			programs = organized_programs[6]

		if prob == "double-letters":
			programs = organized_programs[7]

		if prob == "even-squares":
			programs = organized_programs[8]

		if prob == "for-loop-index":
			programs = organized_programs[9]

		if prob == "grade":
			programs = organized_programs[10]

		if prob == "last-index-of-zero":
			programs = organized_programs[11]

		if prob == "median":
			programs = organized_programs[12]

		if prob == "mirror-image":
			programs = organized_programs[13]

		if prob == "negative-to-zero":
			programs = organized_programs[14]

		if prob == "pig-latin":
			programs = organized_programs[15]

		if prob == "replace-space-with-newline":
			programs = organized_programs[16]

		if prob == "scrabble-score":
			programs = organized_programs[17]

		if prob == "small-or-large":
			programs = organized_programs[18]

		if prob == "smallest":
			programs = organized_programs[19]

		if prob == "string-differences":
			programs = organized_programs[20]

		if prob == "string-lengths-backwards":
			programs = organized_programs[21]

		if prob == "sum-of-squares":
			programs = organized_programs[22]

		if prob == "super-anagrams":
			programs = organized_programs[23]

		if prob == "syllables":
			programs = organized_programs[24]

		if prob == "vector-average":
			programs = organized_programs[25]

		if prob == "vectors-summed":
			programs = organized_programs[26]

		if prob == "wallis-pi":
			programs = organized_programs[27]

		if prob == "word-stats":
			programs = organized_programs[28]

		if prob == "x-word-lines":
			programs = organized_programs[29]

		#maximum number of occurances is equal to the number of programs
		max_frequency = len(programs)
		freqs = {}
		locations = {}

		#calculates the number of occurances
		for program in programs:

			program = fix_strings(program)  #7/16 ******************I RECENTLY CHANGED THIS SECTION SO PLEASE DOUBLE CHECK IT WOOLSOCK

			#this length includes constants 
			prog_len = len(program)

			this_run = []

			#print_prog(program)
			for x in range(0, len(program)):

				func = program[x]

				#ACCOUNTS FOR CONSTANTS
				is_constant = check_if_constant(func)
				if (not is_constant) and not (func in this_run):
					this_run.append(func)
					if func in freqs:
						freqs[func] += 1
						locations[func].append(float(x) / prog_len)
					else:
						freqs[func] = 1
						#x = location of function in program
						locations[func] = [float(x) / prog_len]


		#only does the rest if there are any solution programs for the problem in question
		if max_frequency > 0:

			print prob
			print "Max possible occurances: %i" % max_frequency
			print

			#iterates over all functions in all_funcs
			for i in range(0, len(all_funcs)):

				function = all_funcs[i]

				#if this function doesn't occur in this problem, we must set frequency to zero
				# otherwise, it is the number of times the function occurs over the total number of programs
				if function in freqs:
					frequency = (freqs[function] / float(max_frequency))
					#print freqs[function]
					#print locations[function]
					loc = sum(locations[function]) / len(locations[function])
					#print func_loc 
					#print
				else:
					frequency = 0.0

				if prob == "all_programs":
					all_programs.append(frequency)

				#if this is the first IO problem, the the list will be empty so we simply append
				#if it isn't, then the list already contains an entry for each func so we add to each entry
				if prob in tags["I/O"]:
					if len(IO) - 1 < i:
						IO.append(frequency)
						IOl.append(loc)
					else:
						IO[i] = IO[i] + frequency
						IOl[i] = IOl[i] + loc

					if i == len(all_funcs) - 1:
						iocount += 1

				if prob in tags["arithmetic"]:
					if len(arithmetic) - 1 < i:
						arithmetic.append(frequency)
						arithmeticl.append(loc)						
					else:
						arithmetic[i] = arithmetic[i] + frequency
						arithmeticl[i] = arithmeticl[i] + loc

					if i == len(all_funcs) - 1:
						arithcount += 1

				if prob in tags["comparison"]:
					if len(comparison) - 1 < i:
						comparison.append(frequency)
						comparisonl.append(loc)
					else:
						comparison[i] = comparison[i] + frequency
						comparisonl[i] = comparisonl[i] + loc

					if i == len(all_funcs) - 1:
						compcount += 1

				if prob in tags["boolean"]:
					if len(boolean) - 1 < i:
						boolean.append(frequency)
						booleanl.append(loc)
					else:
						boolean[i] = boolean[i] + frequency
						booleanl[i] = booleanl[i] + loc

					if i == len(all_funcs) - 1:
						boolcount += 1

				if prob in tags["string_handling"]:
					if len(string_handling) - 1 < i:
						string_handling.append(frequency)
						string_handlingl.append(loc)
					else:
						string_handling[i] = string_handling[i] + frequency
						string_handlingl[i] = string_handlingl[i] + loc

					if i == len(all_funcs) - 1:
						strcount += 1

				if prob in tags["vectors"]:
					if len(vectors) - 1 < i:
						vectors.append(frequency)
						vectorsl.append(loc)
					else:
						vectors[i] = vectors[i] + frequency
						vectorsl[i] = vectorsl[i] + loc

					if i == len(all_funcs) - 1:
						vectorcount += 1


	#goes through each list and calculates the average frequency
	for a in range(0, len(all_funcs)):
		element = IO[a]
		IO[a] = element / iocount
		IOl[a] = IOl[a] / iocount

		element = arithmetic[a]
		arithmetic[a] = element / arithcount
		arithmeticl[a] = arithmeticl[a] / arithcount

		element = comparison[a]
		comparison[a] = element / compcount
		comparisonl[a] = comparisonl[a] / compcount

		element = boolean[a]
		boolean[a] = element / boolcount
		booleanl[a] = booleanl[a] / boolcount

		element = string_handling[a]
		string_handling[a] = element / strcount
		string_handlingl[a] = string_handlingl[a] / strcount

		element = vectors[a]
		vectors[a] = element / vectorcount
		vectorsl[a] = vectorsl[a] / vectorcount

	destwriter.writerow(["Tag"] + all_funcs)
	destwriter.writerow(["IO"] + IO)
	destwriter.writerow(["Locations"] + IOl)
	destwriter.writerow(["Arithmetic"] + arithmetic)
	destwriter.writerow(["Locations"] + arithmeticl)
	destwriter.writerow(["Comparison"] + comparison)
	destwriter.writerow(["Locations"] + comparisonl)
	destwriter.writerow(["Boolean"] + boolean)
	destwriter.writerow(["Locations"] + booleanl)
	destwriter.writerow(["String Handling"] + string_handling)
	destwriter.writerow(["Locations"] + string_handlingl)
	destwriter.writerow(["Vectors"] + vectors)
	destwriter.writerow(["Locations"] + vectorsl)
	destwriter.writerow(["All Programs"] + all_programs)



def goodfuncs2(): #DOES NOT CALCULATE LOCATION
	"""Calculates the frequency of each function that is returned by get_funcs_list for each tag, then
	writes that data to a CSV, separated by tag.
	Frequency is calculated as number of programs that contain that function, not number of occurances of that function"""
	tags = {"I/O" : ["number-io", "checksum", "digits", "double-letters", "even-squares", "for-loop-index", "grade", "median", "negative-to-zero", "pig-latin", "replace-space-with-newline", "small-or-large", "smallest", "string-differences", "string-lengths-backwards", "syllables", "word-stats", "x-word-lines"],
			"arithmetic" : ["number-io", "checksum", "collatz-numbers", "count-odds", "digits", "even-squares", "for-loop-index", "replace-space-with-newline", "scrabble-score", "sum-of-squares", "syllables", "vector-average", "vectors-summed", "wallis-pi", "word-stats"],
			"comparison" : ["collatz-numbers", "compare-string-lengths", "double-letters", "grade", "last-index-of-zero", "median", "mirror-image", "negative-to-zero", "small-or-large", "smallest","string-differences", "super-anagrams"],
			"boolean" : ["compare-string-lengths", "mirror-image", "super-anagrams"],
			"string_handling" : ["checksum", "compare-string-lengths", "digits", "double-letters", "pig-latin", "replace-space-with-newline", "scrabble-score", "string-differences", "string-lengths-backwards", "super-anagrams", "syllables", "word-stats", "x-word-lines"],
			"vectors" : ["count-odds", "last-index-of-zero", "mirror-image", "negative-to-zero", "string-lengths-backwards", "vector-average", "vectors-summed"]}

	#contains frequencies of all functions
	IO = []
	arithmetic = []
	comparison = []
	boolean = []
	string_handling = []
	vectors = []
	all_programs = []

	#tracks number of successful problems in the category
	iocount = 0
	arithcount = 0
	compcount = 0
	boolcount = 0
	strcount = 0
	vectorcount = 0

	if len(sys.argv) > 1:
	    destination = sys.argv[1]
	else:
	    print("please provide a destination file in the format <filename>.csv")
	    exit(1)


	destfile = open(destination, mode="w")
	destwriter = csv.writer(destfile)

	organized_programs = success_only()


	#I removed file from this list because no program with that tag has succeeded, providing no data
	problems = ["all_programs", "number-io", "checksum", "collatz-numbers", "compare-string-lengths", "count-odds", "digits", "double-letters", "even-squares", "for-loop-index", "grade", "last-index-of-zero", "median", "mirror-image", "negative-to-zero", "pig-latin", "replace-space-with-newline", "scrabble-score", "small-or-large", "smallest", "string-differences", "string-lengths-backwards", "sum-of-squares", "super-anagrams", "syllables", "vector-average", "vectors-summed", "wallis-pi", "word-stats", "x-word-lines"]

	all_funcs = get_funcs_list(organized_programs)

	for prob in problems:

		if prob == "all_programs":
			programs = organized_programs[0]

		if prob == "number-io":
			programs = organized_programs[1]

		if prob == "checksum":
			programs = organized_programs[2]

		if prob == "collatz-numbers":
			programs = organized_programs[3]

		if prob == "compare-string-lengths":
			programs = organized_programs[4]

		if prob == "count-odds":
			programs = organized_programs[5]

		if prob == "digits":
			programs = organized_programs[6]

		if prob == "double-letters":
			programs = organized_programs[7]

		if prob == "even-squares":
			programs = organized_programs[8]

		if prob == "for-loop-index":
			programs = organized_programs[9]

		if prob == "grade":
			programs = organized_programs[10]

		if prob == "last-index-of-zero":
			programs = organized_programs[11]

		if prob == "median":
			programs = organized_programs[12]

		if prob == "mirror-image":
			programs = organized_programs[13]

		if prob == "negative-to-zero":
			programs = organized_programs[14]

		if prob == "pig-latin":
			programs = organized_programs[15]

		if prob == "replace-space-with-newline":
			programs = organized_programs[16]

		if prob == "scrabble-score":
			programs = organized_programs[17]

		if prob == "small-or-large":
			programs = organized_programs[18]

		if prob == "smallest":
			programs = organized_programs[19]

		if prob == "string-differences":
			programs = organized_programs[20]

		if prob == "string-lengths-backwards":
			programs = organized_programs[21]

		if prob == "sum-of-squares":
			programs = organized_programs[22]

		if prob == "super-anagrams":
			programs = organized_programs[23]

		if prob == "syllables":
			programs = organized_programs[24]

		if prob == "vector-average":
			programs = organized_programs[25]

		if prob == "vectors-summed":
			programs = organized_programs[26]

		if prob == "wallis-pi":
			programs = organized_programs[27]

		if prob == "word-stats":
			programs = organized_programs[28]

		if prob == "x-word-lines":
			programs = organized_programs[29]

		max_frequency = len(programs)
		freqs = {}

		for program in programs:
			this_run = []
			#print_prog(program)
			for func in program:
				#ACCOUNTS FOR CONSTANTS
				is_constant = check_if_constant(func)
				if (not is_constant) and not (func in this_run):
					this_run.append(func)
					if func in freqs:
						freqs[func] += 1
					else:
						freqs[func] = 1


		if max_frequency > 0:

			print prob
			print "Max possible occurances: %i" % max_frequency
			print


			for i in range(0, len(all_funcs)):
				function = all_funcs[i]
				if function in freqs:
					frequency = (freqs[function] / float(max_frequency))
				else:
					frequency = 0.0


				if prob == "all_programs":
					all_programs.append(frequency)


				#if this is the first IO problem, the the list will be empty so we simply append
				#if it isn't, then the list already contains an entry for each func so we add to each entry
				if prob in tags["I/O"]:
					if len(IO) - 1 < i:
						IO.append(frequency)
					else:
						IO[i] = IO[i] + frequency

					if i == len(all_funcs) - 1:
						iocount += 1

				if prob in tags["arithmetic"]:
					if len(arithmetic) - 1 < i:
						arithmetic.append(frequency)
					else:
						arithmetic[i] = arithmetic[i] + frequency

					if i == len(all_funcs) - 1:
						arithcount += 1

				if prob in tags["comparison"]:
					if len(comparison) - 1 < i:
						comparison.append(frequency)
					else:
						comparison[i] = comparison[i] + frequency

					if i == len(all_funcs) - 1:
						compcount += 1

				if prob in tags["boolean"]:
					if len(boolean) - 1 < i:
						boolean.append(frequency)
					else:
						boolean[i] = boolean[i] + frequency

					if i == len(all_funcs) - 1:
						boolcount += 1

				if prob in tags["string_handling"]:
					if len(string_handling) - 1 < i:
						string_handling.append(frequency)
					else:
						string_handling[i] = string_handling[i] + frequency

					if i == len(all_funcs) - 1:
						strcount += 1

				if prob in tags["vectors"]:
					if len(vectors) - 1 < i:
						vectors.append(frequency)
					else:
						vectors[i] = vectors[i] + frequency

					if i == len(all_funcs) - 1:
						vectorcount += 1
				"""#I can almost guarantee this is not the best way to do this
				if prob == "all_programs":
					all_programs.append(frequency)
					all_prog_funcs.append(function)

				if prob in tags["I/O"]:
					if not function in iofuncs:
						IO.append(frequency)
					else:
						IO[i] = IO[i] + frequency

				
				if prob in tags["arithmetic"]:
					if not function in arithfuncs:
						arithmetic.append(frequency)
						arithfuncs.append(function)						
					else:
						loc = arithfuncs.index(function)
						arithmetic[loc] = arithmetic[loc] + frequency


				if prob in tags["comparison"]:
					if not function in compfuncs:
						comparison.append(frequency)
						compfuncs.append(function)						
					else:
						loc = compfuncs.index(function)
						comparison[loc] = comparison[loc] + frequency


				if prob in tags["boolean"]:
					if not function in boolfuncs:
						boolean.append(frequency)
						boolfuncs.append(function)						
					else:
						loc = boolfuncs.index(function)
						boolean[loc] = boolean[loc] + frequency


				if prob in tags["string_handling"]:
					if not function in strfuncs:
						string_handling.append(frequency)
						strfuncs.append(function)						
					else:
						loc = strfuncs.index(function)
						string_handling[loc] = string_handling[loc] + frequency


				if prob in tags["vectors"]:
					if not function in vectorfuncs:
						vectors.append(frequency)
						vectorfuncs.append(function)						
					else:
						loc = vectorfuncs.index(function)
						vectors[loc] = vectors[loc] + frequency



	#calculated by earlier edition of this program, should be double checked
	iocount = 8
	arithcount = 6
	compcount = 6
	boolcount = 2
	strcount = 7
	vectorcount = 6"""

	#will only contain those funcs with 60% or higher frequency
	iofuncs = []
	arithfuncs = []
	compfuncs = []
	boolfuncs = []
	strfuncs = []
	vectorfuncs = []
	all_prog_funcs = []

	newio = []
	newarith = []
	newcomp = []
	newbool = []
	newstr = []
	newvectors = []
	new_all_progs = []


	for a in range(0, len(all_funcs)):
		element = IO[a]
		IO[a] = element / iocount
		if IO[a] > 0.6:
			iofuncs.append(all_funcs[a])
			newio.append(IO[a])

		element = arithmetic[a]
		arithmetic[a] = element / arithcount
		if arithmetic[a] > 0.6:
			arithfuncs.append(all_funcs[a])
			newarith.append(arithmetic[a])

		element = comparison[a]
		comparison[a] = element / compcount
		if comparison[a] > 0.6:
			compfuncs.append(all_funcs[a])
			newcomp.append(comparison[a])

		element = boolean[a]
		boolean[a] = element / boolcount
		if boolean[a] > 0.6:
			boolfuncs.append(all_funcs[a])
			newbool.append(boolean[a])

		element = string_handling[a]
		string_handling[a] = element / strcount
		if string_handling[a] > 0.6:
			strfuncs.append(all_funcs[a])
			newstr.append(string_handling[a])

		element = vectors[a]
		vectors[a] = element / vectorcount
		if vectors[a] > 0.6:
			vectorfuncs.append(all_funcs[a])
			newvectors.append(vectors[a])


		element = all_programs[a]
		if all_programs[a] > 0.6:
			all_prog_funcs.append(all_funcs[a])
			new_all_progs.append(all_programs[a])

	"""for a in range(0, len(IO)):
		element = IO[a]
		IO[a] = element / iocount
		if IO[a] <= .6:
			freqfirst = IO[:a]
			freqrest = IO[a+1:]
			IO = freqfirst + freqrest

			funcfirst = iofuncs[:a]
			funcrest = iofuncs[a+1:]
			iofuncs = funcfirst + funcrest


	for b in range(0, len(arithmetic)):
		element = arithmetic[b]
		arithmetic[b] = element / arithcount

	for c in range(0, len(comparison)):
		element = comparison[c]
		comparison[c] = element / compcount

	for d in range(0, len(boolean)):
		element = boolean[d]
		boolean[d] = element / boolcount

	for e in range(0, len(string_handling)):
		element = string_handling[e]
		string_handling[e] = element / strcount

	for f in range(0, len(vectors)):
		element = vectors[f]
		vectors[f] = element / vectorcount"""


	destwriter.writerow(["Tag"] + all_prog_funcs)
	destwriter.writerow(["All Programs"] + new_all_progs)

	destwriter.writerow(["Tag"] + iofuncs)
	destwriter.writerow(["IO"] + newio)

	destwriter.writerow(["Tag"] + arithfuncs)
	destwriter.writerow(["Arithmetic"] + newarith)

	destwriter.writerow(["Tag"] + compfuncs)
	destwriter.writerow(["Comparison"] + newcomp)

	destwriter.writerow(["Tag"] + boolfuncs)
	destwriter.writerow(["Boolean"] + newbool)
	
	destwriter.writerow(["Tag"] + strfuncs)
	destwriter.writerow(["String Handling"] + newstr)

	destwriter.writerow(["Tag"] + vectorfuncs)
	destwriter.writerow(["Vectors"] + newvectors)

def main():

	goodfuncs1()
	#fix_strings(['""""', 'v', 'rh:P/', '"Ao6\'\\\\f"""', 'string_first', 'in1', '\\newline', 'string_replacechar', 'print_string', 'in1', 'string_split', 'string_concat', 'string_concat', 'string_concat', 'exec_eq', 'boolean_not', 'string_dup', 'string_concat', 'string_concat', 'string_concat', 'string_stackdepth', 'string_concat', 'string_dup', 'string_nth', 'string_concat', 'string_concat', 'string_length'])
	#print(['""""', 'v', 'rh:P/', '"Ao6\'\\\\f"""', 'string_first', 'in1', '\\newline', 'string_replacechar', 'print_string', 'in1', 'string_split', 'string_concat', 'string_concat', 'string_concat', 'exec_eq', 'boolean_not', 'string_dup', 'string_concat', 'string_concat', 'string_concat', 'string_stackdepth', 'string_concat', 'string_dup', 'string_nth', 'string_concat', 'string_concat', 'string_length'])

if __name__ == '__main__':
	main()
