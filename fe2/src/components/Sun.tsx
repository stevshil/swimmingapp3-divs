import React, {useEffect, useState} from 'react';
import './Layout.css';
import sunrise from '../images/sunrise.svg';
import sunset from '../images/sunset.svg';
import sunfull from '../images/sun.svg';

interface SunProps {
    theDay: number;
    serverURL: string;
}

interface SunData {
    forecast?: {
        forecastday?: Array<{
            astro?: {
                sunrise?: string;
                sunset?: string;
            };
        }>;
    };
}

const Sun = ({ theDay, serverURL }: SunProps) => {
    const [sun, setSun] = useState<SunData | null>(null);

    useEffect(() => {
        async function getData() {
            try {
                const response = await fetch(`${serverURL}/weather`);
                const data = await response.json();
                setSun(data);
            } catch {
                setSun(null);
            }
        }

        getData();
    }, [serverURL]);

    const dayForecast = sun?.forecast?.forecastday?.[theDay];
    const sunriseTime = dayForecast?.astro?.sunrise ?? '';
    const sunsetTime = dayForecast?.astro?.sunset ?? '';

    if (!dayForecast) {
        return <h3>Waiting for sun data</h3>;
    }

    return (
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
                    {sunriseTime}
                </div>
                <div className='div-table-col sun'>
                    {sunsetTime}
                </div>
            </div>
            <div className='div-table-row sun'>&nbsp;</div>
        </div>
    );
};


export default Sun;