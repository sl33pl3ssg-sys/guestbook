services:
  - type: web
    name: guestbook
    env: python
    startCommand: gunicorn guestbook:app
    plan: free