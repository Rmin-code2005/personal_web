# Personal Website Portfolio 🚀

## English

### Overview
A full-stack personal portfolio website built with **Django** (backend) and **React** (frontend). This project showcases projects, resume, skills, and portfolio information with a modern, responsive design.

### Features
- ✨ **Modern UI/UX** - Responsive design for all devices
- 📱 **Portfolio Showcase** - Display your projects and achievements
- 📄 **Resume/CV** - Comprehensive resume section
- 🔧 **Skills Management** - Highlight your technical skills
- 🎨 **Project Gallery** - Beautiful project presentation
- 🔐 **Secure Backend** - Django REST API with JWT authentication
- 💾 **Database Support** - PostgreSQL integration
- ☁️ **Cloud Ready** - Configured for Liara deployment
- 📦 **S3 Integration** - AWS S3 storage support
- 🔄 **Celery Tasks** - Background job processing

### Tech Stack

#### Backend
- **Framework**: Django 5.2
- **API**: Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: PostgreSQL
- **Caching**: Redis
- **Task Queue**: Celery
- **Server**: Gunicorn
- **Deployment**: Liara
- **Storage**: AWS S3 (boto3)

#### Frontend
- **Framework**: React
- **Package Manager**: npm
- **Build Tool**: Create React App

### Project Structure
```
personal_web/
├── backend/
│   ├── core/              # Django core settings
│   ├── portfolio/         # Portfolio app
│   ├── manage.py          # Django management script
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables
│   ├── liara.json         # Liara deployment config
│   └── backend.zip        # Backup archive
│
└── frontend/
    └── my-portfolio/      # React portfolio app
        └── package.json   # NPM dependencies
```

### Installation & Setup

#### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL 12+
- Redis (for caching)
- npm or yarn

#### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create or update `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_NAME=minWeb_db
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket

# Redis (for caching)
REDIS_URL=redis://localhost:6379/0
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Start development server**
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

#### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend/my-portfolio
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure API endpoint** (in `.env` or config file)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

4. **Start development server**
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

### Deployment

#### Deploy to Liara (Recommended)

1. **Install Liara CLI**
```bash
npm install -g @liara/cli
```

2. **Login to Liara**
```bash
liara login
```

3. **Deploy backend**
```bash
cd backend
liara deploy
```

4. **Configure environment on Liara dashboard**
- Set all required environment variables
- Configure database and Redis
- Upload AWS S3 credentials if needed

#### Alternative Deployment Options
- Heroku
- AWS Elastic Beanstalk
- DigitalOcean App Platform
- PythonAnywhere (for backend only)
- Vercel/Netlify (for frontend)

### API Documentation

The Django backend provides a REST API. After running the server, access:
- **API Root**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **API Schema**: `http://localhost:8000/api/schema/` (Swagger/OpenAPI)

### Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode | `False` |
| `ALLOWED_HOSTS` | Allowed host domains | `localhost,yourdomain.com` |
| `DB_NAME` | PostgreSQL database name | `minWeb_db` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `secure-password` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |

### Usage

1. **Admin Panel**: Manage projects, resume, and portfolio content
   - URL: `http://localhost:8000/admin/`
   - Login with superuser credentials

2. **Frontend**: View your portfolio
   - Access at `http://localhost:3000`
   - All content is dynamically loaded from the backend API

3. **Add/Edit Content**:
   - Use Django admin to add projects
   - Update resume information
   - Manage portfolio sections

### Common Issues & Troubleshooting

**Port already in use**
```bash
# Backend (change port)
python manage.py runserver 8001

# Frontend (change port)
PORT=3001 npm start
```

**Database connection error**
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists: `createdb minWeb_db`

**Redis connection error**
- Install Redis or use Memcached as alternative
- Update cache settings in `core/settings.py`

**Static files not loading**
```bash
python manage.py collectstatic --noinput --clear
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is open source and available under the MIT License.

---

## فارسی

### نمای کلی
یک وبسایت نمونه‌کار شخصی تمام‌پایه (Full-Stack) که با **Django** (بک‌اند) و **React** (فرانت‌اند) ساخته شده است. این پروژه پروژه‌ها، رزومه، مهارت‌ها و اطلاعات نمونه‌کار را با طراحی مدرن و پاسخ‌گو نمایش می‌دهد.

### ویژگی‌ها
- ✨ **رابط کاربری مدرن** - طراحی پاسخ‌گو برای تمام دستگاه‌ها
- 📱 **نمایش نمونه‌کار** - نمایش پروژه‌ها و دستاوردهای شما
- 📄 **بخش رزومه/CV** - بخش رزومه جامع
- 🔧 **مدیریت مهارت‌ها** - برجسته‌سازی مهارت‌های فنی شما
- 🎨 **گالری پروژه** - ارائه زیبای پروژه‌ها
- 🔐 **بک‌اند ایمن** - Django REST API با احراز هویت JWT
- 💾 **پشتیبانی پایگاه‌داده** - ادغام PostgreSQL
- ☁️ **آماده ابر** - پیکربندی برای استقرار در Liara
- 📦 **ادغام S3** - پشتیبانی از ذخیره‌سازی AWS S3
- 🔄 **وظایف Celery** - پردازش کارهای پس‌زمینه

### پشته فناوری

#### بک‌اند
- **چارچوب**: Django 5.2
- **API**: Django REST Framework
- **احراز هویت**: JWT (SimpleJWT)
- **پایگاه‌داده**: PostgreSQL
- **حافظه پنهان**: Redis
- **صف وظایف**: Celery
- **سرور**: Gunicorn
- **استقرار**: Liara
- **ذخیره‌سازی**: AWS S3 (boto3)

#### فرانت‌اند
- **چارچوب**: React
- **مدیریت بسته**: npm
- **ابزار ساخت**: Create React App

### ساختار پروژه
```
personal_web/
├── backend/               # بک‌اند
│   ├── core/              # تنظیمات هسته Django
│   ├── portfolio/         # اپ نمونه‌کار
│   ├── manage.py          # اسکریپت مدیریت Django
│   ├── requirements.txt    # وابستگی‌های Python
│   ├── .env               # متغیرهای محیطی
│   ├── liara.json         # پیکربندی استقرار Liara
│   └── backend.zip        # بایگانی پشتیبان
│
└── frontend/              # فرانت‌اند
    └── my-portfolio/      # اپ React نمونه‌کار
        └── package.json   # وابستگی‌های NPM
```

### نصب و راه‌اندازی

#### پیش‌نیازها
- Python 3.10+
- Node.js 16+
- PostgreSQL 12+
- Redis (برای حافظه پنهان)
- npm یا yarn

#### راه‌اندازی بک‌اند

1. **به دایرکتوری بک‌اند بروید**
```bash
cd backend
```

2. **محیط مجازی ایجاد کنید**
```bash
python -m venv venv
source venv/bin/activate  # در Windows: venv\Scripts\activate
```

3. **وابستگی‌ها را نصب کنید**
```bash
pip install -r requirements.txt
```

4. **متغیرهای محیطی را پیکربندی کنید**
فایل `.env` را ایجاد یا بروزرسانی کنید:
```env
SECRET_KEY=کلید-محرمانه-شما
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,دامنه-شما.com

# پایگاه‌داده
DB_NAME=minWeb_db
DB_USER=postgres
DB_PASSWORD=رمز-عبور-ایمن-شما
DB_HOST=localhost
DB_PORT=5432

# AWS S3 (اختیاری)
AWS_ACCESS_KEY_ID=کلید-aws-شما
AWS_SECRET_ACCESS_KEY=رمز-aws-شما
AWS_STORAGE_BUCKET_NAME=سطل-شما

# Redis (برای حافظه پنهان)
REDIS_URL=redis://localhost:6379/0
```

5. **انتقال‌ها (Migrations) را اجرا کنید**
```bash
python manage.py migrate
```

6. **کاربر ادمین ایجاد کنید**
```bash
python manage.py createsuperuser
```

7. **فایل‌های ایستا را جمع‌آوری کنید**
```bash
python manage.py collectstatic --noinput
```

8. **سرور توسعه را شروع کنید**
```bash
python manage.py runserver
```

بک‌اند در `http://localhost:8000` دردسترس خواهد بود

#### راه‌اندازی فرانت‌اند

1. **به دایرکتوری فرانت‌اند بروید**
```bash
cd frontend/my-portfolio
```

2. **وابستگی‌ها را نصب کنید**
```bash
npm install
```

3. **نقطه پایانی API را پیکربندی کنید** (در فایل `.env` یا پیکربندی)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

4. **سرور توسعه را شروع کنید**
```bash
npm start
```

فرانت‌اند در `http://localhost:3000` دردسترس خواهد بود

### استقرار

#### استقرار در Liara (توصیه شده)

1. **CLI Liara را نصب کنید**
```bash
npm install -g @liara/cli
```

2. **به Liara وارد شوید**
```bash
liara login
```

3. **بک‌اند را استقرار دهید**
```bash
cd backend
liara deploy
```

4. **محیط را در داشبورد Liara پیکربندی کنید**
- تمام متغیرهای محیطی مورد نیاز را تنظیم کنید
- پایگاه‌داده و Redis را پیکربندی کنید
- در صورت نیاز، اعتبارات AWS S3 را بارگذاری کنید

#### گزینه‌های استقرار جایگزین
- Heroku
- AWS Elastic Beanstalk
- DigitalOcean App Platform
- PythonAnywhere (فقط برای بک‌اند)
- Vercel/Netlify (فقط برای فرانت‌اند)

### مستندات API

بک‌اند Django یک REST API فراهم می‌کند. پس از اجرای سرور، دسترسی داشته باشید:
- **ریشه API**: `http://localhost:8000/api/`
- **پنل ادمین**: `http://localhost:8000/admin/`
- **طرح API**: `http://localhost:8000/api/schema/` (Swagger/OpenAPI)

### مرجع متغیرهای محیطی

| متغیر | توضیح | مثال |
|-------|-------|------|
| `SECRET_KEY` | کلید محرمانه Django | `django-insecure-...` |
| `DEBUG` | حالت اشکال‌زدایی | `False` |
| `ALLOWED_HOSTS` | دامنه‌های میزبان مجاز | `localhost,دامنه-شما.com` |
| `DB_NAME` | نام پایگاه‌داده PostgreSQL | `minWeb_db` |
| `DB_USER` | کاربر PostgreSQL | `postgres` |
| `DB_PASSWORD` | رمز عبور PostgreSQL | `رمز-عبور-ایمن` |
| `DB_HOST` | میزبان PostgreSQL | `localhost` |
| `DB_PORT` | درگاه PostgreSQL | `5432` |

### استفاده

1. **پنل ادمین**: مدیریت پروژه‌ها، رزومه و محتوای نمونه‌کار
   - URL: `http://localhost:8000/admin/`
   - ورود با اعتبارات کاربر ادمین

2. **فرانت‌اند**: مشاهده نمونه‌کار شما
   - دسترسی در `http://localhost:3000`
   - تمام محتوا به‌صورت پویا از API بک‌اند بارگذاری می‌شود

3. **افزودن/ویرایش محتوا**:
   - از ادمین Django برای افزودن پروژه‌ها استفاده کنید
   - اطلاعات رزومه را بروزرسانی کنید
   - بخش‌های نمونه‌کار را مدیریت کنید

### مشکلات رایج و حل‌آنها

**درگاه در حال استفاده است**
```bash
# بک‌اند (تغییر درگاه)
python manage.py runserver 8001

# فرانت‌اند (تغییر درگاه)
PORT=3001 npm start
```

**خطای اتصال پایگاه‌داده**
- تأیید کنید PostgreSQL در حال اجرا است
- اعتبارات پایگاه‌داده را در `.env` بررسی کنید
- اطمینان حاصل کنید پایگاه‌داده وجود دارد: `createdb minWeb_db`

**خطای اتصال Redis**
- Redis را نصب کنید یا Memcached را به‌عنوان جایگزین استفاده کنید
- تنظیمات حافظه پنهان را در `core/settings.py` بروزرسانی کنید

**فایل‌های ایستا بارگذاری نمی‌شوند**
```bash
python manage.py collectstatic --noinput --clear
```

### مشارکت

1. مخزن را Fork کنید
2. یک شاخه ویژگی ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را Commit کنید (`git commit -m 'Add amazing feature'`)
4. به شاخه Push کنید (`git push origin feature/amazing-feature`)
5. یک Pull Request باز کنید

### مجوز

این پروژه متن‌باز است و تحت مجوز MIT دردسترس است.

---

**Made with ❤️ by Rmin-code2005**
