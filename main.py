#MADE BY KESHAV SANTHANAM AND SAMEER ISLAM
import sys
import time

def display_time(start, end):
	elapsed_time = end - start
	# print("Elapsed time: {:.2f} seconds".format(elapsed_time))

def main():
	all_output = ""
    
    # each line: [line_num, [sign, var]]
	kb_file = sys.argv[1]
	with open(kb_file, 'r') as f:
		original_lines = f.readlines()            
	original_test_clause = original_lines.pop()
	count = 1
	lines = []
	for line in original_lines:
		vars = line.split()
		temp = []
		for var in vars:                
			if var[0] == '~':
				temp.append(('-', var[1:]))
			else:
				temp.append(('+', var))
		lines.append([count, temp])
		count += 1

		test_clause = original_test_clause.split()
		test_clause_vars = []
		for var in test_clause:
			if var[0] == '~':
				test_clause_vars.append(('+', var[1:]))
			else:
				test_clause_vars.append(('-', var))
	
	for var_tup in test_clause_vars:
		sublist = [count, [var_tup]]
		lines.append(sublist)
		count += 1
	
	sorted_lines = lines.copy()
	for i in range(len(lines)):
		sorted_lines[i][1] = sorted(lines[i][1])
		
    # beginnning of printing (inputs)
	for line in lines:
		out_string = ""
		for op, variable in line[1]:
			out_string += "~" if op == '-' else ''
			out_string += variable + ' '       
		print(f"{line[0]}. {out_string}{{}}")
		all_output += f"{line[0]}. {out_string}{{}}\n"
		out_string = ""
    
	def is_redundant(new_clause, lines):
		# sample line: [1, [['-', 'p'], ['+', 'q']]]
		s_nc = sorted(new_clause)
		for line in lines:
			if s_nc == line[1]:
				return True
		return False
	#print(is_redundant([1, [('+', 'q'), ('-', 'p')]], lines[0:5]))

	def resolvable(line1, line2):
		set1, set2 = set(), set()
		for sign, var in line1[1]:
			set1.add(var)
		for sign, var in line2[1]:
			set2.add(var)
		return len(set1.intersection(set2)) > 0
	
	def generate(prev, curr):
		# [1, [('-', 'NoLeak'), ('-', 'LowTemp'), ('+', 'ReactorUnitSafe'), ('-', 'NoLeakH1'), ('-', 'NoLeakH2'), ('+', 'okH1'), ('+', 'okH2'), ('+', 'l'), ('+', 'V1'), ('+', 'V2')]]
		prev_vals, curr_vals = prev[1].copy(), curr[1].copy()
		final = []
		visited = set()
		removed = False
		for i in range(len(prev_vals)):
			sign, var = prev_vals[i]
			if sign == '-':
				temp = ('+', var)
				if temp in curr_vals:
					prev_vals.remove((sign, var))
					curr_vals.remove(temp)		
					removed = True			
					break
			elif sign == '+':
				temp = ('-', var)
				if temp in curr_vals:
					prev_vals.remove((sign, var))
					curr_vals.remove(temp)
					removed = True			
					break
										
		combined_vals = curr_vals + prev_vals
		final_vals = []
		if not removed:
			return final_vals		
		for val in combined_vals:
			sign, var = val
			if sign == '+':
				if ('-', var) in combined_vals:
					return []
			else:
				if ('+', var) in combined_vals:
					return []
			if val not in visited:
				final_vals.append(val)
			visited.add(val)
		return final_vals
	
	# resolution
	has_contradiction = False
	cd_idx = (0, 0)
	i = 1
	continue_flag = True
	while not has_contradiction and i < len(lines):
		# try all clauses from [0:clause_index] for each clause
		# append each new clause to lines
		for j in range(i):
			if resolvable(lines[j], lines[i]):
				final = lines[j][1] + lines[i][1]
				if len(final) == 2 and final[0][0] != final[1][0] and final[0][1] == final[1][1]:
					has_contradiction = True
					cd_idx = (i+1, j+1)
					j = i
					continue_flag = False
				if continue_flag:
					candidate = generate(lines[j], lines[i])
					if candidate == []:
						continue
					if not is_redundant(candidate, sorted_lines):
						lines.append([count, candidate])
						sorted_lines.append([count, sorted(candidate)])
						for op, variable in candidate:
							out_string += "~" if op == '-' else ''
							out_string += variable + ' '       
						print(f"{count}. {out_string}{{{i+1}, {j+1}}}")
						all_output += f"{count}. {out_string}{{{i+1}, {j+1}}}\n"
						count += 1
						out_string = ""
		if has_contradiction:
			lines.append(f"Contradiction {{{cd_idx[0]}, {cd_idx[1]}}}")
			print(f"{count}. {lines[-1]}")
			print("Valid")
			all_output += f"{count}. {lines[-1]}\nValid\n"
			
		i += 1
	if not has_contradiction:
		print("Fail")

	# file1 = open("task_output.out", "w") 
	# file1.write(all_output)
	# file1.close()


if __name__ == "__main__":
	start_time = time.time()
	main()

	end_time = time.time()

	# Display elapsed time
	display_time(start_time, end_time)
