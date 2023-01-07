from flask import Flask, request,make_response,jsonify
import requests

app = Flask(__name__)


#extract the max in temp and the corresponding time
def doubleMax(temp,time):
  return max(temp),time[temp.index(max(temp))]

#Error handeling
@app.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({'error':'Bad request'}),400)

@app.route('/headquarter-weather')
def home():
    args = request.args
    weather={}

    if len(args)==0:
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=51.424&longitude=6.993&current_weather=true")
        res=response.json()
        weather["current_temperature"]=res["current_weather"]["temperature"]
        weather["current_time"]=res["current_weather"]["time"]
        return weather
    if ("include_maximum" not in args.keys()) or ("include_maximum" in args.keys() and args["include_maximum"]!="true"):
        return {'error':'Bad request'}
    else:
            response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=51.424&longitude=6.993&current_weather=true&timezone=UTC&hourly=temperature_2m&hourly=apparent_temperature&start_date=2023-01-05&end_date=2023-01-05")
            res=response.json()
            hourly=res["hourly"]
            weather["current_temperature"]=res["current_weather"]["temperature"]
            weather["current_time"]=res["current_weather"]["time"]
            weather["max_temperature"],weather["max_temperature_time"]=doubleMax(hourly['temperature_2m'],hourly["time"])
            weather["max_apparent_temperature"],weather["max_apparent_temperature_time"]=doubleMax(hourly['apparent_temperature'],hourly["time"])
            return weather
            
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)