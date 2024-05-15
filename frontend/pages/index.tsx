import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Index() {
  const [param, setParam] = useState('Loading');
  const [timestamp, setTimestamp] = useState('Loading');
  const [value, setValue] = useState('Loading');

  const [devices, setDevices] = useState({});
  

  const [chartData, setChartData] = useState({ datasets: [] });
  const [chartOptions, setChartOptions] = useState({});
   
   useEffect(() => {
    // Fetch devices data
    fetch('http://localhost:8080/api/devices')
      .then(response => response.json())
      .then(data => {
        setDevices(data);
      })
      .catch(error => {
        console.error('Error fetching devices:', error);
      });
  }, []);


  useEffect(() => {

    

    const fetchDataByDevice = async () => {
      const data = {
        device_name: 'device.foo',
        parameter_name: '',
        start_time: '2024-03-5',
        end_time: '2024-05-8',
      };

      try {
        const response = await fetch('http://localhost:8080/api/visualize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        setParam(responseData.parameter_numeric.parameters);
        setTimestamp(responseData.parameter_numeric.timestamp);
        setValue(responseData.parameter_numeric.values);

        setChartData({
          labels: responseData.parameter_numeric.timestamp,
          datasets: [
            {
              label: responseData.parameter_numeric.parameters,
              data: responseData.parameter_numeric.values,
              borderColor: 'rgb(53, 162, 235)',
              backgroundColor: 'rgb(53, 162, 235)',
            },
          ],
        });

        setChartOptions({
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: data.device_name,
            },
          },
          maintainAspectRatio: false,
          responsive: true,
        });
      } catch (error) {
        console.error('Error:', error);
      }
    };

    /*fetchData();*/
    const fetchDataParam = async () => {
      const data = {
        device_name: 'device.foo',
        parameter_name: 'parameter.foo',
        start_time: '2024-03-07 11:20:00.0',
        end_time: '2024-03-07 11:29:00.0',
        token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiamVmZiIsImV4cCI6MTcxNTcwOTA1MH0.gQrnLsr0THWFiGpgdS6AZ0u3cgKpRD5O3RfmyOjqI6g"
      };

      try {
        const response = await fetch('http://localhost:8080/api/visualize', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
       /* setParam(responseData.parameter_numeric.parameters);
        setTimestamp(responseData.parameter_numeric.timestamp);
        setValue(responseData.parameter_numeric.values);*/

        setChartData({
          labels: responseData.timestamp,
          datasets: [
            {
              label: "parameter value",
              data: responseData.values,
              borderColor: 'rgb(53, 162, 235)',
              backgroundColor: 'rgb(53, 162, 235)',
            },
          ],
        });

        setChartOptions({
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text:  data.device_name + " > " +responseData.parameter_name,
            },
          },
          maintainAspectRatio: false,
          responsive: true,
        });
      } catch (error) {
        console.error('Error:', error);
      }
    };


   fetchDataParam();
  }, []);

    // Event handler for option selection
    const handleOptionChange = (event) => {
    // Get the selected option value
    const selectedOption = event.target.value;

    // For demonstration purposes, let's assume the selected options are "option1" and "option2"
    const option1 = 'option1'; // Replace with actual value from first select element
    const option2 = selectedOption; // Use the selected value from the second select element

    // Call fetchData function with selected options
    fetchData(option1, option2);
  };
  return (
    <div className="body">
      <div className="select-container">
        {/* First select element */}
        <select>
          <option value="option1">device.foo</option>
          <option value="option2">Option 2</option>
          <option value="option3">Option 3</option>
        </select>

        {/* Second select element with event listener */}
        <select onChange={handleOptionChange}>
          <option value="option1">parameter.foo</option>
          <option value="option2">Option 2</option>
          <option value="option3">Option 3</option>
        </select>
      </div>
      <div className="chart-container">
        {/* Placeholder for chart */}
        
        {/* You can replace this with your actual chart component using the fetched data */}
        <div>
            <Bar data={chartData} options={chartOptions} />
        </div>
      </div>
    </div>
   
  );
}

export default Index;
 