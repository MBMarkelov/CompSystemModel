import React, { useState } from 'react';

const liquids = {
  glycerin: { name: 'Глицерин', rho: 1260, mu: 1.5},
  kerosene: { name: 'Керосин', rho: 800, mu: 0.015}
};

const materials = {
  steel: { name: 'Сталь', rho: 7850},
  tin: { name: 'Олово', rho: 7300}
};

const Lab2 = () => {
  const [radius, setRadius] = useState(0.13);
  const [selectedLiquid, setSelectedLiquid] = useState('kerosene');
  const [selectedMaterial, setSelectedMaterial] = useState('tin');
  const [imageUrl, setImageUrl] = useState('');
  const [modalOpen, setModalOpen] = useState(false);

  const handleCalculate = async () => {
    const liquid = liquids[selectedLiquid];
    const material = materials[selectedMaterial];

    try {
      const response = await fetch('http://localhost:8000/L2/PyTasks/ball/drop_ball/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          r: radius,
          g: 9.81,
          rho_ball: material.rho,
          rho_liquid: liquid.rho,
          mu: liquid.mu,
          h: 10.5
        })
      });

      const data = await response.json();
      if (data.image_url) {
        setImageUrl(data.image_url.image_url);
        setModalOpen(true);
      }
    } catch (error) {
      console.error('Ошибка при получении изображения:', error);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100vh', backgroundColor: '#e0f2fe' }}>
      <div style={{ width: '300px', padding: '20px', backgroundColor: 'white', borderRadius: '10px', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)', textAlign: 'center' }}>
        <h2>Настройки погружения</h2>
        <label>
          Размер шарика (r):
          <input type="number" value={radius} onChange={(e) => setRadius(parseFloat(e.target.value))} step="0.001" min="0.001" max="5.000" style={{ width: '100%', marginTop: '5px' }} />
        </label>
        <label>
          Выберите жидкость:
          <select value={selectedLiquid} onChange={(e) => setSelectedLiquid(e.target.value)} style={{ width: '100%', marginTop: '5px' }}>
            {Object.entries(liquids).map(([key, liquid]) => (
              <option key={key} value={key}>{liquid.name}</option>
            ))}
          </select>
        </label>
        <label>
          Выберите материал шарика:
          <select value={selectedMaterial} onChange={(e) => setSelectedMaterial(e.target.value)} style={{ width: '100%', marginTop: '5px' }}>
            {Object.entries(materials).map(([key, material]) => (
              <option key={key} value={key}>{material.name}</option>
            ))}
          </select>
        </label>
        <button onClick={handleCalculate} style={{ marginTop: '10px', padding: '10px', width: '100%', backgroundColor: '#007bff', color: 'white', borderRadius: '5px', cursor: 'pointer' }}>Посчитать</button>
      </div>

      {modalOpen && (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', position: 'relative' }}>
            <img key={imageUrl}
              src={imageUrl}
              alt="Результат погружения"
              style={{ maxWidth: '3500px', maxHeight: '500vh', borderRadius: '5px' }}/>
          </div>
          <button onClick={() => setModalOpen(false)} style={{ position: 'absolute', top: '10px', right: '10px', cursor: 'pointer', border: 'none', background: 'none', fontSize: '18px' }}>ЗАКРЫТЬ</button>

        </div>
      )}
    </div>
  );
};

export default Lab2;
