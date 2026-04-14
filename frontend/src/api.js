const runtimeHost = window.location.hostname;
const runtimeBaseUrl = `${window.location.protocol}//${runtimeHost}:5000`;
const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL;

function resolveApiBaseUrl() {
  if (!configuredBaseUrl) {
    return runtimeBaseUrl;
  }

  try {
    const parsed = new URL(configuredBaseUrl);
    const configuredHost = parsed.hostname;
    const isConfiguredLoopback = configuredHost === "127.0.0.1" || configuredHost === "localhost";
    const isRuntimeLoopback = runtimeHost === "127.0.0.1" || runtimeHost === "localhost";

    if (isConfiguredLoopback && !isRuntimeLoopback) {
      return runtimeBaseUrl;
    }
    return configuredBaseUrl;
  } catch {
    return runtimeBaseUrl;
  }
}

export const API_BASE_URL = resolveApiBaseUrl();

async function parseResponse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message =
      data.error ||
      data.message ||
      `Request failed (${response.status} ${response.statusText})`;
    throw new Error(message);
  }
  return data;
}

export async function registerUser(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return parseResponse(response);
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(`Cannot reach backend at ${API_BASE_URL}. Start Flask server and verify CORS.`);
    }
    throw error;
  }
}

export async function loginUser(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return parseResponse(response);
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(`Cannot reach backend at ${API_BASE_URL}. Start Flask server and verify CORS.`);
    }
    throw error;
  }
}

export async function getCurrentUser(token) {
  const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return parseResponse(response);
}

export async function logoutUser(token) {
  const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return parseResponse(response);
}
