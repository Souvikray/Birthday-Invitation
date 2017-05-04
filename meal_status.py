import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest  import Client

#load your json file
json_key = json.load(open('')) #add file name for the json created for the spread sheet
scope = ['https://spreadsheets.google.com/feeds']

creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#authorize yoir credentials
client = gspread.authorize(creds)
#open your spreadsheet
gi = client.open("GuestInfo")
#get your first worksheet
gi_g = gi.get_worksheet(0)
#get your second worksheet
gi_f = gi.get_worksheet(1)

#your twilio credentials
ACCOUNT_SID = 'AC598fdd1a56846658f660************'
AUTH_TOKEN = 'ce2337ed21d390367e01************'
#your twilio number
my_twilio_num = "+185646*****"

#create a client object containing your twilio credential
client = Client(ACCOUNT_SID, AUTH_TOKEN) 

#iterate over each and every guest     
for num in range(2,n):
   
   #get the phone number of the guest who chose the meal 
   gf_num = gi_f.acell('D' +str(num)).value 
   
   #if the cell is not empty ie the guest has chosen a meal
   if not gf_num=="":
    #check the number provided by the guest in your first worksheet and store the value of the cell containing that number
    g_num = gi_g.find(gf_num).value
    #get the row of the cell containing the matched number
    g_num_row = gi_g.find(gf_num).row
    #get the name of the guest of that particular row 
    g_name = gi_g.acell('A' + str(g_num_row)).value
    #get the cell containing the phone number of the guest
    g_cell = gi_g.find(str(g_num).strip())
    #get the row of that cell and update the confirmation status
    gi_g.update_acell('E'+str(g_cell.row),'Y')	
    #get the meal status of the guest
    meal_status = gi_g.acell("E" + str(g_num_row)).value
    #get the number of meals confirmed
    g_meal_conf = gi_f.acell('B12').value
    #get the number of meals unconfirmed 
    g_meal_unconf = gi_f.acell('B14').value
    
    #if the number provided by the guest in the form matches the number in your database(spreadsheet)
    if gf_num == g_num:
	  #if the guest has confirmed the meal  
          if meal_status == 'Y':
           print('Meal already confirmed!') 
          
	  #update the spreadsheet for latest confirmation
          else:
            print ('Updating data for '+g_name)
            gi_g.update_acell("E" + str(g_num_row), 'Y')
   
    #if the guest hasn't confirmed their meal preference	
    else:
      print('Nothing found')
      #increment the message count
      gi_g.update_acell('C'+str(num), gi_g.acell('C' +str(num)).value + str(1))
   
   print("Sending confirmation message to guests about their preferences")	
   client.messages.create(
   from_="" + my_twilio_num
   to=g_num, 
   body ="Hey "+g_name + "!"+"You chose "+gi_g.acell('B'+str(num)+" & "+gi_g.acell('C'+str(num)+"!"+" See you on my birthday!")

   #send message to yourself that the process has been completed with latest stats
   client.messages.create(
   from_="" + my_twilio_num
   to="+919844******", #admin number
   body ="Finished Scanning!\nGuest meals confirmed" + guest_meals_confirmed + "\nGuest meals unconfirmed: " + guest_meals_unconfirmed)
	
