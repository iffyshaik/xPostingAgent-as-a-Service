// frontend/src/api/index.ts

import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'; // fallback

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Automatically add JWT from localStorage
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface SubmitTopicPayload {
  original_topic: string;
  content_type: 'thread' | 'article';
  auto_post?: boolean;
  thread_tweet_count?: number;
  max_article_length?: number;
  include_source_citations?: boolean;
  citation_count?: number;
  platform: 'x' | 'typefully';
}

export const submitTopic = async (payload: SubmitTopicPayload) => {
  const response = await api.post('/content/requests', payload);
  return response.data;
};

export default api;
