import SAS from './SAS';
import Southern from './Southern';
import './Layout.css';

const Sites = () => {
  return (
    <>
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
  )
};

export default Sites;