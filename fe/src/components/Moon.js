import React, {useEffect, useState} from 'react';
import moonrise from '../images/moonrise.svg';
import moonset from '../images/moonset.svg';
import './Layout.css';

const Moon = ({theDay}) => {
    let found = 0;
    console.log("theDay: "+theDay);

    const apiurl = process.env.REACT_APP_SERVER_API_URL;

    const [moon, setMoon] = useState([]);
    useEffect(() => {
        async function getData() {
            try {
                let response = await fetch(apiurl+'/weather');
                let data = await response.json();
                setMoon(data);
            } catch {
                
            }
        };

        getData();
    }, []);

    let moon_illum = "";
    let moonpic="swim/images/moon_phases/"

    if (!moon.current || moon.forecast.forecastday.length == 0) {
        console.log("Data not found")
    } else {
        // console.log("Data found")
        console.log("MOON LENGTH: "+moon.forecast.forecastday.length)
        moon_illum = moon.forecast.forecastday[theDay].astro.moon_illumination;
        found = 1;

        // Calculate moon phase picture
        var moon_lum=Math.round(moon_illum*.12)
        var pic_phase = moon.forecast.forecastday[theDay].astro.moon_phase.substring(0,6).toLowerCase();
        var pic_phase_full = ""
        if ( moon_lum === 0 ) {
            moon_lum=""
            pic_phase="new"
        }
        if (pic_phase.includes("full")) {
            pic_phase="full"
            moon_lum=""
        } else if (pic_phase.includes("new")) {
            pic_phase="new"
            moon_lum=""
        } else if (pic_phase_full.includes("Last Q")) {
            pic_phase="waning"
        } else if (pic_phase_full.includes("First Q")) {
            pic_phase="waxing"
        }

        moonpic=moonpic+pic_phase+moon_lum+"Z.jpg"

    }

    if ( found === 1 ) {
        return (
            <>
                <div className='div-table moon'>
                    <div className='div-table-row moon'>
                    <img src={moonpic} alt={moonpic} width="60px" valign='middle' />
                    </div>
                    <div className='div-table-row moon'>
                    <div className='div-table-col moon'>
                        Phase:
                    </div>
                    <div className='div-table-col moon'>
                        {moon.forecast.forecastday[theDay].astro.moon_phase}
                    </div>
                    </div>
                    <div className='div-table-row moon'>
                    <div className='div-table-col moon'>
                        Percent:
                    </div>
                    <div className='div-table-col moon'>
                        {moon_illum} %
                    </div>
                    </div>
                    <div className='div-table-row moon'>
                    <div className='div-table-col moon'>
                        <img src={moonrise} width="60px" alt="Rise" />
                    </div>
                    <div className='div-table-col moon'>
                        <img src={moonset} width="60px" alt="Set" />
                    </div>
                    </div>
                    <div className='div-table-row moon'>
                    <div className='div-table-col moon'>
                        {moon.forecast.forecastday[theDay].astro.moonrise}
                    </div>
                    <div className='div-table-col moon'>
                        {moon.forecast.forecastday[theDay].astro.moonset}
                    </div>
                    </div>
                    <div className='div-table-row moon'>&nbsp;</div>
                </div>
            </>
        );
    }
    if ( found === 0 ) {
        return (
            <h3>Waiting for moon data</h3>
        )
    }
};

export default Moon;