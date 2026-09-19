import React, { useEffect, useState } from 'react';
import ResultsTable from '../components/ResultsTable';

const ResultsPage = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const rawData = localStorage.getItem('scrapedData');
    console.log("Raw Data from LocalStorage:", rawData); // Log raw data from localStorage
  
    if (rawData) {
      try {
        const parsed = JSON.parse(rawData);
        console.log("Parsed Data in ResultsPage:", parsed);  // Log to verify data structure
        setData(parsed);
      } catch (error) {
        console.error("Error parsing JSON data:", error);
        setData([]);  // Set empty data if JSON parsing fails
      }
    }
  }, []);
  

  return (
    <div>
      <h2>Scraped Results</h2>
      <ResultsTable data={data} />
    </div>
  );
};

export default ResultsPage;
