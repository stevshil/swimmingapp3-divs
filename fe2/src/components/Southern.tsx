import React, {Component} from 'react';
import './Layout.css';

class Southern extends Component {
    render() {
        // const url = "https://riversandseaswatch.southernwater.co.uk/?map=live-updates&zoom=12"
        const url = "https://riversandseaswatch.southernwater.co.uk/?map=live-updates&selectedFeature=109794%3AOutfall&zoom=12"
        // const url = "https://experience.arcgis.com/experience/e9a1db8d193d4cd582d550285a3aeb44#widget_1582=active_datasource_id:dataSource_29,center:622883.8082198033%2C136540.32519658137%2C27700,scale:99393.58355433522/"
        
        return (
            <>
                <div align='center' id="sas">
                    <button className="threeD-button" onClick={() => window.open(url)}>Southern Water</button>
                </div>
            </>
        );
    };
};

export default Southern;