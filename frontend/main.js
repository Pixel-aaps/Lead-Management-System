const API_BASE = "https://lead-management-system-1-01rf.onrender.com"; 

class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
    }
}

async function apiFetch(path, options = {}, auth = true) {
    const headers = options.headers || {};

    if (!(options && options.body instanceof FormData)) {
        headers["Content-Type"] = headers["Content-Type"] || "application/json";
    }

    if (auth) {
        const token = localStorage.getItem("token");
        if (token) {
            headers["Authorization"] = "Bearer " + token;
        }
    }

    // include cookies
    const fetchOptions = {
        ...options,
        headers,
        credentials: 'include' // <- sends cookies (and receives Set-Cookie)
    };

    const res = await fetch(API_BASE + path, fetchOptions);

    let body = null;
    try { body = await res.json(); } catch (e) { body = null; }

    // If 401: redirect to login
    if (res.status === 401) {
        try { localStorage.removeItem('token'); } catch(e){}
        window.location.href = '/login';
        return null;
    }

    if (!res.ok) {
        return body || { error: `HTTP ${res.status}` };
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

// Loading state helpers 
function setLoading(isLoading) {
    document.body.classList.toggle('loading', isLoading);
}

// sanitize input 
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
