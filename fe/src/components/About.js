import './About.css';
import plus from '../images/plus3.png';
import minus from '../images/minus.png';
import now from '../images/Now2.webp';

const About = () => {
    return (
        <>
        <div>
        <h1>About</h1>
        <p>This app was written by Steve Shilling of TPS Services Ltd.</p>
        <p>It's aim was to develop a web API and front end for obtaining useful data for local swimmers in the Folkestone area in Kent.</p>
        <p>The application is on GitHub, and you can make changes and distribute freely, but cannot charge for this application without the expressed permission of TPS Services Ltd.</p>
        <h1>Using the App</h1>
        <p>The app is fairly simple.  You can change the hour of the forecast by clicking the <img src={plus} alt="Plus" width="8%" /> or <img src={minus} alt="Minus" width="8%" /> buttons and will go forward to 3 days.</p>
        <p>The <img src={now} alt="Now" width="8%" /> button will set your time back to the current time</p>
        <p>Note that the big temperature is the current temperature.</p>
        <p>Temperature for the selected hour will be to the right of the big temperature.</p>
        <p>All other data is displayed based on the selected hour or day.</p>
        </div>
        </>
    );
}

export default About;