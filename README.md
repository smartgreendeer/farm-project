#create a virtua environment not required
python -m venv weather_env

#activate the virtual environment
weather_env\Scripts\activate


#install required libraries for the project to run
pip install -r requirements.txt

#see results inthe terminal
python weather_test.py


#run the app
python weather.py

The problem want to solve is farmers not being ready for their farms therefore reducing damage control to farm tools and vegetables
My target audience are the young farmers who have not been taught how to farm and using the old ways to take care of their farms
The project can be used to get the soil and agricultural use of that area in case a new person visits or intends to visit a new area
It can also be used to analyze the crypto market for those in trading and investing as I can change the 
 
Project Documentation Template
Project Title: FARM-PROJECT
________________________________________
Table of Contents

________________________________________
Introduction
The project is mainly about how to  use the weather of a location and get the activity to do to your crops or what to grow In that area in case you are planning to move or buy a farm it gives you suggestion on what thrives in that weather conditions.
This is the use of AI in farming as it will help a farmer not to buy land in a place with the current climate change and the crop the user wants to grow maybe affected thus reducing loss and increasing productivity in case you are already in the area it gives you a suggestion on an activity on what to do to your farm on that day based on the weather this prevents the farmer from doing certain activities that may be affected by the weather 
Problem Statement
My project is used to solve the problem of low food production and the change in climate how it affects thus helping the farmer on their productivity in the area they live or want to buy a farm in the area.________________________________________
Solution Overview 
My project gives a solution any time wastage and loss in basic farm tools like when it is raining it will tell you to not spray the farm thus reducing loss of the pesticide and reducing the risk of it being carried to other water sources thus conserving the environment.________________________________________
Target Audience
My target audience are the young farmers who have not been taught on how to farm or are just typically lazy to research on what they are going to do or what they should grow in their farms    in case of inheritance.
________________________________________
Project Setup
Prerequisites
The required libraries are:
1.	The project runs on python version of 3.8 and above
2.	Install the requirements which have been stated in the requirements.txt and they include
I.	Gradio
II.	Asyncio
III.	Asyncflows
IV.	Hhtpx
V.	Os
VI.	dotenv
Installation
To install the app please follow the following steps step by step to get access
First you should visit my repos and clone the farm project repo
# Clone the repository
Git clone https://github.com/smartgreendeer/farm-project

Change the location to where you have stored the repo using the function below
# Navigate to the project directory
cd farm-project

Create a virtual environment to prevent interfering with your python software
Python -m venv weather_env

Next activate the virtual environment
weather_env\Scripts\activate

 
Next you have to install all the dependencies and libraries required for the project to run smoothly (in case of any error install the libraries step by step)
# Install dependencies
Pip install -r requirements.txt

Running the Project
In order to run the project 
Go to you environment in the terminal and key in the following 
Python weather.py 
this will run the app and it will appear as a web server as it has used Gradio UI interface
In case you want to see the functionality you can run 
Python weather_test.py 
This will run in the terminal

________________________________________
Flow Design
Flow Diagram
Include a diagram of your flow. You can use tools like Lucid chart, draw.io, or any other diagramming tool.
Flow Description
The first step is whereby the user input their location or a location they require, here you will be prompted to input the city name cause that is the get functionality of the api were are using this will prevent the user from getting errors
Next step is where by it gets a response which we got the action from the weather.py file this will give us the response from the API about the weather of that location (city) that the user had input
________________________________________
Custom Action
Description
My action is to get the weather information of a certain area thus helping which is an action from the main file this will give a response based on that
Code
Include the code for your custom action. Highlight important sections and provide comments to explain the logic.
async def handle_weather(location):
    api_key = os.getenv('VISUAL_CROSSING_API_KEY')
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"

    params = {
        'unitGroup': 'metric',
        'key': api_key,
        'contentType': 'json'
    }

The logic for this action is to handle weather whereby we get our weather for the timeline which is current, we get the weather from an API server.
Integration
Explain how the custom action integrates into your flow. Provide code snippets or configuration details.
________________________________________
User Interface
UI Design
The design of my user interface is the y using the gradio default template.
The submit button submits whatever the user input in the text area 
The clear button erases every information from the text area and output area thus
The flag button acts as our save button which saves whatever the app has displayed on the output area for future references for the user
 
Gradio Implementation
I used Gradio to create the interface by creating buttons and areas to input text and out text required by the user 

import httpx
import os
import gradio as gr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to handle weather information retrieval using Visual Crossing Weather API
async def handle_weather(location):
    api_key = os.getenv('VISUAL_CROSSING_API_KEY')
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"

    params = {
        'unitGroup': 'metric',
        'key': api_key,
        'contentType': 'json'
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()  # Raise HTTPStatusError for non-2xx responses

            data = response.json()

            # Parse weather data
            weather_description = data.get('description', 'N/A')
            weather_condition = data.get("conditions", "N/A")
            temperature = data.get('temp', {}).get('maxt', 'N/A')
            humidity = data.get('humidity', {}).get('humidity', 'N/A')

            # Determine crop recommendation based on temperature
            if temperature != 'N/A' and temperature is not None:
                temperature = float(temperature)
                if temperature < 25:
                    crop_recommendation = "Recommended crops: Wheat, Barley"
                    activity_suggestion = "Activity suggestion: Plan indoor activities or greenhouse maintenance."
                elif temperature > 40:
                    crop_recommendation = "Recommended crops: Potatoes, Carrots"
                    activity_suggestion = "Activity suggestion: Prepare soil for planting or start seedlings indoors."
                elif temperature > 25:
                    crop_recommendation = "Recommended crops: Corn, Soybeans"
                    activity_suggestion = "Activity suggestion: Plant seeds or transplant seedlings into the garden."
                else:
                    crop_recommendation = "Recommended crops: Tomatoes, Peppers"
                    activity_suggestion = "Activity suggestion: Water plants and monitor for pests or diseases."
            else:
                crop_recommendation = "Temperature data not available."
                activity_suggestion = ""

            # Build weather response
            weather_response = (
                f"Weather in {location}:\n"
                F"Condition: {weather_condition}\n"
                f"Description: {weather_description}\n"
                f"Temperature: {temperature}°C\n"
                f"Humidity: {humidity}%\n\n"
                f"{crop_recommendation}\n\n"
                f"{activity_suggestion}"
            )

            return weather_response

    except httpx.HTTPStatusError as http_err:
        if http_err.response.status_code == 404:
            return f"Weather data not found for {location}. Please check the location name."
        else:
            return f"HTTP error occurred: {http_err}"
    except (httpx.TimeoutException, httpx.RequestError) as err:
        return f"Error fetching weather for {location}: {str(err)}"
    except Exception as e:
        return f"Unknown error occurred: {str(e)}"

# Initialize Gradio interface
iface = gr.Interface(
    fn=handle_weather,  # Function to call on input
    inputs=gr.Textbox(label="Enter Location", placeholder="Enter city name"),
    outputs=gr.Textbox(label="Weather & Recommendations", type="text"),
    title="John Farm Tool",
    description="Enter a location to get current weather information, crop recommendations, and activity suggestions.",
)

# Launch the Gradio interface
if __name__ == "__main__":
    iface.launch(share=True)


________________________________________
How to Use
To runthe project follow the step by step instructions to run it
Step 1: Start the Application
1.	Run the application using the command provide above ensure it’s in your terminal
2.	You can use the ctrl+click to open the url or follow the statement below 
3.	Open your web browser and navigate to the local host URL (usually http://localhost:7860/).
4.	 
Step 2: Interact with the UI
1.	Enter the location you want to get weather information from
2.	Click the submit button to run the flow or just click the enter button.
3.	View the output results in the weather and recommendation text area
4.	 
Step 3: Understanding the Output
1.	The output above the first shows the location that you had input 
2.	The second part shows the conditions for the area that is if it is cloudy or not  and the description of the condition in that area
3.	The rest is the recommended crops and activity to be carried out by the user
4.	The above screenshot is for Nairobi area
5.	

Use Cases
My project can be used by a user who wants to get the weather information for an area or a farmer who wants to see the crop to grow or how to plan their day
________________________________________
Demo Video
This is the link for my demo video of my app in action
Demo Video Link
________________________________________
Conclusion
My project is built for farmers
I achieved to get to know how to integrate ape’s using python language to my code to get real-time information about the weather of a place.
Challenges faced was to get a free API for the weather but with the use or rapid API I got a free API 
________________________________________
Future Work
I plan to add the soil api whereby when user input a location he not only get the weather but the soil and the plants that can survive in that particular weather condition and soil condition thus helping and improving its functionality in a great way
I also plant integrate a llama model that educate the farmer on the area of study omits agricultural area and value and the main crop that is been grown in that area and how they can do to achieve high productivity  for them and discuss the various pests in that area and how to eradicate those pests
________________________________________
References
https://www.visualcrossing.com/weather/weather-data-services#-site used to get my API for the weather real-time information
ChatGpt
Junior Akwa the idea owner
Asyncflows.com
Gradio.app
________________________________________

 
API to stock market and the output will be based the market

