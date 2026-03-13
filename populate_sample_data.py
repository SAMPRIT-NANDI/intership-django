#!/usr/bin/env python
"""
Enhanced Sample Data for Interview Demo - Run: python manage.py shell < populate_sample_data.py
Improved: Idempotent (by code), more diverse data, dynamic object mappings (no hardcoded IDs), atomic.
"""
import os
import django
from django.db import transaction

# Setup Django (in case run standalone, but prefer shell)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internship_api.settings')
django.setup()

from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


@transaction.atomic
def create_sample_data():
    print("🚀 Loading enhanced sample data...")

    # 1. Vendors (5)
    vendor_data = [
        {"name": "TechCorp", "code": "TC001", "description": "Technology Solutions Provider"},
        {"name": "EduTech Inc", "code": "ET001", "description": "Educational Technology Leader"},
        {"name": "ProSkills Academy", "code": "PS001", "description": "Professional Training Experts"},
        {"name": "DataMasters", "code": "DM001", "description": "Data Science Specialists"},
        {"name": "CloudNinja", "code": "CN001", "description": "Cloud & DevOps Consultants"},
    ]
    vendors = []
    for data in vendor_data:
        vendor, created = Vendor.objects.get_or_create(code=data["code"], defaults=data)
        if created:
            print(f"✅ Created Vendor: {vendor}")
        vendors.append(vendor)
    print(f"📦 Vendors ready: {len(vendors)}")

    # 2. Products (6)
    product_data = [
        {"name": "Python Developer Courseware", "code": "PD001", "description": "Complete Python curriculum & tools"},
        {"name": "DevOps Toolkit", "code": "DT001", "description": "CI/CD, Docker, Kubernetes toolkit"},
        {"name": "Data Science Suite", "code": "DS001", "description": "ML pipelines + Data Analysis"},
        {"name": "Full Stack Web Dev", "code": "FS001", "description": "React + Django + Deployment"},
        {"name": "Cybersecurity Fundamentals", "code": "CS001", "description": "Security best practices"},
        {"name": "AWS Cloud Architect", "code": "AW001", "description": "AWS certification prep"},
    ]
    products = []
    for data in product_data:
        product, created = Product.objects.get_or_create(code=data["code"], defaults=data)
        if created:
            print(f"✅ Created Product: {product}")
        products.append(product)
    print(f"📦 Products ready: {len(products)}")

    # 3. Courses (7)
    course_data = [
        {"name": "Advanced Python Programming", "code": "PY201", "description": "Intermediate-Advanced Python"},
        {"name": "Docker & Kubernetes Mastery", "code": "DK101", "description": "Container orchestration hands-on"},
        {"name": "Machine Learning Basics", "code": "ML101", "description": "Intro ML with Scikit-Learn"},
        {"name": "React Frontend Development", "code": "RF101", "description": "Modern React with Hooks"},
        {"name": "Cybersecurity Essentials", "code": "CY101", "description": "Threat modeling & defense"},
        {"name": "AWS Cloud Practitioner", "code": "AW101", "description": "AWS fundamentals"},
        {"name": "Data Engineering Pipeline", "code": "DE101", "description": "ETL with Airflow & Spark"},
    ]
    courses = []
    for data in course_data:
        course, created = Course.objects.get_or_create(code=data["code"], defaults=data)
        if created:
            print(f"✅ Created Course: {course}")
        courses.append(course)
    print(f"📚 Courses ready: {len(courses)}")

    # 4. Certifications (6)
    cert_data = [
        {"name": "Certified Python Professional", "code": "CPP001", "description": "Advanced Python certification"},
        {"name": "DevOps Certified Engineer", "code": "DCE001", "description": "DevOps practices & tools"},
        {"name": "Machine Learning Practitioner", "code": "MLP001", "description": "ML deployment"},
        {"name": "AWS Certified Architect", "code": "ACA001", "description": "Cloud architecture"},
        {"name": "Cybersecurity Analyst", "code": "CSA001", "description": "SIEM & incident response"},
        {"name": "Full Stack Developer Cert", "code": "FSD001", "description": "End-to-end web dev"},
    ]
    certs = []
    for data in cert_data:
        cert, created = Certification.objects.get_or_create(code=data["code"], defaults=data)
        if created:
            print(f"✅ Created Certification: {cert}")
        certs.append(cert)
    print(f"🏆 Certifications ready: {len(certs)}")

    # 5. Vendor-Product Mappings (logical)
    vpm_data = [
        (vendors[0], products[0], True),  # TechCorp - Python (primary)
        (vendors[0], products[1]),        # TechCorp - DevOps
        (vendors[1], products[2], True),  # EduTech - Data Science (primary)
        (vendors[1], products[3]),        # EduTech - Full Stack
        (vendors[2], products[4], True),  # ProSkills - Cybersecurity
        (vendors[3], products[5]),       # DataMasters - AWS
        (vendors[4], products[1]),       # CloudNinja - DevOps
    ]
    vpm_count = 0
    for vendor, product, *primary in vpm_data:
        mapping, created = VendorProductMapping.objects.get_or_create(
            vendor=vendor, product=product, defaults={"primary_mapping": primary[0] if primary else False}
        )
        if created:
            vpm_count += 1
            print(f"🔗 Created VPM: {vendor.code}-{product.code}")
    print(f"🔗 VendorProductMappings: {vpm_count} new")

    # 6. Product-Course Mappings
    pcm_data = [
        (products[0], courses[0], True),  # Python product -> Python course
        (products[1], courses[1], True),  # DevOps -> Docker
        (products[2], courses[2], True),  # DS -> ML
        (products[3], courses[3]),        # FS -> React
        (products[3], courses[6]),        # FS -> Data Eng
        (products[4], courses[4], True),  # Cyber -> Cyber
        (products[5], courses[5], True),  # AWS -> AWS
        (products[1], courses[1]),        # extra
    ]
    pcm_count = 0
    for product, course, *primary in pcm_data:
        mapping, created = ProductCourseMapping.objects.get_or_create(
            product=product, course=course, defaults={"primary_mapping": primary[0] if primary else False}
        )
        if created:
            pcm_count += 1
            print(f"📖 Created PCM: {product.code}-{course.code}")
    print(f"📖 ProductCourseMappings: {pcm_count} new")

    # 7. Course-Certification Mappings
    ccm_data = [
        (courses[0], certs[0], True),  # Python course -> Python cert
        (courses[1], certs[1], True),  # Docker -> DevOps
        (courses[2], certs[2], True),  # ML -> ML
        (courses[3], certs[5]),        # React -> Full Stack
        (courses[4], certs[4], True),  # Cyber -> Cyber
        (courses[5], certs[3], True),  # AWS -> AWS Architect
        (courses[6], certs[2]),        # Data Eng -> ML Practitioner
    ]
    ccm_count = 0
    for course, cert, *primary in ccm_data:
        mapping, created = CourseCertificationMapping.objects.get_or_create(
            course=course, certification=cert, defaults={"primary_mapping": primary[0] if primary else False}
        )
        if created:
            ccm_count += 1
            print(f"🎓 Created CCM: {course.code}-{cert.code}")
    print(f"🎓 CourseCertificationMappings: {ccm_count} new")

    # Final summary
    print("\n🎉 **ENHANCED SAMPLE DATA LOADED SUCCESSFULLY!** 🚀")
    print(f"📊 SUMMARY:")
    print(f"   Vendors: {Vendor.objects.count()}")
    print(f"   Products: {Product.objects.count()}")
    print(f"   Courses: {Course.objects.count()}")
    print(f"   Certifications: {Certification.objects.count()}")
    print(f"   VPM: {VendorProductMapping.objects.count()}")
    print(f"   PCM: {ProductCourseMapping.objects.count()}")
    print(f"   CCM: {CourseCertificationMapping.objects.count()}")
    print("\n🌐 Dashboard: http://127.0.0.1:8000/")
    print("📋 Swagger: http://127.0.0.1:8000/swagger/")
    print("\n**INTERVIEW READY with rich demo data!** 🔥")


if __name__ == '__main__':
    create_sample_data()

