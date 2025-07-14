import React, { useState, useEffect } from 'react';
import { AlertTriangle, CheckCircle, Activity, Gauge } from 'lucide-react';

interface SensorData {
  mq2Value: number;
  voltage: number;
  isAlert: boolean;
  ledStatus: {
    green: boolean;
    red: boolean;
  };
}

function App() {
  const [sensorData, setSensorData] = useState<SensorData>({
    mq2Value: 0,
    voltage: 0,
    isAlert: false,
    ledStatus: {
      green: false,
      red: false
    }
  });

  useEffect(() => {
    const fetchSensorData = async () => {
      try {
        const response = await fetch('http://192.168.160.233/api/sensor');
        const data = await response.json();
        setSensorData(data);
      } catch (error) {
        console.error('Error fetching sensor data:', error);
      }
    };

    const interval = setInterval(fetchSensorData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="p-6">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Gas Detection</h1>
              <p className="text-sm text-gray-500">Real-time monitoring system</p>
            </div>
            <Activity className="w-6 h-6 text-blue-500 animate-pulse" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-sm text-gray-500">Gas Level (ADC)</p>
                  <p className="text-3xl font-bold text-gray-800">{sensorData.mq2Value}</p>
                </div>
                <Gauge className="w-8 h-8 text-blue-500" />
              </div>
              <div className="relative pt-1">
                <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-200">
                  <div
                    style={{ width: `${(sensorData.mq2Value / 1023) * 100}%` }}
                    className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center transition-all duration-500 ${
                      sensorData.isAlert ? 'bg-red-500' : 'bg-green-500'
                    }`}
                  />
                </div>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Voltage</p>
                  <p className="text-3xl font-bold text-gray-800">
                    {sensorData.voltage.toFixed(2)}V
                  </p>
                </div>
                <div className="w-8 h-8 text-yellow-500">⚡</div>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center">
              {sensorData.isAlert ? (
                <>
                  <AlertTriangle className="w-8 h-8 text-red-500 mr-3" />
                  <div>
                    <p className="text-red-500 font-bold">Gas Leakage Detected!</p>
                    <p className="text-sm text-gray-500">
                      Gas concentration exceeds safe threshold
                    </p>
                  </div>
                </>
              ) : (
                <>
                  <CheckCircle className="w-8 h-8 text-green-500 mr-3" />
                  <div>
                    <p className="text-green-500 font-bold">Air Quality Normal</p>
                    <p className="text-sm text-gray-500">
                      Gas levels within safe range
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>

          <div className="mt-6 text-center text-sm text-gray-500">
            Last updated: {new Date().toLocaleTimeString()}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;