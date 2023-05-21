import React, { useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchBox from './components/SearchBox';
import Header from './components/Header';
import Footer from './components/Footer';
import About from './pages/About';
import Data from './pages/Data';
import Home from './pages/Home';
import Leaderboard from './pages/Leaderboard';
import Players from './pages/Players';


function App() {
  useEffect(() => {
    console.log('working')
  })
  



  return (
    <>
      <div className="App">
         <Header />
         <div className='container'>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/Home" element={<Home />} />
            <Route path="/About" element={<About />} />
            <Route path="/Data" element={<Data />} />
            <Route path="/Leaderboard" element={<Leaderboard />} />
            <Route path="/Players" element={<Players />} />
          </Routes>
         </div>
        <Footer />
       </div>
    </>
      
  );
}

export default App;
