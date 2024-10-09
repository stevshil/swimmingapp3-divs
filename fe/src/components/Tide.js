import React, {useState, useEffect} from 'react';
import { format } from 'date-fns';
import './Layout.css';

const Tide = ({theDate}) => {

    let found = 0;
    const apiurl = process.env.REACT_APP_SERVER_API_URL;
    console.log("TIDE URL: "+apiurl+"/tide/"+theDate);

    const [tide, setTide] = useState([]);
    const [getUpdate, setUpdate] = useState(theDate);
    useEffect(() => {
        async function getData() {
            try {
                let response = await fetch(apiurl+'/tide/'+theDate);
                let data = await response.json();
                setTide(data);
                setUpdate(theDate);
            } catch {
                
            }
        };

        getData();
    }, [theDate]);

    if (tide.length == 0) {
        console.log("Data not found")
    } else {
        console.log("TIDE: "+tide[0].time);
        found = 1;
    }

    if ( found === 1 ) {
        return (
            <>
                <div className='div-table'>
                {tide.map(info => (
                    <div className='div-table-row'>
                        <div className='div-table-col'>
                            {info.type}:
                        </div>
                        <div className='div-table-col'>
                            {((info.time).split("T")[1]).replace(/:[0-9][0-9]\+.*$/,"")}
                        </div>
                    </div>
                    ))}
                </div>
            </>
        );
    }
    if ( found === 0 ) {
        return (
            <div className='div-table'>
                <div className='div-table-row'>
                <div className='div-table-col-max'>
                    <h3>Waiting for tide data</h3>
                </div>
                </div>
            </div>
        )
    }
};

export default Tide;