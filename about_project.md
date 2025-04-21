# Livestock Manager Project Documentation

## Project Overview

Livestock Manager is a comprehensive web application designed for farmers and agricultural businesses to streamline livestock management operations. The platform provides an end-to-end solution for tracking animals, monitoring health records, managing ownership transfers, and generating analytical insights to optimize farming operations.

## Basic Information

- **Project Name:** Livestock Manager
- **Author:** Prashant Kumar
- **Author Website:** [https://enally.in](https://enally.in)
- **Live Demo:** [https://livestock-manager.onrender.com](https://livestock-manager.onrender.com)

## Purpose & Target Audience

This application is tailored for:
- Individual farmers managing their livestock
- Agricultural enterprises with large-scale operations
- Veterinarians tracking animal health records
- Agricultural businesses seeking data-driven insights
- Farm administrators requiring ownership and transfer management

## Technology Stack

### Backend Framework
- **Django 5.0.4**: Python web framework providing robust ORM, authentication system, and admin interface
- **Python 3.x**: Core programming language

### Frontend Technologies
- **HTML/CSS/JavaScript**: For creating responsive UI components
- **TailwindCSS**: Utility-first CSS framework for designing responsive interfaces
- **Font Awesome**: Icon library for enhanced UI elements
- **AOS (Animate On Scroll)**: Library for scroll-based animations

### Database
- **SQLite** (Development): Lightweight database for local development
- Support for PostgreSQL in production environments through dj-database-url

### Authentication & Security
- Django's built-in authentication system
- CSRF protection for form submissions

### Deployment & Infrastructure
- Configured for deployment on **Vercel**
- Environment variable management with **python-decouple** and **django-environ**
- **Gunicorn** as the WSGI HTTP server

### Media Handling
- **Pillow**: Python Imaging Library for processing image uploads

## Core Features

### 1. Animal Management System
- Comprehensive digital records for each animal
- Species, breed, and lineage tracking
- Custom species and breed creation
- Gender tracking
- Tag number generation and management
- Photo uploads and visual documentation

### 2. Health Record Management
- Vaccination schedules and records
- Treatment documentation
- Regular health checkups
- Medication tracking
- Cost tracking for health interventions
- Follow-up scheduling
- Timeline view of animal health history

### 3. Ownership Management
- Digital ownership records
- Secure transfer mechanism between users
- Transfer request validation
- Transfer history tracking
- Ownership verification

### 4. User Profile & Customization
- User profile management
- Business information configuration
- Notification preferences
- Interface customization options
- Profile picture uploads

### 5. Administration & User Management
- User verification system
- User activity monitoring
- Status management (enable/disable accounts)
- User statistics tracking

### 6. Support System
- Built-in support ticketing system
- Request categorization
- Status tracking for support requests

### 7. Analytics & Insights
- Production analytics
- Health status monitoring
- Feed efficiency metrics
- Performance tracking
- Real-time activity monitoring

## Application Architecture

### Project Structure
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

### Key Models (Inferred from Templates)
1. **User/Owner**: Extended user model with profile information
2. **Animal**: Core animal data including species, breed, tag number
3. **HealthRecord**: Animal health interventions and history
4. **OwnershipTransfer**: Records of animal ownership changes
5. **SupportRequest**: User support tickets and inquiries

## UI/UX Design Approach

The application features a modern, professional design with these characteristics:

### Design Elements
- **Color Scheme**: Primarily amber/gold with complementary blue accents, symbolizing agriculture and professionalism
- **Typography**: Clean, readable fonts with clear hierarchy
- **Components**: Card-based design with rounded corners and subtle shadows
- **Visual Effects**: 
  - Glassmorphism (frosted glass effect) for cards and containers
  - Subtle animations using AOS library
  - Gradient backgrounds

### User Experience Features
- **Responsive Design**: Works across mobile and desktop devices
- **Progressive Disclosure**: Complex functionalities revealed progressively
- **Animated Transitions**: Smooth state changes and loading effects
- **Toast Notifications**: Non-intrusive feedback system
- **Dual View Options**: Table and card views for data representation

### Dashboard
- Interactive charts and visualizations
- Status cards with key metrics
- Recent activity feed
- Performance indicators

## Pricing Model

The application appears to follow a tiered pricing strategy:
1. **Basic Plan** (₹3,999/year): For small farms, up to 100 animals
2. **Standard Plan** (₹8,999/year): For growing operations, up to 500 animals
3. **Premium Plan** (₹15,999/year): For large enterprises, unlimited animals

Each tier offers progressively more advanced features, analytics capabilities, and support options.

## Deployment Instructions

### Local Development
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Start the development server: `python manage.py runserver`

### Vercel Deployment
1. Clone the repository: `git clone <repository-url>`
2. Login to Vercel CLI: `vercel login`
3. Deploy to Vercel: `vercel`
4. For production: `vercel --prod`

### Render.com Deployment
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Select the Python runtime
4. Set the build command: `sh ./build_render.sh`
5. Set the start command: `gunicorn livestockManager.wsgi:application`
6. Add required environment variables

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'False' in production
- `VERCEL_ENV`: Set to 'production' for Vercel environments
- `RENDER`: Set to 'True' for Render environments
- `DATABASE_URL`: Connection string for the database (if using external database)

## Security Considerations

- Django's built-in security features are leveraged
- CSRF protection is implemented for forms
- Environment variables are used for sensitive configuration
- Password hashing through Django's authentication system

## Performance Optimization

- Static files are collected and served efficiently
- AOS animations are optimized for performance
- Lazy loading techniques for media elements
- Django template inheritance to minimize redundancy

## Conclusion

Livestock Manager represents a comprehensive solution for the agricultural sector, combining modern web technologies with domain-specific functionality. Its carefully designed user interface, robust backend architecture, and scalable feature set make it suitable for livestock operations of all sizes.

## Credits

Developed by Prashant Kumar, as indicated in the footer credit section.

---

*This documentation was generated based on codebase analysis and may not capture all aspects of the application. Refer to specific code files for detailed implementation details.*
