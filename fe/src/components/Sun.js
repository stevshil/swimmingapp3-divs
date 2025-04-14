import React, {useEffect, useState} from 'react';
import './Layout.css';
import sunrise from '../images/sunrise.svg';
import sunset from '../images/sunset.svg';
import sunfull from '../images/sun.svg';

const Sun = ({theDay}) => {

    let found = 0;

    const apiurl = process.env.REACT_APP_SERVER_API_URL+'/weather';

    const [sun, setSun] = useState([]);
    useEffect(() => {
        async function getData() {
            try {
                let response = await fetch(apiurl);
                let data = await response.json();
                setSun(data);
            } catch {
                
            }
        };

        getData();
    }, [apiurl]);

    if (!sun.current) {
        console.log("Data not found")
    } else {
        // console.log("Data found")
        console.log(sun)
        found = 1;
    }

    if ( found === 1 ) {
        return (
            <>
                <div className='div-table sun'>
                    <div className='div-table-row sun'>
                        <img src={sunfull} alt="Sun" width="80px" />
                    </div>
                    <div className='div-table-row sun'>
                        <div className='div-table-col sun'>
                        <img src={sunrise} width="70px" alt="Rise" />
                        </div>
                        <div className='div-table-col sun'>
                        <img src={sunset} width="70px" alt="Rise" />
                        </div>
                    </div>
                    <div className='div-table-row sun'>
                        <div className='div-table-col sun'>
                        {sun.forecast.forecastday[theDay].astro.sunrise}
                        </div>
                        <div className='div-table-col sun'>
                        {sun.forecast.forecastday[theDay].astro.sunset}
                        </div>
                    </div>
                    <div className='div-table-row sun'>&nbsp;</div>
                    </div>
            </>
        );
    };

    if ( found === 0 ) {
        return (
            <h3>Waiting for sun data</h3>
        )
    }
};


export default Sun;