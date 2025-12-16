import React, { useState } from 'react';
import { transactions } from '../services/api';

const TransactionForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    type: 'expense',
    amount: '',
    category: '',
    description: '',
    date: new Date().toISOString().split('T')[0]
  });

  const categories = {
    expense: ['Food', 'Transportation', 'Entertainment', 'Bills', 'Shopping', 'Other'],
    income: ['Salary', 'Freelance', 'Investment', 'Other']
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await transactions.create({
        ...formData,
        amount: parseFloat(formData.amount)
      });
      setFormData({
        type: 'expense',
        amount: '',
        category: '',
        description: '',
        date: new Date().toISOString().split('T')[0]
      });
      onSuccess?.();
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-4">Add Transaction</h3>
      
      <div className="space-y-4">
        <select
          value={formData.type}
          onChange={(e) => setFormData({...formData, type: e.target.value, category: ''})}
          className="w-full p-2 border rounded"
        >
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>

        <input
          type="number"
          step="0.01"
          placeholder="Amount"
          value={formData.amount}
          onChange={(e) => setFormData({...formData, amount: e.target.value})}
          className="w-full p-2 border rounded"
          required
        />

        <select
          value={formData.category}
          onChange={(e) => setFormData({...formData, category: e.target.value})}
          className="w-full p-2 border rounded"
          required
        >
          <option value="">Select category</option>
          {categories[formData.type].map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>

        <input
          type="date"
          value={formData.date}
          onChange={(e) => setFormData({...formData, date: e.target.value})}
          className="w-full p-2 border rounded"
          required
        />

        <input
          type="text"
          placeholder="Description (optional)"
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          className="w-full p-2 border rounded"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          Add Transaction
        </button>
      </div>
    </form>
  );
};

export default TransactionForm;