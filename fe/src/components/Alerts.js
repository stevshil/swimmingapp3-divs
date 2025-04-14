import React, {useState, useEffect} from 'react';
import { format,parseISO } from 'date-fns';
import './Layout.css';

const Alerts = () => {
    let found = 0;

    const apiurl = process.env.REACT_APP_SERVER_API_URL+"/sewage";

    const [alerts, setAlerts] = useState([]);
    const [alertState, setAlertState] = useState([]);
    useEffect(() => {
        async function getData() {
            try {
            let response = await fetch(apiurl);
            let data = await response.json();
            let res = response.status
            console.log(data)
            setAlerts(data);
            setAlertState(res)
            } catch {
            
            }
        };

        getData();
    }, [alertState, apiurl]);

    let clientTZ="";
    let alertsTime="";

    try {
        if (! alerts.Alerts.length > 0) {
            console.log("Data not found, alert state: "+alertState)
            if (alertState === 200) {
                found = 2;
                clientTZ = Number(((new Date()).toString()).split("+")[1].split("")[1]);
                alertsTime = new Date(alerts.updated)
                alertsTime.setHours(alertsTime.getHours()+clientTZ)
            }
        } else {
            // console.log("Data found")
            console.log(alerts)
            found = 1;
            // clientTZ = (new Date()).getTimezoneOffset();
            clientTZ = Number(((new Date()).toString()).split("+")[1].split("")[1]);
            alertsTime = new Date(alerts.updated)
            alertsTime.setHours(alertsTime.getHours()+clientTZ)
            // console.log("TZ: "+clientTZ)
            // console.log("Alerts Time: "+alertsTime)
        }
    } catch {
        console.log("No alerts")
    }

    if ( found === 2 ) {
        return (
            <>
            <div className='div-table white'>
                <div className='div-table-row white'>
                    <div className='div-table-col-max white'>
                        <div className='Alert'>&#128169; &ensp; Alerts &ensp; &#128169;</div>
                        <div>Last updated: {format(alertsTime,'dd/MM/yyyy HH:mm')}</div>
                    </div>
                </div>
            </div>
            <div className='div-table'>
                <div className='div-table-row'>
                    <div className='div-table-col-max white'>
                        <h4>No Alerts</h4>
                        <p>
                            {/* Last release: {format(alerts.lastoutfall.lastoutfall,'dd/MM/yyyy')}<br/> */}
                            Last release: {alerts.lastoutfall?.lastoutfall ? format(parseISO(alerts.lastoutfall.lastoutfall), 'dd/MM/yyyy') : "N/A"}<br />
                            {alerts.lastoutfall.lastoutfalllocation}
                        </p>
                    </div>
                </div>
            </div>
            </>
        )
    }
    if ( found === 1 ) {
        return (
            <>
                <div className='div-table white'>
                    <div className='div-table-row white'>
                        <div className='div-table-col-max white'>
                            <div className='Alert'>&#128169; &ensp; Alerts &ensp; &#128169;</div>
                            <div>Last updated: {format(alertsTime,'dd/MM/yyyy HH:mm')}</div>
                        </div>
                    </div>
                </div>
                <div className='div-table'>
                    {alerts.Alerts.map((data) => ( 
                    <div className='div-table-row'>
                        <div className='div-table-col-left'>
                            Location<br/>
                            Started<br/>
                            Stopped<br/>
                            Activity<br/>
                            Impact<br/>
                            Outlet
                            <hr/>
                        </div>
                        <div className='div-table-col-right'>
                            {data.bathingSite}<br/>
                            {format(data.eventStart, 'dd/MM/yyyy HH:mm')}<br/>
                            {format(data.eventStop, 'dd/MM/yyyy HH:mm')}<br/>
                            {data.activity}<br/>
                            {data.impact}<br/>
                            <span className="outlet">{data.outlet}</span>
                            <hr/>
                        </div>
                    </div>
                    ))}
                </div>
            </>
        );
    }
    if ( found === 0 ) {
        return (
            <h3>Waiting for alert data</h3>
        )
      }
};

export default Alerts;