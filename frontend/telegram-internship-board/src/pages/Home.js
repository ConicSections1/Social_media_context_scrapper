import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Home = () => {
  const [phone, setPhone] = useState('');
  const navigate = useNavigate();

  const handleScrape = async () => {
    try {
      const response = await axios.post('http://localhost:8000/scrape_without_code', { phone });
      console.log("Scrape response:", response.data);
  
      if (response.status === 200) {
        const allMessages = [];
  
        // Flatten all messages from each channel
        response.data.result.forEach(channel => {
          if (channel.messages) {
            allMessages.push(...channel.messages);
          }
        });
  
        localStorage.setItem('scrapedData', JSON.stringify(allMessages));
        navigate('/results');
      } else if (response.status === 401) {
        const code = prompt('Enter the security code sent to your phone:');
        const authResponse = await axios.post('http://localhost:8000/scrape', { phone, security_code: code });
  
        const allMessages = [];
        authResponse.data.result.forEach(channel => {
          if (channel.messages) {
            allMessages.push(...channel.messages);
          }
        });
  
        localStorage.setItem('scrapedData', JSON.stringify(allMessages));
        navigate('/results');
      }
    } catch (err) {
      console.error('Error:', err);
      alert('Scraping failed. Check phone/code.');
    }
  };
  
  

  return (
    <div>
      <h2>Telegram Scraper</h2>
      <input
        type="text"
        placeholder="Enter phone number"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />
      <button onClick={handleScrape}>Start Scraping</button>
    </div>
  );
};

export default Home;
