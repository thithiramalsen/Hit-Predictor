import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const api = {
  getModels: async () => {
    const response = await axios.get(`${API_URL}/models`);
    return response.data.models;
  },

  uploadImage: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_URL}/ocr`, formData);
    return response.data.features;
  },

  predict: async (modelId, features) => {
    const formData = new FormData();
    formData.append('model_id', modelId);
    formData.append('features', JSON.stringify(features));

    // Debug: log payload before sending
    console.debug('api.js: predict payload', { modelId, features });

    try {
      const response = await axios.post(`${API_URL}/predict`, formData);
      // Debug: log response
      console.debug('api.js: predict response', response.data);
      return response.data.prediction;
    } catch (error) {
      // Debug: log error
      console.error('api.js: predict error', error);
      throw error;
    }
  },

  getEvaluationMetrics: async () => {
    const response = await axios.get('/evaluation_metrics.json');
    return response.data;
  },

  getStatus: async () => {
    const response = await axios.get(`${API_URL}/status`);
    return response.data;
  }
};