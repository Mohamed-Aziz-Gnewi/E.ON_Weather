from flask import Flask, request,make_response,jsonify
import requests

app = Flask(__name__)


#extract the max in temp and the corresponding time
def doubleMax(temp,time):
  return max(temp),time[temp.index(max(temp))]

#Error handeling
@app.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({'error 400':'Bad request'}),400)

@app.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error 404':'Not Found,The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'}),404)

@app.route('/headquarter-weather')
def home():
    args = request.args
    weather={}

    if len(args)==0:
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=51.424&longitude=6.993&current_weather=true").json()
        weather["current_temperature"]=response["current_weather"]["temperature"]
        weather["current_time"]=response["current_weather"]["time"]
        return weather
    if ("include_maximum" not in args.keys()) or ("include_maximum" in args.keys() and args["include_maximum"]!="true"):
        return {'error 400':'Bad request'}
    else:
            response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=51.424&longitude=6.993&current_weather=true&timezone=UTC&hourly=temperature_2m&hourly=apparent_temperature&start_date=2023-01-05&end_date=2023-01-05").json()
            hourly=response["hourly"]
            weather["current_temperature"]=response["current_weather"]["temperature"]
            weather["current_time"]=response["current_weather"]["time"]
            weather["max_temperature"],weather["max_temperature_time"]=doubleMax(hourly['temperature_2m'],hourly["time"])
            weather["max_apparent_temperature"],weather["max_apparent_temperature_time"]=doubleMax(hourly['apparent_temperature'],hourly["time"])
            return weather
            
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)