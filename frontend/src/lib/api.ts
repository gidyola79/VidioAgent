import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Attach token from localStorage automatically (for browser environment)
export function setAuthToken(token: string | null) {
    if (token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        try { localStorage.setItem('vidioagent_token', token) } catch {}
    } else {
        delete api.defaults.headers.common['Authorization'];
        try { localStorage.removeItem('vidioagent_token') } catch {}
    }
}

// Initialize from storage when module loads (client-side only)
if (typeof window !== 'undefined') {
    try {
        const t = localStorage.getItem('vidioagent_token')
        if (t) api.defaults.headers.common['Authorization'] = `Bearer ${t}`
    } catch {}
}

export interface AnalyzeRequest {
    name?: string;
    business_type?: string;
    text: string;
}

export interface AnalyzeResponse {
    analysis: string;
}

export const analyzeText = async (data: AnalyzeRequest): Promise<AnalyzeResponse> => {
    const response = await api.post<AnalyzeResponse>('/api/analyze', data);
    return response.data;
};
