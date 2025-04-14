import Weather from './components/Weather';
import Tide from './components/Tide';
import Alerts from './components/Alerts';
import SAS from './components/SAS';
import Moon from './components/Moon';
import Sun from './components/Sun';


const Home = ({theDay, hour}) => {

    return (
        <>
        <Weather theHour={hour} theDay={theDay} />
        <Tide theDay={theDay} />
        <Alerts />
        <SAS />
        <Moon theDay={theDay} />
        <Sun theDay={theDay} />
        </>
    )
}

export default Home;