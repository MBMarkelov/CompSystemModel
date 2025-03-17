import React, { useState } from 'react';

function App() {
  const [goldenData, setGoldenData] = useState(null);
  const [dichotomyData, setdichotomyData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGoldenSelection = async () => {
    setLoading(true);
    setError(null);
    setGoldenData(null);
    setdichotomyData(null);
    
    try {
      const response = await fetch('http://localhost:8000/L3/golden_selection/');
      if (!response.ok) {
        throw new Error('Ошибка при получении данных золотого сечения');
      }
      const data = await response.json();
      setGoldenData(data);
    } catch (err) {
      setError(err);
    }
    setLoading(false);
  };

  const handledichotomy = async () => {
    setLoading(true);
    setError(null);
    setGoldenData(null);
    setdichotomyData(null);
    
    try {
      const response = await fetch('http://localhost:8000/L3/dichotomy_selection/');
      if (!response.ok) {
        throw new Error('Ошибка при получении данных метода Дихотомии');
      }
      const data = await response.json();
      setdichotomyData(data);
    } catch (err) {
      setError(err);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Оптимизационные методы</h1>
      <div style={{ marginBottom: '20px' }}>
        <button onClick={handleGoldenSelection} style={{ marginRight: '10px' }}>
          Золотое сечение
        </button>
        <button onClick={handledichotomy}>
          Метод Дихотомии
        </button>
      </div>

      {loading && <p>Загрузка...</p>}
      {error && <p style={{ color: 'red' }}>Ошибка: {error.message}</p>}

      {goldenData && (
        <div>
          <h2>Результаты метода золотого сечения</h2>
          <p>Локальный минимум: x = {goldenData.min.x}, y = {goldenData.min.y}</p>
          <p>Локальный максимум: x = {goldenData.max.x}, y = {goldenData.max.y}</p>
          <p>Интервал экстремумов: {goldenData.extrema_interval}</p>
          {goldenData.image && (
            <img
              src={`data:image/png;base64,${goldenData.image}`}
              alt="График золотого сечения"
              style={{ maxWidth: '100%', marginTop: '10px' }}
            />
          )}
        </div>
      )}

      {dichotomyData && (
        <div>
          <h2>Результаты метода Дихотомии</h2>
          <p>Локальный минимум: x = {dichotomyData.min.x}, y = {dichotomyData.min.y}</p>
          <p>Локальный максимум: x = {dichotomyData.max.x}, y = {dichotomyData.max.y}</p>
          <ul>
          {dichotomyData.extrema_points.map((x, index) => (
                <li key={index}>
                    Экстремум: x = {x}
                </li>
            ))}
                    </ul>
          {dichotomyData.image && (
                <img
                    src={`data:image/png;base64,${dichotomyData.image}`}
                    alt="График метода Дихотомии"
                    style={{ maxWidth: '100%', marginTop: '10px' }}
                />
            )}
        </div>
      )}
    </div>
  );
}

export default App;
