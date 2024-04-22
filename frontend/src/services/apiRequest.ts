import { NextRequest } from 'next/server';

const API_URL = 'http://localhost:8000';

export interface IRequest {
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: any;
  contentType?: string;
}

export default async function MakeRequest({
  endpoint,
  method,
  data,
  contentType = 'application/json',
}: IRequest) {
  let headers: HeadersInit = {
    'Content-Type': contentType,
  };
  let body;
  if (data instanceof FormData) {
    headers = {};
    body = data;
  } else if (data) {
    body = JSON.stringify(data);
  }

  const request = new NextRequest(`${API_URL}${endpoint}`, {
    method,
    headers,
    body,
  });

  const response = await fetch(request);
  let responseBody;
  try {
    responseBody = await response.json();
  } catch (error) {
    console.log('Error parsing response body');
  }
  if (response.ok) {
    return responseBody;
  }
}
