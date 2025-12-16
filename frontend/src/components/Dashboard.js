import React, { useState, useEffect } from 'react';
import { transactions } from '../services/api';

const Dashboard = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await transactions.getDashboard();
      setData(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const removeIncomeItem = async (category) => {
    try {
      await transactions.deleteByCategory('income', category);
      fetchData(); // Re-fetch to get updated calculations
    } catch (error) {
      console.error('Error deleting income:', error);
    }
  };

  if (!data) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-green-100 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-green-800">Income</h3>
          <p className="text-2xl font-bold text-green-600">₹{data.income}</p>
        </div>
        <div className="bg-red-100 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-red-800">Expenses</h3>
          <p className="text-2xl font-bold text-red-600">₹{data.expenses}</p>
        </div>
        <div className="bg-blue-100 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-800">Savings</h3>
          <p className="text-2xl font-bold text-blue-600">₹{data.savings}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-xl font-semibold mb-4">Income</h3>
        {data.category_breakdown_income.map(item => (
          <div key={item.category} className="flex justify-between items-center py-2">
            <span>{item.category}</span>
            <span>₹{item.amount}</span>
            <button 
              className="ml-2 text-gray-500 hover:text-red-500" 
              onClick={() => removeIncomeItem(item.category)}
              aria-label="Remove item"
            >
              X
            </button>
          </div>
        ))}
      </div>
       <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-xl font-semibold mb-4">Expenses Breakdown</h3>
        {data.category_breakdown.map(item => (
          <div key={item.category} className="flex justify-between py-2">
            <span>{item.category}</span>
            <span>₹{item.amount}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;