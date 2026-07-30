import React, {useState} from 'react';
import { format } from 'date-fns';
import './App.css';
import Header from './components/Header';
import Weather from './components/Weather';
import Tide from './components/Tide';
import Alerts from './components/Alerts';
// import SAS from './components/SAS';
// import Southern from './components/Southern';
import Moon from './components/Moon';
import Sun from './components/Sun';
import './components/Tables.css';
import plus from './images/plus3.png';
import minus from './images/minus.png';
import now from './images/Now2.webp';

// App currently only deals with 3 day

const App = () => {

  function setAllDatesNow() {
    setHour(today.getHours());
    setDate(format(today,"yyyy-MM-dd"));
    setDay(0);
  }

  const today = new Date();

  const [hour,setHour] = useState<number>(today.getHours());
  const [theDate,setDate] = useState<string>(format(today,"yyyy-MM-dd"));
  const [theDay,setDay] = useState<number>(0);

    if ( hour > 23 ) {
      setHour(0);
      if ( theDay < 2 ) {
        setDay(theDay+1);
        const newDate = new Date(theDate);
        newDate.setDate(newDate.getDate() + 1);
        console.log("NEW DATE: "+format(newDate,"yyyy-MM-dd"))
        setDate(format(newDate,"yyyy-MM-dd"));
      }
    }

    if ( hour < 0 ) {
      setHour(23);
      if ( theDay > 0 ) {
        setDay(theDay-1);
        const newDate2 = new Date(theDate);
        newDate2.setDate(newDate2.getDate() - 1);
        setDate(format(newDate2,"yyyy-MM-dd"));
      }
    }


  console.log("APP Date: "+theDate);
  console.log("APP Day: "+theDay);
  console.log("APP hour: "+hour);

  return (
    <>
    <div className="App">
      <div className="home-container">
        <header>
          <title>Folkestone Weather</title>
          <meta property="og:title" content="Folkestone Weather" />
        </header>
        <Header />
        <div className="main-row">
        <div className="controls">
            <h4>Change Hour</h4>
            <img src={plus} onClick={() => setHour(hour+1)} alt="Plus" width="75%" />
            <br/>
            <img src={now} onClick={() => setAllDatesNow()} alt="Now" width="75%" />
            <br/>
            <img src={minus} onClick={() => setHour(hour-1)} alt="Minus" width="75%" />
            <br/>
            &nbsp;
            </div>
          <div>
            <Weather theHour={hour} theDay={theDay} serverURL={import.meta.env.VITE_SERVER_API_URL} />
            <Tide theDay={theDay} serverURL={import.meta.env.VITE_SERVER_API_URL} />
            <Alerts serverURL={import.meta.env.VITE_SEWAGE_URL} />
            <Moon theDay={theDay} serverURL={import.meta.env.VITE_SERVER_API_URL} />
            <Sun theDay={theDay} serverURL={import.meta.env.VITE_SERVER_API_URL} />
          </div>
        </div>
      </div>
    </div>
    </>
  );
}

export default App;
