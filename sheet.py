import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

#load your json file(you get this when you request the google spreadsheet api)
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
ACCOUNT_SID = 'AC598fdd1a56846658f660************'
AUTH_TOKEN = 'ce2337ed21d390367e01************'
#your twilio number
my_twilio_num = "+185646*****"

#create a client object containing your twilio credential
client = Client(ACCOUNT_SID, AUTH_TOKEN)
#iterate over each and every guest 
for num in range(2, n):
    print("sleeping for 2 seconds")
    #add a delay to avoid filtering by your service career	
    time.sleep(2)
    #get the guest number from your spreadsheet	
    g_num = gi_g.acell('B'+str(num)).value
    #get the guest name from your spreadsheet
    g_name = gi_g.acell('A'+str(num)).value
    message = "Hey Its my Birthday!Please text 'Yes' or 'No' to confirm your presence."
    print('Sending message to ' + g_name) 
    #send the guests a message	
    client.messages.create(
            to="+1" + g_num,
            from_="" + my_twilio_num,
            body=message,
        )
    #keep a counter of the messages sent to the guests
    gi_g.update_acell('C'+str(num), gi_g.acell('C'+str(num)).value + str(1)) 

print('finished')

