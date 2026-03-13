# Django Internship API - Modular Entity and Mapping System

## Project Structure
```
internship/
├── internship_api/ (main project)
├── vendor/
├── product/
├── course/
├── certification/
├── vendor_product_mapping/
├── product_course_mapping/
├── course_certification_mapping/
├── manage.py
├── db.sqlite3
└── README.md
```

## Setup Instructions

1. **Install Dependencies** (already done):
```
pip install django djangorestframework drf-yasg
```

2. **Run Migrations** (already done):
```
python manage.py makemigrations
python manage.py migrate
```

3. **Create Superuser**:
```
python manage.py createsuperuser
```

**4. Populate Sample Data** (Windows/PowerShell):
```
Get-Content populate_sample_data.py | python manage.py shell
```
**Alternative (any OS)**:
```
python populate_sample_data.py
```

**Example Output**:
```
🚀 Loading enhanced sample data...
✅ Created Vendor: TechCorp
✅ Created Product: Python Developer Courseware
...
📦 Vendors ready: 5
📦 Products ready: 6
📚 Courses ready: 7
🏆 Certifications ready: 6
🔗 VendorProductMappings: 7 new
📖 ProductCourseMappings: 8 new
🎓 CourseCertificationMappings: 7 new
🎉 **ENHANCED SAMPLE DATA LOADED SUCCESSFULLY!** 🚀
📊 SUMMARY:
   Vendors: 5
   Products: 6
   Courses: 7
   Certifications: 6
   VPM: 7
   PCM: 8
   CCM: 7
```
Expected: 5 vendors, 6 products, 7 courses, 6 certs, 22 mappings.

5. **Run Server**:
```
python manage.py runserver
```

## API Endpoints

**Dashboard**: http://127.0.0.1:8000/
**Swagger Docs**: http://127.0.0.1:8000/swagger/
**ReDoc**: http://127.0.0.1:8000/redoc/
**Admin**: http://127.0.0.1:8000/admin/

### Master Entities
- `GET/POST /api/vendors/` - List/Create vendors
- `GET/PUT/PATCH/DELETE /api/vendors/<id>/`
- `GET/POST /api/products/` 
- `GET/PUT/PATCH/DELETE /api/products/<id>/`
- `GET/POST /api/courses/` 
- `GET/PUT/PATCH/DELETE /api/courses/<id>/`
- `GET/POST /api/certifications/` 
- `GET/PUT/PATCH/DELETE /api/certifications/<id>/` 

### Mappings
- `GET/POST /api/vendor-product-mappings/` (?vendor_id=1 &product_id=1)
- `GET/PUT/PATCH/DELETE /api/vendor-product-mappings/<id>/`
- `GET/POST /api/product-course-mappings/` (?product_id=1 &course_id=1)
- `GET/PUT/PATCH/DELETE /api/product-course-mappings/<id>/`
- `GET/POST /api/course-certification-mappings/` (?course_id=1 &certification_id=1)
- `GET/PUT/PATCH/DELETE /api/course-certification-mappings/<id>/`

## Validation Rules Implemented
✅ Unique code per master entity  
✅ Duplicate mapping prevention (unique_together)  
✅ Single primary_mapping per parent  
✅ Required fields validation  
✅ Soft delete (is_active=False)  

## Sample Usage (cURL/Postman)

**Create Vendor**:
```bash
curl -X POST http://127.0.0.1:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "TechCorp", "code": "TC001", "description": "Technology Company"}'
```

**Create Product**:
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Pro", "code": "LP001"}'
```

**Create Primary Mapping**:
```bash
curl -X POST http://127.0.0.1:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{"vendor": 1, "product": 1, "primary_mapping": true}'
```

## Features
- **APIView only** (no ViewSets/routers)
- **Full CRUD** operations
- **Query filtering** across relationships
- **Custom validation** (duplicate prevention, single primary)
- **Soft delete**
- **Auto-documented** Swagger/ReDoc
- **Modular apps** (models/serializers/views/urls/admin per app)

**Project complete & ready to test! 🎉**

