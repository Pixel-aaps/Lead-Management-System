// frontend/main.js
const API_BASE = "https://lead-management-system-1-01rf.onrender.com";

class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
    }
}

// path is like "/api/leads" or "/api/leads/1"
async function apiFetch(path, options = {}, auth = true) {
    const headers = options.headers || {};

    if (!(options && options.body instanceof FormData)) {
        headers["Content-Type"] = headers["Content-Type"] || "application/json";
    }

    if (auth) {
        const token = localStorage.getItem("token");
        if (token) headers["Authorization"] = "Bearer " + token;
    }

    const fetchOptions = {
        ...options,
        headers,
        credentials: 'include' // crucial for cross-site cookies
    };

    const res = await fetch(API_BASE + path, fetchOptions);

    let body = null;
    try { body = await res.json(); } catch (e) { body = null; }

    if (res.status === 401) {
        try { localStorage.removeItem('token'); } catch(e){}
        // redirect user to login page
        window.location.href = 'login.html';
        return null;
    }

    if (!res.ok) {
        const err = body || { error: `HTTP ${res.status}` };
        throw new ApiError(err.error || JSON.stringify(err), res.status);
    }
    return body;
}

function apiGet(path) { return apiFetch(path, { method: "GET" }); }
function apiPost(path, data = {}, auth = true) {
    const body = (data instanceof FormData) ? data : JSON.stringify(data);
    const opts = { method: "POST", body };
    return apiFetch(path, opts, auth);
}
function apiPut(path, data) { return apiFetch(path, { method: "PUT", body: JSON.stringify(data) }); }
function apiDelete(path) { return apiFetch(path, { method: "DELETE" }); }

function escapeHtml(s) {
  if (!s) return "";
  return s.replace(/[&<>"']/g, function (m) {
    return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"})[m];
  });
}

function setLoading(isLoading) {
    document.body.classList.toggle('loading', isLoading);
}

function sanitizeInput(str) {
    if (!str) return '';
    return str.replace(/[<>&"']/g, function(c) {
        return {
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '"': '&quot;',
            "'": '&#39;'
        }[c];
    });
}
