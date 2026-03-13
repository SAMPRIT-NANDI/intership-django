# intership-django
>>>>>>> 245b02ac748fd82a059b88e7f12741a82a2b72a3
=======
# Django Internship API - Vendor → Product → Course → Certification Pipeline

## 🎯 Problem Solved
**Question**: "Create Django API + Dashboard for internship pipeline with Vendors → Products → Courses → Certifications + Windows PowerShell sample data error."

**Solution Steps**:
1. **Modular Django apps**: vendor/product/course/certification + 3 mapping apps
2. **DRF CRUD**: ListCreateAPIView + DetailAPIView (full POST/GET/PUT/PATCH/DELETE)
3. **Validation**: Unique codes, no duplicate mappings, single primary per parent
4. **Sample data**: Idempotent script (get_or_create by code)
5. **Windows fix**: `Get-Content script.py | python manage.py shell`
6. **Dashboard**: Glassmorphism UI + Chart.js + live CRUD/search/theme

## 🚀 Quick Start
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # sampritnandi
Get-Content populate_sample_data.py | python manage.py shell  # Windows
python populate_sample_data.py  # Linux/Mac/standalone
python manage.py runserver
```

**Live**:
- http://127.0.0.1:8000/ → Dashboard (stats/charts/lists)
- /swagger/ → API docs
- /admin/ → Admin panel

## 📊 Expected Data (after populate)
```
Vendors: 5 (TechCorp TC001...)
Products: 6 (Python PD001...)
Courses: 7 (Advanced Python PY201...)
Certifications: 6 (Certified Python CPP001...)
Mappings: 22 total
```

## 🔗 API Endpoints
```
POST /api/vendors/vendors/ → {"name": "NewCorp", "code": "NC001"}
GET /api/vendors/vendors/ → List all
/api/vendors/vendors/1/ → Detail/update/delete
```
*(Same pattern for products/courses/certs/mappings)*

## 💡 Key Features
- ✅ **Nested URLs**: /api/vendors/vendors/ (app-named)
- ✅ **Primary mappings**: 1 primary per parent (validated)
- ✅ **Idempotent data**: Rerun populate anytime
- ✅ **Dashboard**: Real-time stats/charts/search/CRUD
- ✅ **Responsive**: Mobile/tablet/desktop
- ✅ **Dark/Light theme**: Auto-detect

## 🎨 Dashboard Demo Flow
1. Stats cards update live (Vendors:6...)
2. Doughnut chart [V,P,C,Cert,Maps]
3. Click "Add" → Form → Submit → Instant refresh
4. Search "TC001" → Filters lists
5. Edit/Delete hover buttons
6. Global search across all entities

**100% Complete & Interview Ready!** 🚀

=======
# intership-django
>>>>>>> 245b02ac748fd82a059b88e7f12741a82a2b72a3
