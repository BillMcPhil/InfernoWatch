import logo from './logo.svg';
import './App.css';
import axios from 'axios';

import { useState, useEffect } from 'react';


function App() {
  const [backend, setBackend] = useState("");

  useEffect(() => {
    const fetchData = async () => {
          try {
              const response = await axios.get("http://127.0.0.1:8080/api/test");
              setBackend(response.data);
          } catch (err) {
            
          }
      };

      fetchData();
  }, []); 

  return (
    <>
          {backend.data}
    </>
  );
}

export default App;

