// frontend/main.js
const API_BASE = window.location.origin;  // Auto: https://lead-management-system-1-01rf.onrender.com on Render

/**
 * Custom API Error with status code
 */
class ApiError extends Error {
  constructor(message, status, rawResponse = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.rawResponse = rawResponse;
  }
}

/**
 * Core fetch wrapper with auth, JSON/FormData support, and error handling
 */
async function apiFetch(path, options = {}, auth = true) {
  const headers = { ...options.headers };
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
  }

  if (auth) {
    const token = localStorage.getItem("token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  const fetchOptions = {
    ...options,
    headers,
    credentials: "include",
  };

  if (options.body && !(options.body instanceof FormData)) {
    fetchOptions.body = JSON.stringify(options.body);
  }

  let response;
  try {
    response = await fetch(API_BASE + path, fetchOptions);
  } catch (err) {
    console.error("Network error:", err);
    throw new ApiError("Network error. Please check your connection.", 0);
  }

  let data = null;
  let rawText = "";
  try {
    rawText = await response.text();
    if (rawText) {
      data = JSON.parse(rawText);
    }
  } catch (jsonError) {
    console.warn("Response is not valid JSON:", rawText.substring(0, 200));
  }

  if (response.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "login.html";
    return null;
  }

  if (!response.ok) {
    const errorMessage =
      (data && (data.error || data.message)) ||
      `HTTP ${response.status} ${response.statusText}`;
    console.error(`API Error [${response.status}]:`, {
      url: API_BASE + path,
      method: options.method || "GET",
      response: rawText.substring(0, 500),
    });
    throw new ApiError(errorMessage, response.status, rawText);
  }

  return data;
}

// HTTP Method Helpers
function apiGet(path, auth = true) {
  return apiFetch(path, { method: "GET" }, auth);
}
function apiPost(path, data = {}, auth = true) {
  return apiFetch(
    path,
    {
      method: "POST",
      body: data,
    },
    auth
  );
}
function apiPut(path, data, auth = true) {
  return apiFetch(
    path,
    {
      method: "PUT",
      body: data,
    },
    auth
  );
}
function apiDelete(path, auth = true) {
  return apiFetch(path, { method: "DELETE" }, auth);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  if (text == null) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Export globally
window.apiGet = apiGet;
window.apiPost = apiPost;
window.apiPut = apiPut;
window.apiDelete = apiDelete;
window.escapeHtml = escapeHtml;