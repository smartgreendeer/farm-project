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
            temperature = data.get('temp', {}).get('maxt', '22')
            humidity = data.get('humidity', {}).get('humidity', '59')

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
