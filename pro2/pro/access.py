"""
@file File Documentation
"""
import glob
import yaml
import math
import numpy as np
import csv
import os.path
from os import path
##Class Responsible for opening and preprocessing a single file
#This class is will open an instance of a single CSV file of a match, preprocess it and create/append to CSV files for players playing/contributing in the match.
class Read:
	##Constructor to initialize the filename of the CSV file associated with the object
	def __init__(self, filename):
		##Filename of the CSV file of the match.
		self.filename = filename 

	##Member function to initialize a few variables related to the match, like team names, venue of the match, etc.
	#Function also reads the CSV file and stores it into two tables in the memory, player_details, and match_details.
	def read_file(self):
		##Matrix containing per ball data of the match.
		self.player_details = [] 
		##Matrix containing match details of the match.
		self.match_details = [] 
		with open(self.filename, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			next(reader, None)
			for row in reader:
				if len(row) == 3:
					self.match_details.append(row)
				else:
					self.player_details.append(row)
		s = "YAML" + self.filename[12:-4] + ".yaml"
		with open(s, "r") as stream:
			try:
				##Contains data of the match in YAML format, to get extra information of the match wrt the players who have caught/run out batsmen.
				self.data = yaml.safe_load(stream) 
				# print(s)
			except yaml.YAMLError as exc:
				print(exc)

	def print_file(self):
		for d in self.player_details:
			print(d)

	##Function associated with preprocessing the tables and generating a CSV for each player playing in the match if no CSV is already generated, or appending to the CSV if the CSV is already generated.
	def gen_csv(self):
		##List of batsmen playing in the match, initialized to empty
		self.batsmen = set(()) 
		##List of bowlers playing in the match, initialized to empty
		self.bowlers = set(()) 

		self.fielder = set(())

		self.teamplayers = set(())
		self.year_set = ['2003' , '2004' , '2005' , '2006' , '2007' , '2008' , '2009' , '2010' , '2011' , '2012' ,
		 '2013' , '2014' , '2015' , '2016' , '2017' , '2018' , '2019' , '2020' , '2021']
		teams = []
		# print("--------------------------------------------")
		for row in self.match_details:
			if row[1] == 'team':
				teams.append(row[2])
			if row[1] == 'venue':
				venue = row[2]
		venue = venue.replace(',' , '')
		for row in self.match_details:
			if row[1] == 'date':
				year = row[2]
				year = year[:4]
				# print(year)
		bats_name = ""
		bow_name = ""
		fiel_name = ""
		bowler_dict = {}
		batsmen_dict = {}
		fielder_dict = {}
		encode_year = []
		run_after = 0
		ball_count = 0
		prev_over = 0
		cur_over = 0
		delivery = 0
		inning = 1
		for row in self.player_details:
			bats_name = row[4]
			bow_name = row[6]
			bats_name = bats_name.replace(" ", "")
			bow_name = bow_name.replace(" ", "")
			#print(inning, "\t", row[1])
			if inning == 1 and row[1] == '2':
				inning = 2
				delivery = 0
			#print(inning, "\t", row[1])
			#print(row[2], "\t", delivery)
			self.teamplayers.add(bats_name)
			self.teamplayers.add(bow_name)
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


				######################################PATCH WORK################################################
				if row[9] == 'run out':
					if inning == 1:
						s = '1st innings'
					else:
						s = '2nd innings'
					##In case the person who has run out the batsmen is the bowler itself.
					try:
						runout = self.data['innings'][inning - 1][s]['deliveries'][delivery][float(row[2])]['wicket']['fielders']
						# print(runout)
						fiel_name = runout[0].replace(" ","")
						# print(fiel_name)
						if fiel_name not in self.fielder:
							ls3 = [fiel_name]
							ls3.append(1)
							ls3.append(0)
							fielder_dict[fiel_name] = ls3
						else:
							ls3 = fielder_dict[fiel_name]
							ls3[1] += 1
							fielder_dict[fiel_name] = ls3

						# print(row[9], "\t", self.data['innings'][inning - 1][s]['deliveries'][delivery][float(row[2])]['wicket']['fielders'])
					except:
						# print("yaha3")
						# print(bow_name)
						fiel_name = bow_name
						if fiel_name not in self.fielder:
							ls3 = [fiel_name]
							ls3.append(1)
							ls3.append(0)
							fielder_dict[fiel_name] = ls3
						else:
							ls3 = fielder_dict[fiel_name]
							ls3[1] += 1
							fielder_dict[fiel_name] = ls3

					self.fielder.add(fiel_name)
					self.teamplayers.add(fiel_name)
				if row[9] == 'caught':
					if inning == 1:
						s = '1st innings'
					else:
						s = '2nd innings'
					caughtout = self.data['innings'][inning - 1][s]['deliveries'][delivery][float(row[2])]['wicket']['fielders']
					# print(caughtout)
					fiel_name = caughtout[0].replace(" ","")
					# print(fiel_name)
					if fiel_name not in self.fielder:
							ls3 = [fiel_name]
							ls3.append(0)
							ls3.append(1)
							fielder_dict[fiel_name] = ls3
					else:
						ls3 = fielder_dict[fiel_name]
						ls3[2] += 1
						fielder_dict[fiel_name] = ls3
					# print(row[9], "\t", self.data['innings'][inning - 1][s]['deliveries'][delivery][float(row[2])]['wicket']['fielders'])
					self.fielder.add(fiel_name)
				#################################FINISH PATCH WORK##############################################

				bowler_dict[bow_name] = ls2
				
			else:
				ls2 = bowler_dict[bow_name]

				#################################PATCH WORK##################################################
				
				if row[9] == 'run out':
					if inning == 1:
						s = '1st innings'
					else:
						s = '2nd innings'

					##In case the person who has run out the batsmen is the bowler itself.
					try:
						runout = self.data['innings'][inning - 1][s]['deliveries'][delivery][float(row[2])]['wicket']['fielders']
						# print("trty")
						# print(runout)
						fiel_name = runout[0].replace(" ","")
						# print(fiel_name)
						if fiel_name not in self.fielder:
							ls3 = [fiel_name]
							ls3.append(1)
							ls3.append(0)
							fielder_dict[fiel_name] = ls3
						else:
							ls3 = fielder_dict[fiel_name]
							ls3[1] += 1
							fielder_dict[fiel_name] = ls3
						# print(row[9], "\t", self.data['innings'][inning - 1][s]['deliveries'][delivery][float(row[2])]['wicket']['fielders'])
					except:
						# print("yaha2")
						# print(bow_name)
						fiel_name = bow_name
						if fiel_name not in self.fielder:
							ls3 = [fiel_name]
							ls3.append(1)
							ls3.append(0)
							fielder_dict[fiel_name] = ls3
						else:
							ls3 = fielder_dict[fiel_name]
							ls3[1] += 1
							fielder_dict[fiel_name] = ls3

					self.fielder.add(fiel_name)
				if row[9] == 'caught':
					if inning == 1:
						s = '1st innings'
					else:
						s = '2nd innings'
					try:

						caughtout = self.data['innings'][inning - 1][s]['deliveries'][delivery][float(row[2])]['wicket']['fielders']
						# print(caughtout)
						fiel_name = caughtout[0].replace(" ","")
						# print(fiel_name)
						if fiel_name not in self.fielder:
							ls3 = [fiel_name]
							ls3.append(0)
							ls3.append(1)
							fielder_dict[fiel_name] = ls3
						else:
							ls3 = fielder_dict[fiel_name]
							ls3[2] += 1
							fielder_dict[fiel_name] = ls3
						# print(row[9], "\t", self.data['innings'][inning - 1][s]['deliveries'][delivery][float(row[2])]['wicket']['fielders'])
					except:
						# print("yaha1")
						# print(bow_name)
						fiel_name = bow_name
						if fiel_name not in self.fielder:
							ls3 = [fiel_name]
							ls3.append(0)
							ls3.append(1)
							fielder_dict[fiel_name] = ls3
						else:
							ls3 = fielder_dict[fiel_name]
							ls3[2] += 1
							fielder_dict[fiel_name] = ls3

					self.fielder.add(fiel_name)
				##############################FINISH PATCH WORK###############################################
				

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
			delivery += 1
			#with open("players/" + bats_name + ".csv", 'w'):
			#with open("players/" + bats_name + ".csv", 'w'):



		# print( self.teamplayers)
		# for l, j in fielder_dict.items():
		# 	# print(l, " : ", j)







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

		# print()

		########## still merging ####################
		for l, j in bowler_dict.items():
			batsmen_dict[l] = bowler_dict[l]
		


		# print( self.teamplayers)
		# for l, j in batsmen_dict.items():
		# 	print(l)

		###########################################

		for l, j in batsmen_dict.items():
			temp = batsmen_dict[l]

			temp.append(0)
			temp.append(0)
			temp.append(year)
			batsmen_dict[l] = temp




		################# append catch and runout ###########
		for l , j in batsmen_dict.items():

			if l in fielder_dict.keys():
				temp = batsmen_dict[l]
				temp1 = fielder_dict[l]
				temp[15] = temp1[1]							#runout
				temp[16] = temp1[2]							#catchout
				batsmen_dict[l] = temp

		print()
#"Player name" , "Country" , "Opponent team" , "Runs Scored" , "Balls played" , "Four" , "Six" , "Strike Rate" , "Balls bowled" 
#, "over" , "Runs Given" , "Wickets" , "Maiden Over" , "Economy" , "Venue" , "runout" , "catch" , "year" ,"Total Score"]
		for l,j in fielder_dict.items():
			if l not in fielder_dict.keys():
				temp=[l ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,over,0 ,0 ,0 ,0 ,venue , j[1], j[2] , year ]
				batsmen_dict[l] = temp
				print(batsmen_dict[l])
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
			########## catch and run out #################

			score += temp[15]*12
			score += temp[16]*8

			temp[18] = score

			batsmen_dict[l] = temp				######## final score ##############
			#print(l, " : ", j)
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

			
		encode = []
		encode_year = []
		with open ("temp.csv" , "r") as playercsv:
			reader = csv.reader( playercsv , delimiter = ',')
			for row in reader:
				# print(row[1])
				# print()
				if row[1] in self.teamplayers:
					encode.append(1)
				else:
					encode.append(0) 
		# print(self.filename)
		for i in self.year_set:
			# print(year)
			if year == i:


				# print(year)
				encode_year.append(1)
			else:
				encode_year.append(0)
		# print(encode_year)
		encode += encode_year
		# encode.append(encode_year)
		# print(encode)
		counter = 0
		# print(self.filename)
		for i in self.teamplayers:
			encode_temp = []
			# if counter != 0:
				# encode_temp = encode[:-counter]
			# else:
			encode_temp = encode[:]
			counter += 1
			filename2 = "train/" + i + ".csv"
			# print(i)
			if i not in batsmen_dict:
				continue
			templist = batsmen_dict[i]
			# print(templist)
			player_score = templist[-1:]
			# print(i)
			# print(player_score)
			encode_temp += player_score
			# print(encode_temp)
			# print(len(encode_temp))
			with open ( filename2 , "a" ) as traincsv:
					writer = csv.writer(traincsv , delimiter = ',')
					writer.writerow(encode_temp)

def addH():

	header = ["Player name" , "Country" , "Opponent team" , "Runs Scored" , "Balls played" , "Four" , "Six" , "Strike Rate" , "Balls bowled" , "over" , "Runs Given" , "Wickets" , "Maiden Over" , "Economy" , "Venue" , "runout" , "catch" , "year" ,"Total Score"]
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
