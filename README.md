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
