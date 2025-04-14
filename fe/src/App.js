import React, {useState} from 'react';
import { format } from 'date-fns';
import './App.css';
import Header from './components/Header';
import Home from './Home';
import About from './components/About';
import './components/Tables.css';
import plus from './images/plus3.png';
import minus from './images/minus.png';
import now from './images/Now2.webp';
import home from './images/home.png';
import about from './images/about.png';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

// App currently only deals with 3 day

function App() {

  function setAllDatesNow() {
    setHour(today.getHours());
    setDate(format(today,"yyyy-MM-dd"));
    setDay(0);
  }

  var today = new Date();

  const [hour,setHour] = useState();
  const [theDate,setDate] = useState();
  const [theDay,setDay] = useState();

    if ( hour === undefined ) {
        setHour(today.getHours());
    }

    if ( theDate === undefined ) {
      // setDate(format(today.getDate(),"yyyy-MM-dd"));
      setDate(format(today,"yyyy-MM-dd"));
    }

    if ( theDay === undefined ) {
      setDay(0);
    }

    if ( hour > 23 ) {
      setHour(0);
      if ( theDay < 2 ) {
        setDay(theDay+1);
        var newDate = new Date(theDate);
        newDate.setDate(newDate.getDate() + 1);
        console.log("NEW DATE: "+format(newDate,"yyyy-MM-dd"))
        setDate(format(newDate,"yyyy-MM-dd"));
      }
    }

    if ( hour < 0 ) {
      setHour(23);
      if ( theDay > 0 ) {
        setDay(theDay-1);
        var newDate2 = new Date(theDate);
        newDate2.setDate(newDate2.getDate() - 1);
        setDate(format(newDate2,"yyyy-MM-dd"));
      }
    }


  console.log("APP Date: "+theDate);
  console.log("APP Day: "+theDay);
  console.log("APP hour: "+hour);

  return (
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
            <img src={now} onClick={() => setAllDatesNow()} alt="Now" width="70%" />
            <br/>
            <img src={minus} onClick={() => setHour(hour-1)} alt="Minus" width="75%" />
            <br/>
            <img src={home} onClick={() => window.location.href = "/swim"} alt="Home" width="75%" />
            <br/>
            <img src={about} onClick={() => window.location.href = "/swim/about"} alt="About" width="75%" />
            </div>
            <div>
            <BrowserRouter>
            <Routes>
              <Route path="/swim" element={<Home theDay={theDay} hour={hour} />} />
              <Route path="/about" element={<About />} />
              <Route path="*" element={<Home theDay={theDay} hour={hour} />} />
              </Routes>
            </BrowserRouter>
            </div>
        </div>
      </div>
    </div>
  );
}

export default App;
