#This program will send an email alert when a waterspout is detected
#This program will provide the current date and time it was detected
#The current date and time will be that of when the program is being prompted to run


#Email account that sends the alerts:  oswegocloud@gmail.com
#Email password: CloudCoverage1!
#Feel free to use a different email but make sure to change it in this program!

#Code written by: Peter Bush

import smtplib
import datetime

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

#This function is used for the SEND TO part of the alert email
#Change line 18 to fit how you want to send emails to people
def send_to(file):
	#This is the address that is receiving the email
	#Read emails off a text file and send to those emails
	text_file = open("Documents/CloudProject/recipients.txt", "r")
	lines = text_file.readlines()
	
	return lines
	
#This function is used for getting the date and time that the alert was triggered
def date_time():

	#Declare Variables
	#Variable "time" is an integer used to convert military time to actual hour
	#Variable "time" is always be equal to currentDT.hour,12 or currentDT.hour - 12
	#Variable "tod" is a string used to show AM or PM 
	time = 0
	tod = " "
	minute = " "
	second = " "

	#currentDT = datetime.datetime.now() will get the current date and time that this\
	#program is being ran
	currentDT = datetime.datetime.now()

	#Set the variable 'time' equal to the integer currentDT.hour
	#Set the variable 'minute' equal to the string currentDT.minute
	#Set currentDT.minute equal to a string because of the 0 added in front for less than 10
	#Set the variable 'second' equal to the string currentDT.second
	#Set currentDT.second equal to a string because of the 0 added in front for less than 10
	time = currentDT.hour 
	minute = str(currentDT.minute)
	second = str(currentDT.second)

	#This code converts military time to AM or PM
	if currentDT.hour == 24 or currentDT.hour == 0:
		time = 12
		tod = "AM"
	elif currentDT.hour > 12:
		time = currentDT.hour - 12
		tod = "PM"
	elif currentDT.hour < 12:
		time = currentDT.hour
		tod = "AM"
	elif currentDT.hour == 12:
		time = currentDT.hour
		tod = "PM"

	#This code adds adds a 0 in front of the minute if it is less than 10
	#It does not add a 0 in front if it is greater than 10 	
	if currentDT.minute < 10:
		minute = "0" + str(currentDT.minute)
	else:
		minute = str(currentDT.minute)

	#This code adds adds a 0 in front of the second if it is less than 10
	#It does not add a 0 in front if it is greater than 10 	
	if currentDT.second < 10:
		second = "0" + str(currentDT.second)
	else:
		second = str(currentDT.second)
		
	return time, minute, second, tod, currentDT
	
#This function creates and sends the email	
def send_message(file):
	
	lines = send_to(file)
	time, minute, second, tod, currentDT = date_time()
	
	toaddr = lines

	msg = MIMEMultipart()

	#This is the address sending the email
	fromaddr = "oswegocloud@gmail.com"
	msg['From'] = fromaddr

	msg['Subject'] = "Waterspout Detected!"


	#This is the body of the email, which will be sent
	body = "A waterspout has been detected on Lake Ontario! \nDate Detected: " + \
		str(currentDT.month) + "-" + str(currentDT.day) + "-" + str(currentDT.year) + \
		"\nTime Detected: " + str(time) + ":" + minute + ":" + second + " " + tod + \
		"\n\nAttached is a picture of the waterspout!"
		
	msg.attach(MIMEText(body, 'plain'))

	#This is for the attachment
	#Will be a picture of a waterspout
	filename = "test.jpg"
	attachment = open("/Users/peterbush/Documents/CloudProject/test.jpg", "r")
	
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
	msg.attach(part)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "CloudCoverage1!")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	
#This statement is used to send the email	
send_message("Users/peterbush/Documents/CloudProject/cloudAlert.py")
print "Email sent"

