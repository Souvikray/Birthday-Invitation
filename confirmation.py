from flask import Flask,request
#import twilio.twiml
from twilio.twiml.messaging_response import MessagingResponse
import time
import json 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#create a flask app
app = Flask(__name__)

#load your json file
json_key = json.load(open('client_secret.json'))
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#authorize your credentials
client = gspread.authorize(creds)
#open your spreadsheet
gi = client.open("GuestInfo")
#get your first worksheet
gi_g = gi.get_worksheet(0)
#get your second worksheet
gi_f = gi.get_worksheet(1)

#just for sanity check...when your server is running,this is what you will see
@app.route("/")
def hello():
    return "My birthday!!"

#all the sms requests will be handled in the messages section of our app
@app.route("/messages",methods=['GET' , 'POST'])
def contact_guest():
        #create a twilio response object
	#resp = twilio.twiml.Response()
	resp = MessagingResponse()
        #get the number from the twilio http request 
	from_num = request.values.get('From', None)
        #get the body from the twilio http request 
	from_body = request.values.get('Body', None)
	#convert the message to lower case
	message_body = from_body.lower()
	#remove +91 from the number
	clean_num = from_num.strip("+1")
	
        #get the value for the guest acceptance
	g_accpt = gi_g.acell('B12').value
        #get the value for the guest decline
	g_decln = gi_g.acell('B13').value
        #get the value if there is zero response 
	g_zero_resp = gi_g.acell('B14').value
        #get the value for the guest acceptance rate(%age of guests accepted)
	g_accept_rate = gi_g.acell('B15').value
        
        #get the value for the meal confirmation
	g_ml_conf = gi_g.acell('B17').value
	#get the value for the meal unconfirmed by the guests
	g_ml_unconf = gi_g.acell('B18').value
	#get the confirmed guest's cell through their number
	g_conf_cell = gi_g.find(str(clean_num))	

	#below information will give us an overview of the meals and beverages
        #get the value for total guests who opted for veg
	g_tot_veg = gi_f.acell('B10').value
	#get the value for total guests who opted for non veg
	g_tot_nonveg = gi_f.acell('B11').value
	#get the value for total no of meals
	g_tot_meal = gi_f.acell('B12').value
	#get the value for total guests who opted for alcohol
	g_tot_alco_req = gi_f.acell('B13').value
	

      	#if the guest responds 'Yes'
	if "yes" in message_body: 
	    #update the status to accepted for that guest
	    gi_g.update_acell('D' + str(g_conf_cell.row), 'Yes')
	    #gi_g.update_acell('D2', 'Yes')
	    #respond to the guest with a message
	    t = resp.message("Thanks for your confirmation.I will reach back to you soon!In the mean time,please visit the link- https://docs.google.com/forms/d/e/1FAIpQLSfTbv7IoHRk7hyRfOdtrGKHGko4OUF2G6gVA0N_8uOgtBsemg/viewform?usp=sf_link  to select your meal preferences") 
	
 	#if the guest responds 'No'
	elif "no" in message_body:
	    #update the status to declined for that guest
	    gi_g.update_acell("F" + str(g_conf_cell.row), 'No')
	    #respond to the guest with a message  
	    resp.message("Oh thats bad!Next time then!") #respond to the user confirming the action 
	
  	#if you want an overview of the event information
	elif "statistics" in from_body.lower(): #return statistics (total guests, food choices list)   
	   resp.message("\nTotal Accepted: " + g_accpt +
	   "\nTotal declined: " + g_decln + "\nTotal no response: " +
	   g_zero_resp + "\nAcceptance rate: " + g_accept_rate)
	
	#if you want an overview of the food information
	elif "food" in message_body.strip():   #respond with the current food totals and the meal choices  

		resp.message("Meals confirmed:" + g_ml_conf + 
		"\nMeals unconfirmed: " + g_ml_unconf +
		"\nMenu Overview:\n" + "Total Veg" +": " +
		g_tot_veg + "\n" + "Total Non Veg" +": " +
		g_tot_nonveg + "\n" + "Total Meal" +": " +
		g_tot_meal + "\n" + "Total Drinks"  +": " +
		g_tot_alco_req)
	
	#tell the guest to respond with a valid keyword
	else:
		resp.message("You sent an invalid keyword...please sent either 'Yes' or 'No' ")
	
	#return string representation of the message
	return str(resp) 

#run the app        
if __name__ == "__main__":
	app.run(debug=True)
