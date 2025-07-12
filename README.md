# EchoLog

EchoLog is a simple, modern homelab journal web app. It lets you document what you did each day, search and filter your entries, and review your homelab journey over time.

## Features
- Add daily journal entries with multi-line support
- Edit and delete entries using a sleek modal interface
- Search and filter entries by keyword or date
- Pagination for easy browsing of large journals
- Optional login for privacy (can be enabled via environment variable)
- Beautiful dark mode UI powered by Tailwind CSS
- MySQL database backend for reliable storage

## How it works
- Entries are saved to a MySQL database, with connection details set via environment variables
- The web interface is built with Flask and styled with Tailwind CSS
- All features are accessible from a single, responsive page
- You can enable login protection and set credentials using environment variables

## Docs
For more information, see the [Docs](https://echolog.jdbnet.co.uk).

## Environment Variables

```
MYSQL_HOST=10.10.2.27
MYSQL_USER=echolog
MYSQL_PASSWORD=gHH0&nGWK!@8Y5
MYSQL_DATABASE=echolog
SECRET_KEY=bgSNcrA0gZiRX9LbZmminf2LItEXeo
TZ=Europe/London
LOGIN_ENABLED=true
LOGIN_USERNAME=jamie
LOGIN_PASSWORD=jamieB223
```