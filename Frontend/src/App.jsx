

import { BrowserRouter,  Route,  Routes } from 'react-router-dom';
import NavBar from './components/navBar/NavBar';
import Home from './pages/Home';
import Vehicules from './components/vehicules/Vehicules';
import DeliveryPoint from './components/deliveryPoint/DeliveryPoint';
import Deposit from './components/deposit/Deposit';
import Demand from './components/demand/Demand';
import OptimizarPage from './components/maps/OptimizarPage';

const App = () => {
  return (
    <div>
     <BrowserRouter>
      <NavBar />
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="deposit" element={<Deposit />} />
          <Route path="vehicules" element={<Vehicules />} /> 
          <Route path="delivery-point" element={<DeliveryPoint />} /> 
          <Route path="demand" element={<Demand />} /> 
          <Route path="/optimizar" element={<OptimizarPage />} />
        </Routes>

    </BrowserRouter>
    </div>
  )
}

export default App

