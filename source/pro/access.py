import glob
import math
import numpy as np
import csv
import os.path
from os import path
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
		venue = venue.replace(',' , '')
		bats_name = ""
		bow_name = ""
		bowler_dict = {}
		batsmen_dict = {}
		run_after = 0
		ball_count = 0
		prev_over = 0
		cur_over = 0
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
				if row[7] == '4':
					ls[5] = ls [5] + 1
				######### 6: Number of 6's##################
				if row[7] == '6':
					ls[6] = ls[6] + 1
				batsmen_dict[bats_name] = ls


			if bow_name not in self.bowlers:
				ls2 = [bow_name]			#0: bowler name
				if row[3] == teams[0]:
					ls2.append(teams[1])	#1: team name
					ls2.append(teams[0])	#2: opponent team
				else:
					ls2.append(teams[0])
					ls2.append(teams[1])
				ls2.append(0)				#3: runs scored
				ls2.append(0)				#4: balls faced
				ls2.append(0)				#5: 4's
				ls2.append(0)				#6: 6's
				ls2.append(0)				#7: Strike rate
				ls2.append(0)				#8: Balls bowled
				ls2.append(0)				#9: overs
				ls2.append(int(row[7]) + int(row[8]))	#10: Runs givens
				################11: wickets ######################
				ball_count = 1
				run_after = ls2[10]
				prev_over = int(float(row[2]))
				cur_over = int(float(row[2]))
				if row[9] != "":
					if row[9] != 'run out':
						ls2.append(1)
					else:
						ls2.append(0)
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

				cur_over = int(float(row[2]))
				# prev_over = cur_over			
				if(cur_over == prev_over):
					ball_count = ball_count + 1
					if ball_count == 6:
						run_after = run_after + int(row[7]) + int(row[8])
						if run_after == 0:
							ls2[12] = ls2[12] + 1
						run_after = 0
						
					else:
						run_after = run_after + int(row[7]) + int(row[8])
				else:
					ball_count = 1
					run_after = 0
					prev_over = int(float(row[2]))
					# cur_over = int(float(row[2]))



				bowler_dict[bow_name] = ls2
			self.batsmen.add(bats_name)
			self.bowlers.add(bow_name)
			#with open("players/" + bats_name + ".csv", 'w'):
			#with open("players/" + bats_name + ".csv", 'w'):
		################# calc batsmen strike rate ##################
		for l , j in batsmen_dict.items():
			temp = j
			temp[7] = (temp[3] / temp [4])*100
			batsmen_dict[l] = temp

		################## calc bowler's economy and over ########
		for l, j in bowler_dict.items():
			temp = j
			temp[9] = temp[8] // 6
			if temp[9] != 0:
				temp[13] = temp[10] / temp [9]
			bowler_dict[l] = temp


		# print()
		# for l, j in bowler_dict.items():
		# 	print(l, " : ", j)

		############# merging bowler and batsmen dictionary#############
		for l, j in batsmen_dict.items():
			# print(l, " : ", j)
			if l in bowler_dict.keys(): 
				temp = batsmen_dict[l]
				temp1 = bowler_dict[l]
				for i in range(11):
					temp[i+3] = max(temp[i+3] , temp1[i+3])
				batsmen_dict[temp[0]] = temp
				# print(batsmen_dict[temp[0]])
				del bowler_dict[temp[0]]

		print()

		########## still merging ####################
		for l, j in bowler_dict.items():
			batsmen_dict[l] = bowler_dict[l]
		
		############# calculating total score ########
		for l, j in batsmen_dict.items():
			temp = batsmen_dict[l]
			temp.append(0)
			score = 0
			score += temp[3]			# runs scored
			score += temp[5]			# 4's
			score += temp[6]*2			# 6's
			if(temp[3] >= 100):
				score += 16				# century
			elif temp[3] >= 50:			# half-century
				score += 8
			if ((temp[4] > 0) and (temp[3] == 0)):
				score -= 2				# out for duck
			###### SR score,  TODO: exclude bowlers #########
			if temp[4] > 0 :
				if temp[7] >= 60 and temp[7] < 70 :
					score -= 2

				elif temp[7] >= 50 and temp[7] < 60 :
					score -= 4
				elif temp[7] < 50 :
					score -= 6
			########### wickets ###########
			score += temp[11]*25
			if temp[11] >= 5:
				score += 16
			elif temp[11] == 4:
				score += 8

			score += temp[12]*8			# maiden
			############## economic rate ##################
			if temp[9] >= 2 :
				if temp[13] < 4: 
					score += 6
				elif temp[13] < 5:
					score += 4
				elif temp[13] < 6:
					score += 2
				elif temp[13] >9 and temp[13] <= 10:
					score -= 2
				elif temp[13] >10 and temp[13] <= 11:
					score -= 4
				elif temp[13] > 11:
					score -= 6

			temp[15] = score

			batsmen_dict[l] = temp				######## final score ##############
			print(l, " : ", j)
			filename = "all_csv/" + l + ".csv"
			# print(filename)
			# print(j[0])
			# heading = [ "bat" , "bowl" , "field"]
			# if not (path.exists("../all_csv/" + filename)):
			# 		with open (filename , "a") as csvfile:
			# 			writer = csv.writer(csvfile , delimiter = ',')
			# 			writer.writerow(heading)
				
			with open (filename , "a") as csvfile:
				writer = csv.writer(csvfile , delimiter = ',')
				writer.writerow(temp)
def addH():

	header = ["Player name" , "Country" , "Opponent team" , "Runs Scored" , "Balls played" , "Four" , "Six" , "Strike Rate" , "Balls bowled" , "over" , "Runs Given" , "Wickets" , "Maiden Over" , "Economy" , "Venue" , "Total Score"]
	files = []
	for file in glob.glob("all_csv/*"):
		with open(file , "r") as infile:
			reader = list(csv.reader(infile))
			reader.insert(0, header)

		with open(file, "w") as outfile:
			writer = csv.writer(outfile)
			for line in reader:
				writer.writerow(line)



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
addH()