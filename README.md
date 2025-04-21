<<<<<<< HEAD
# LivestockManager
=======
# Livestock Manager

A comprehensive Django-based livestock management system designed for farmers and agricultural businesses to streamline operations, enhance productivity, and drive growth.

## Features

- **Animal Management**: Track and manage your livestock with detailed records
- **Health Tracking**: Monitor health status with predictive analytics
- **Analytics Dashboard**: Data-driven insights for breeding, nutrition, and management
- **Ownership Transfer**: Manage ownership transfers between users
- **User Management**: Admin controls for user verification and account management
- **Support System**: Built-in support ticketing system for users

## Technology Stack

- Django 5.0.4
- TailwindCSS for responsive UI
- SQLite database (development)
- FontAwesome icons

## Deployment on Vercel

This application is configured for deployment on Vercel.

### Prerequisites

1. A [Vercel](https://vercel.com) account
2. Vercel CLI installed: `npm install -g vercel`
3. Git repository setup

### Deployment Steps

1. Clone this repository:
   ```
   git clone <repository-url>
   cd livestock-manager
   ```

2. Login to Vercel CLI:
   ```
   vercel login
   ```

3. Deploy to Vercel:
   ```
   vercel
   ```

4. For production deployments:
   ```
   vercel --prod
   ```

### Important Environment Variables

Configure these in your Vercel project settings:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'False' in production
- `VERCEL_ENV`: Set to 'production' for deployed environments

## Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Start the development server: `python manage.py runserver`

## Project Structure

```
livestock-manager/
├── livestock/                # Main application
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   ├── forms.py              # Form definitions
│   ├── models.py             # Database models
│   ├── urls.py               # URL routing
│   └── views.py              # View controllers
├── livestock_manager/        # Project settings
├── media/                    # User-uploaded files
├── static/                   # Static assets
├── vercel.json               # Vercel deployment configuration
└── requirements.txt          # Python dependencies
```

## License

Copyright © 2024 Livestock Manager. All rights reserved.
>>>>>>> 0b1bd4c (Initial commit or any appropriate message)
