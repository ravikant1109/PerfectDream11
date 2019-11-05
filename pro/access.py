import glob
import math
import numpy as np
import csv
class Read:
	def __init__(self, filename):
		self.filename = filename
	def read_file(self):
		self.player_details = []
		self.match_details = []
		with open(self.filename, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			next(reader, None)
			for row in reader:
				if len(row) == 3:
					self.match_details.append(row)
				else:
					self.player_details.append(row)
	def print_file(self):
		for d in self.player_details:
			print(d)
	def gen_csv(self):
		self.batsmen = set(())
		self.bowlers = set(())
		teams = []
		for row in self.match_details:
			if row[1] == 'team':
				teams.append(row[2])
			if row[1] == 'venue':
				venue = row[2]
		bats_name = ""
		bow_name = ""
		bowler_dict = {}
		batsmen_dict = {}
		run_after = 0
		balls = 0
		for row in self.player_details:
			bats_name = row[4]
			bow_name = row[6]
			bats_name = bats_name.replace(" ", "")
			bow_name = bow_name.replace(" ", "")
			if bats_name not in self.batsmen:
				ls = [bats_name, row[3]]	#0: batsman name,1: team of batsman
				if teams[0] == row[3]:
					ls.append(teams[1])		#2: opponent team
				else:
					ls.append(teams[0])		#2: opponent team
				ls.append(int(row[7]))		#3: Runs Scored
				ls.append(1)				#4: balls played
				########## 5:Number of 4's#################
				if row[7] == 4:
					ls.append(1)
				else:
					ls.append(0)
				######### 6: Number of 6's##################
				if row[7] == 6:
					ls.append(1)
				else:
					ls.append(0)
				ls.append(0)				# 7: Strike rate
				ls.append(0)				# 8: bowls bowled
				ls.append(0)				# 9:overs
				ls.append(0)				# 10:Runs given
				ls.append(0)				# 11: Wickets
				ls.append(0)				# 12: Maiden	
				ls.append(0)				# 13: Economy
				ls.append(venue)			# 14: Venue
				batsmen_dict[bats_name] = ls

			else:
				ls = batsmen_dict[bats_name]
				ls[3] = ls[3] + int(row[7])
				ls[4] = ls[4] + 1
				########## 5:Number of 4's#################
				if row[7] == 4:
					ls[5] = ls [5] + 1
				######### 6: Number of 6's##################
				if row[7] == 6:
					ls[6] = ls[6] + 1
				batsmen_dict[bats_name] = ls


			if bow_name not in self.bowlers:
				ls2 = [bow_name]
				if row[2] == teams[0]:
					ls2.append(teams[1])
					ls2.append(teams[0])
				else:
					ls2.append(teams[0])
					ls2.append(teams[1])
				ls2.append(0)				#3: runs scored
				ls2.append(0)				#4: balls faced
				ls2.append(0)				#5: 4's
				ls2.append(0)				#6: 6's
				ls2.append(0)				#7: Strike rate
				ls2.append(1)				#8: Balls bowled
				ls2.append(0)				#9: overs
				ls2.append(int(row[7]) + int(row[8]))	#10: Runs givens
				################11: wickets ######################
				balls = 1
				run_after = ls2[10]
				if row[9] != "":
					if row[9] != 'run out':
						ls2.append(1)
					else:
						ls2.append(0)
				ls2.append(0)				#12: maiden 
				ls2.append(0)				#13: economy
				ls2.append(venue)			#14: venue
				bowler_dict[bow_name] = ls2
			else:
				ls2 = bowler_dict[bow_name]
				ls2[8] += 1 #8: Balls bowled
				ls2[10] += int(row[7]) + int(row[8]) #10: Runs given
				##############11: Wickets ##########################
				if row[9] != "":
					if row[9] != 'run out':
						ls2[11] += 1

				balls = balls + 1
				if balls == 6:
					if run_after == 0:
						ls2[12] = ls2[12] + 1
					run_after = 0
					balls = 1
				else:
					run_after = run_after + ls2[10]
				bowler_dict[bow_name] = ls2
			self.batsmen.add(bats_name)
			self.bowlers.add(bow_name)
			#with open("players/" + bats_name + ".csv", 'w'):
			#with open("players/" + bats_name + ".csv", 'w'):
		# for l, j in batsmen_dict.items():
		# 	print(l, " : ", j)

		# print()
		# print()

		for l , j in batsmen_dict.items():
			temp = dj
			temp[7] = (temp[3] / temp [4])*100
			batsmen_dict[l] = temp

		for l, j in bowler_dict.items():
			temp = j
			temp[9] = temp[8] // 6
			temp[13] = temp[10] / temp [9]
			bowler_dict[l] = temp

		print()
		for l, j in batsmen_dict.items():
			print(l, " : ", j)
		print()

		for l, j in bowler_dict.items():
			print(l, " : ", j)
		print()

		for l, j in batsmen_dict.items():
			# print(l, " : ", j)
			if l in bowler_dict.keys(): 
				temp = batsmen_dict[l]
				temp1 = bowler_dict[l]
				for i in range(10):
					temp[i+3] = max(temp[i+3] , temp1[i+3])
				batsmen_dict[temp[0]] = temp
				# print(batsmen_dict[temp[0]])
				del bowler_dict[temp[0]]


		for l, j in bowler_dict.items():
			batsmen_dict[l] = j
			# print(l, " : ", j)
		

		for l, j in batsmen_dict.items():
			print(l, " : ", j)





files = []
for file in glob.glob("t20_csv_male/*"):
	files.append(Read(file))
	# print(file)
# files[0].read_file()
# files[0].gen_csv()
# files[1].read_file()
# files[1].gen_csv()
for f in files:
	f.read_file()
	f.gen_csv()