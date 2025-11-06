Developed a Lead Management System using HTML, TailwindCSS, and Vanilla JS for frontend, with a Flask REST API backend and SQLite/MySQL database. The system supports login authentication (JWT), adding, updating, deleting, and searching leads with pagination.”

## Key Features Implemented:
- User authentication with JWT.
- CRUD operations for leads (Add, Edit, Delete, View).
- Pagination and search across all pages.
- Frontend validation and backend validation using custom validators.
- Duplicate lead handling implemented on backend.
- Responsive UI with TailwindCSS.


##  Technical Considerations / Decisions:

- Search queries are passed to backend to ensure results include all pages, not just the current page.
- API error handling is implemented for invalid data, duplicates, and server errors.
- Frontend communicates securely with backend via token authorization in headers.
