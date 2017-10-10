import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

#load your json file
json_key = json.load(open('client_secret.json'))
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#verify your credentials
client = gspread.authorize(creds)
#open your spreadsheet
gi = client.open("GuestInfo")
#access the first worksheet
gi_g = gi.get_worksheet(0)

#your twilio account credentials 
ACCOUNT_SID = 'AC598fdd1a56846658****************'
AUTH_TOKEN = 'ce2337ed21d39036****************'
#your twilio number
my_twilio_num = "+1856*******"

#create a client object containing your twilio credential
client = Client(ACCOUNT_SID, AUTH_TOKEN) 

#iterate over each and every guest     
for num in range(2,n):
    print("sleeping for 2 seconds")
    #add a delay to avoid filtering by your service career
    time.sleep(2)
    #get the guest number
    g_num = gi_g.acell('B' +str(num)).value
    #get the guest name 
    g_name = gi_g.acell('A'+str(num)).value 
    #get the guest meal preference
    g_pref = gi_g.acell('E' +str(num)).value
    
    #if the guest has not chosen a meal
    if g_pref == "":
    	print('Sending message to ' + g_name)
	client.messages.create(
	    to="+" +wedding_guest_number, 
	    from_="" +my_twilio_num,
	    body ="You haven't selected your meal preference.Please visit the link- https://docs.google.com/forms/d/e/1FAIpQLSfTbv7IoHRk7hyRfOdtrGKHGko4OUF2G6gVA0N_8uOgtBsemg/viewform 		   and fill out the form"
	    )
	#increment the message count
	gi_g.update_acell('C'+str(num), gi_g.acell('C' +str(num)).value +str(1))
                
print('Process finished')
