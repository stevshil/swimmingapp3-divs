import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import SAS from './SAS';
import Southern from './Southern';
import './Layout.css';

interface AlertsProps {
    serverURL: string;
}

const Alerts = ({serverURL}: AlertsProps) => {
    const apiurl = serverURL + "/sewage.json";

    const [alerts, setAlerts] = useState<any[]>([]);
    const [statusCode, setStatusCode] = useState<number | null>(null);
    const [lastModified, setLastModified] = useState<string | null>(null);

    // ------------------------------------------------------------
    // Parse "DD/MM/YYYY HH:mm:ss GMT" into a Date (local time)
    // ------------------------------------------------------------
    function parseGMTDate(raw) {
        if (!raw) return null;

        const parts = raw.split(" ");
        if (parts.length < 2) return null;

        const datePart = parts[0]; // "DD/MM/YYYY"
        const timePart = parts[1]; // "HH:mm:ss"

        const [dd, mm, yyyy] = datePart.split("/").map(Number);
        const [hh, min, ss] = timePart.split(":").map(Number);

        if (
            Number.isNaN(dd) || Number.isNaN(mm) || Number.isNaN(yyyy) ||
            Number.isNaN(hh) || Number.isNaN(min) || Number.isNaN(ss)
        ) {
            return null;
        }

        return new Date(yyyy, mm - 1, dd, hh, min, ss);
    }

    // ------------------------------------------------------------
    // Time formatting helper (GMT-aware)
    // ------------------------------------------------------------
    function formatTimeGMTAware(raw) {
        if (!raw) return "N/A";

        const parts = raw.split(" ");
        if (parts.length < 2) return "N/A";

        const timePart = parts[1]; // HH:mm:ss
        const [hh, mm] = timePart.split(":");

        const offset = new Date().getTimezoneOffset();
        const isBST = offset === -60;

        let hour = Number(hh);
        if (Number.isNaN(hour)) return "N/A";

        if (isBST) hour = (hour + 1) % 24;

        return `${hour.toString().padStart(2, "0")}:${mm}`;
    }

    // ------------------------------------------------------------
    // Fetch sewage data
    // ------------------------------------------------------------
    useEffect(() => {
        async function getData() {
            try {
                const response = await fetch(apiurl);

                const lm = response.headers.get("Last-Modified");
                setLastModified(lm)
                console.log("Last-Modified:", lm);

                const data = await response.json();
                setAlerts(data);
                setStatusCode(response.status);
            } catch {
                setStatusCode(500);
            }
        }
        getData();
    }, [apiurl]);

    // ------------------------------------------------------------
    // Determine state
    // ------------------------------------------------------------
    const noData = statusCode === 200 && alerts.length === 0;
    const hasData = statusCode === 200 && alerts.length > 0;
    const lastModifiedDate = lastModified ? new Date(lastModified) : null;

    // ------------------------------------------------------------
    // Render: No alerts
    // ------------------------------------------------------------
    if (noData) {
        return (
            <>
                <div className='div-table white'>
                    <div className='div-table-row white'>
                        <div className='div-table-col-max white'>
                            <div className='Alert'>&#128169; &ensp; Alerts &ensp; &#128169;</div>
                            <div>Last updated: {lastModifiedDate ? format(lastModifiedDate, 'dd/MM/yyyy HH:mm') : 'N/A'}</div>
                        </div>
                    </div>
                </div>

                <div className='div-table'>
                    <div className='div-table-row'>
                        <div className='div-table-col-max white'>
                            <h4>No Alerts</h4>
                        </div>
                    </div>
                </div>
                <div className='div-table white'>
                    <div className='div-table-row white'>
                        <div className='div-table-col-max white'>
                            <h3>Check sewage status:</h3>
                            <Southern />
                            <br />
                            <SAS />
                            <br />
                        </div>
                    </div>
                </div>
            </>
        );
    }

    // ------------------------------------------------------------
    // Render: API not responding
    // ------------------------------------------------------------
    if (hasData && alerts[0].activity === "API not responding") {
        return (
            <div className='div-table white'>
                <div className='div-table-row white'>
                    <div className='div-table-col-max white'>
                        <h3>Check sewage status:</h3>
                        <Southern />
                        <br />
                        <SAS />
                        <br />
                    </div>
                </div>
            </div>
        );
    }

    // ------------------------------------------------------------
    // Render: Alerts available
    // ------------------------------------------------------------
    if (hasData) {
        return (
            <>
                <div className='div-table white'>
                    <div className='div-table-row white'>
                        <div className='div-table-col-max white'>
                            <div className='Alert'>&#128169; &ensp; Alerts &ensp; &#128169;</div>
                            {/* <div>Last updated: {format(new Date(), 'dd/MM/yyyy HH:mm')}</div> */}
                            <div>Last updated: {lastModifiedDate ? format(lastModifiedDate, 'dd/MM/yyyy HH:mm') : 'N/A'}</div>
                        </div>
                    </div>
                </div>

                <div className='div-table'>
                    {alerts.map((record, index) => {
                        const startRaw = record["Start"];
                        const endRaw = record["End"];

                        const startDateObj = parseGMTDate(startRaw);
                        const endDateObj = parseGMTDate(endRaw);

                        const startedTime = formatTimeGMTAware(startRaw);
                        const stoppedTime = formatTimeGMTAware(endRaw);

                        // ------------------------------------------------------------
                        // Date From/To formatting
                        // ------------------------------------------------------------
                        let dateDisplay = "N/A";

                        if (startDateObj && endDateObj) {
                            const sameDay =
                                startDateObj.getFullYear() === endDateObj.getFullYear() &&
                                startDateObj.getMonth() === endDateObj.getMonth() &&
                                startDateObj.getDate() === endDateObj.getDate();

                            if (sameDay) {
                                dateDisplay = format(startDateObj, "dd/MM/yyyy");
                            } else {
                                const startDay = format(startDateObj, "dd");
                                const endDateFormatted = format(endDateObj, "dd/MM/yyyy");
                                dateDisplay = `${startDay} - ${endDateFormatted}`;
                            }
                        }

                        return (
                            <div>
                            <table>
                                <tbody>
                                    <tr><td className='div-table-col-left'>Date From/To</td><td className='div-table-col-right'>{dateDisplay}</td></tr>
                                    <tr><td className='div-table-col-left'>Duration</td><td className='div-table-col-right'>{record["TotalDuration"]}</td></tr>
                                    <tr><td className='div-table-col-left'>Started</td><td className='div-table-col-right'>{startedTime}</td></tr>
                                    <tr><td className='div-table-col-left'>Stopped</td><td className='div-table-col-right'>{stoppedTime}</td></tr>
                                    <tr><td className='div-table-col-left'>Status</td><td className='div-table-col-right'>{record["Status"]}</td></tr>
                                    <tr><td className='div-table-col-left'>Impact</td><td className='div-table-col-right'>{record["ImpactStatus"]}</td></tr>
                                    <tr><td className='div-table-col-left'>Outlet(s)</td><td className='div-table-col-right'><span className="outlet">{record["AffectedOutfalls"]}</span></td></tr>
                                </tbody>
                            </table>
                            <hr />
                            </div>
                        );
                    })}
                </div>
                <div className='div-table white'>
                    <div className='div-table-row white'>
                        <div className='div-table-col-max white'>
                            <h3>Check sewage status:</h3>
                            <Southern />
                            <br />
                            <SAS />
                            <br />
                        </div>
                    </div>
                </div>
            </>
        );
    }

    // ------------------------------------------------------------
    // Render: Waiting
    // ------------------------------------------------------------
    return <h3>Waiting for alert data</h3>;
};

export default Alerts;
