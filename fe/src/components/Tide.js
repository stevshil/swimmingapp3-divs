import React, { useState, useEffect } from 'react';
// import { format } from 'date-fns';
import './Layout.css';
import './Tide.css';
import { FaSortAmountUp, FaSortAmountDownAlt } from "react-icons/fa";


const Tide = ({theDay}) => {

    let found = 0;
    let tideupdated = 0;
    let info = {};
    const apiurl = process.env.REACT_APP_SERVER_API_URL+'/tide';
    console.log("TIDE URL: "+apiurl+"/tide");
    console.log("Tide DATE: " + theDay);

    const [tide, setTide] = useState([]);
    const [getUpdate, setUpdate] = useState();
    useEffect(() => {
        async function getData() {
            try {
                // let response = await fetch(apiurl+'/tide/'+theDate);
                let response = await fetch(apiurl);
                let data = await response.json();
                setTide(data);
                tideupdated = data.updated;
                console.log("Tide: " + tideupdated);
                setUpdate(tideupdated);
            } catch {

            }
        };

        getData();
    }, [tideupdated]);

    if (tide.length == 0) {
        console.log("Data not found")
    } else {
        console.log("TIDE: " + JSON.stringify(tide.tide[theDay].data, null, 2));
        info = tide.tide[theDay].data.map(item => ({
            type: item[0],
            time: item[1],
            height: item[2]
        }));
        console.log("Tide found: " + info[0].type + " " + info[0].time + " " + info[0].height);
        found = 1;
    };

    if (found === 1) {
        return (
            <>
                <div className='div-table'>
                    <div className='div-table-row'>
                        <div className='div-table-col-left table-header' key="type">
                            Type
                        </div>
                        <div className='div-table-col-left table-header' key="time">
                            Time
                        </div>
                        <div className='div-table-col-left table-header' key="height">
                            Height
                        </div>
                    </div>
                    {info.map((info, index) => (
                        <div className='div-table-row'>
                            <div className='div-table-col-left' key="{index}-type">
                                {/* {info.type} */}
                                {info.type === "High" ? <span className="high">High </span> : <span className="low">Low </span>}
                                {info.type === "High" ? <FaSortAmountUp className="FaSortAmountUp" /> : <FaSortAmountDownAlt className="FaSortAmountDownAlt" />}
                            </div>
                            <div className='div-table-col-left' key="{index}-time">
                                {info.time}
                            </div>
                            <div className='div-table-col-left' key="{index}-height">
                                {info.height}
                            </div>
                        </div>
                    ))}
                </div>
            </>
        );
    }
    if (found === 0) {
        return (
            <>
            <div className='div-table'>
                <div className='div-table-row'>
                    <div className='div-table-col-max' key="waiting">
                        <h3>Waiting for tide data</h3>
                    </div>
                </div>
            </div>
            </>
        )
    }
};

export default Tide;