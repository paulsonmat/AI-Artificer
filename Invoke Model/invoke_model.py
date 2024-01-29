
import gradio as gr
import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


def process_inputs(Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area):  
    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
	# Request data goes here
	# The example below assumes JSON formatting which may be updated
	# depending on the format your endpoint expects.
	# More information can be found here:
	# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data =  {
	  "Inputs": {
	    "data": [
	      {
	        "Gender": Gender,
	        "Married":Married,
	        "Dependents": str(Dependents),
	        "Education": Education,
	        "Self_Employed": Self_Employed,
	        "ApplicantIncome": ApplicantIncome,
	        "CoapplicantIncome": CoapplicantIncome,
	        "LoanAmount": LoanAmount,
	        "Loan_Amount_Term": Loan_Amount_Term,
	        "Credit_History": Credit_History,
	        "Property_Area": Property_Area
	      }
	    ]
	  },
	  "GlobalParameters": {
	    "method": "predict"
	  }
	}
    print(data)
    body = str.encode(json.dumps(data))
    url = 'http://b57edeec-eae2-4bd4-bd7d-740ec9fcc52e.eastus.azurecontainer.io/score'
	
    headers = {'Content-Type':'application/json'}
    req = urllib.request.Request(url, body, headers)
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
	    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
    return {"Eligible for the loan" if json.loads(result)['Results'][0] == True else "Chance of approval is low" }
  
iface = gr.Interface(  
    fn=process_inputs,   
    inputs=[  
        gr.Dropdown(["Male", "Female"],label="Gender"),  
        gr.Radio(["Yes", "No"], label="Married"),  
        gr.Number(label="Dependents"),  
        gr.Textbox(label="Education"),  
        gr.Radio(["Yes", "No"], label="Self_Employed"),  
        gr.Number(label="ApplicantIncome"),  
        gr.Number(label="CoapplicantIncome"),  
        gr.Number(label="LoanAmount"),  
        gr.Number(label="Loan_Amount_Term"),  
        gr.Number(label="Credit_History"),  
        gr.Textbox(label="Property_Area")  
    ],   
    outputs=gr.Json(),  
    title="Loan Application",  
    description="Enter your details and submit"
)  
  
iface.launch()  