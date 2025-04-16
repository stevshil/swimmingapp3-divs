import React, {useState, useEffect} from 'react';
import { format, parseISO } from 'date-fns';
import Sea from './Sea';
import './Layout.css';
import './Tables.css';

const Weather = ({theHour,theDay}) => {

    let found = 0;

    const apiurl = process.env.REACT_APP_SERVER_API_URL+'/weather';
    console.log("APIURL: "+apiurl);

    const [weather, setWeather] = useState([]);
    const [timeData, setTimeData] = useState([]);
    // const [found, setFound] = useState(0);
    useEffect(() => {
        async function getData() {
            try {
                let response = await fetch(apiurl);
                let data = await response.json();
                setWeather(data);
            } catch {
                
            }
        };

        async function getTime() {
            try {
                let response = await fetch(apiurl+'/');
                let time_data = await response.json();
                setTimeData(time_data);
            } catch {

            }
        }

        getData();
    }, [timeData,apiurl]);

    if (!weather.current) {
        found = 0;
        console.log("Data not found "+found)
    } else {
        // console.log("Data found")
        console.log("Found: "+found)
        console.log(weather)
        // setFound(1);
        found = 1;
    }

    if ( found === 1 ) {
    return (
    <>
        <div className='div-table white'>
            <div className='div-table-row'>
                <div className='div-table-col-max white'>
                {/* Data Update: {format(weather.current.last_updated, "yyyy-MM-dd HH:mm")}<br/> */}
                Data Update: {weather.current.last_updated? format(parseISO(weather.current.last_updated), 'dd/MM/yyyy HH:mm') : "N/A"}<br />
                </div>
            </div>
        </div>
        <div className='div-table'>
            <div className='div-table-row'>
                <div className='div-table-col'>
                    <span className='curtemp'>{weather.current.temp_c.toFixed(1)}&#8451;</span>
                </div>
                <div className="div-table-col alignright">
                    Min: {weather.forecast.forecastday[theDay].day.mintemp_c} &#8451;
                    <br />
                    Max: {weather.forecast.forecastday[theDay].day.maxtemp_c} &#8451;
                    <br />
                    {weather.forecast.forecastday[theDay].hour[theHour].time? format(parseISO(weather.forecast.forecastday[theDay].hour[theHour].time), 'HH:mm') : "N/A"}: {weather.forecast.forecastday[theDay].hour[theHour].temp_c.toFixed(1)} &#8451;
                </div>
            </div>
            <div className='div-table-row'>
                <div className='feelslike'>
                    Feels Like: {weather.current.feelslike_c} &#8451;
                </div>
            </div>
            <Sea the_hour={theHour} />
        </div>

        <div className='div-table rain'>
            <div className='div-table-row'>
                <div className='div-table-col rainpic'>
                    <img src={weather.current.condition.icon} alt={weather.current.condition.icon} /><br/>
                    {weather.current.condition.text}
                </div>
                <div className='div-table-col rain alignright'>
                    Rain: {weather.forecast.forecastday[theDay].hour[theHour].precip_mm} mm<br/>
                    Rain Now: {weather.forecast.forecastday[theDay].hour[theHour].chance_of_rain} %<br/>
                    Snow Now: {weather.forecast.forecastday[theDay].hour[theHour].chance_of_snow} %<br/>
                    Rain Today: {weather.forecast.forecastday[theDay].day.daily_chance_of_rain} %<br/>
                    Snow Today: {weather.forecast.forecastday[theDay].day.daily_chance_of_snow} %
                </div>
            </div>
        </div>
        <div className='div-table'>
            <div className='div-table-row'>
                <div className='div-table-col alignright'>
                    Wind: 
                </div>
                <div className='div-table-col alignright'>
                {weather.forecast.forecastday[theDay].hour[theHour].wind_mph} mph
                </div>
            </div>
            <div className='div-table-row'>
                <div className='div-table-col alignright'>
                    Direction: 
                </div>
                <div className='div-table-col alignright'>
                {weather.forecast.forecastday[theDay].hour[theHour].wind_dir}
                </div>
            </div>
            <div className='div-table-row'>
                <div className='div-table-col alignright'>
                    Gusts:
                </div>
                <div className='div-table-col alignright'>
                {weather.forecast.forecastday[theDay].hour[theHour].gust_mph} mph
                </div>
            </div>
        </div>
        <div className='div-table white'>
            <div className='div-table-row'>
                <div className='div-table-col-max white'>
                {/* Forecast Time: {format(weather.forecast.forecastday[theDay].hour[theHour].time,"yyyy-MM-dd HH:mm")}<br/> */}
                Forecast Time: {weather.forecast.forecastday[theDay].hour[theHour].time? format(parseISO(weather.forecast.forecastday[theDay].hour[theHour].time), 'dd/MM/yyyy HH:mm') : "N/A"}<br />
                </div>
            </div>
        </div>
    </>
    )
    }
    if ( found === 0 ) {
        return (
            <h3>Waiting for weather data</h3>
        )
    }
};

export default Weather;