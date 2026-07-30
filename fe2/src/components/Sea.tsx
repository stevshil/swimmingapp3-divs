import React, {useState, useEffect} from 'react';
import './Layout.css';

const Sea = ({the_hour, serverURL}: {the_hour: number, serverURL: string}) => {

    const apiurl = serverURL + '/sea';

    const [sea, setSea] = useState([]);
    useEffect(() => {
        async function getData() {
            try {
                let response = await fetch(apiurl);
                let data = await response.json();
                setSea(data);
            } catch {
                
            }
        };

        getData();
    }, [apiurl]);

    let waterTemp=0;
    // let the_hour = new Date();
    // the_hour = the_hour.getHours();

    if (!sea.hours) {
        console.log("Data not found")
    } else {
        // console.log("Data found")
        console.log(sea + ": "+the_hour)
        let wtemp=Object.values(sea.hours[the_hour].waterTemperature)
        // waterTemp=((tmp.meto+tmp.metno+tmp.sg)/3).toFixed(1)
        waterTemp = (wtemp.reduce((sum, tmp) => sum + tmp, 0) /wtemp.length).toFixed(1);
    }
   
    return (
        <>
            <div className='div-table-row'>
                <div className='seatemp'>
                    Sea: {waterTemp}&#8451;
                </div>
            </div>
        </>
    );
};

export default Sea;