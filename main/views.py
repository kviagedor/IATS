from django.shortcuts import render, get_object_or_404
from . models import *
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .forms import CSVUploadForm
import csv



from django.shortcuts import render
from .models import Employee
import json

def asset_chart(request):
    # Count the number of employees for each status
    type_counts = {}
    for type, _ in ITAsset.ASSET_TYPES:
        type_counts[type] = ITAsset.objects.filter(type=type).count()

    # Convert status counts to JSON format
    type_counts_json = json.dumps(type_counts)

    # Pass the status counts JSON to the template
    print(type_counts_json)
    context = {
        'type_counts_json': type_counts_json
    }

    return render(request, 'asset_chart.html', context)



def upload_employee_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for row in csv_reader:
                department_name = row['department']
                location_name = row['location']

                # Get or create Department object
                department, _ = Department.objects.get_or_create(name=department_name)

                # Get or create Location object
                location, _ = Location.objects.get_or_create(name=location_name)

                # Parse date string and format it as YYYY-MM-DD
                hire_date_str = row['hire_date']
                hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d').date()

                # Create Employee object
                Employee.objects.create(
                    employee_id=row['employee_id'],
                    name=row['name'],
                    # birth_date=row['birth_date'],
                    title=row['title'],
                    reports_to=row['reports_to'],
                    department=department,
                    location=location,
                    status=row['status'],
                    hire_date=hire_date,
                )
            return render(request, 'success.html')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_employee_csv.html', {'form': form})


def upload_it_asset_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()  # Use ISO-8859-1 encoding
            csv_reader = csv.DictReader(decoded_file)
            for row in csv_reader:
                asset_tag = row['ASSET TAG']

                # Check if asset tag already exists
                if ITAsset.objects.filter(asset_tag=asset_tag).exists():
                    # Handle existing asset tag (e.g., update existing record)
                    pass
                else:
                    category = row['CATEGORY']
                    location = row['LOCATION']
                    assigned_to = row['ASSIGNED TO']

                    # Get or create Category object
                    category, _ = Category.objects.get_or_create(name=category)

                    # Get or create Location object
                    location, _ = Location.objects.get_or_create(name=location)

                    # Get or create Employee object
                    assigned_to = None
                    if assigned_to:
                        assigned_to, _ = Employee.objects.get_or_create(name=assigned_to)

                    # Create ITAsset object
                    ITAsset.objects.create(
                        asset_tag=asset_tag,
                        category=category,
                        type=row['TYPE'],
                        brand=row['BRAND'],
                        model=row['MODEL'],
                        serial_number=row['SERIAL NUMBER'],
                        location=location,
                        assigned_to=assigned_to,
                        state=row['STATE'],
                        deployed_date=row['DEPLOY DATE'],
                        request_no=row['REQUEST NUMBER']
                    )
            return render(request, 'success.html')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_it_asset_csv.html', {'form': form})




def asset(request,asset_tag):
    asset = get_object_or_404(ITAsset, asset_tag=asset_tag)
    context = {'asset':asset}
    return render(request, 'asset.html', context)

def universal_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Perform search across multiple models and fields
        results += Employee.objects.filter(field__icontains=query)
        # results += ITAsset.objects.filter(field__icontains=query)

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'search_results.html', context)

def home(request):

    # Fetch all employees from the database
    employees = Employee.objects.all()
    employee_count = Employee.objects.values('status').annotate(employee_count=Count('status'))

    # Get unique locations and departments for filtering dropdowns
    cutoff_date = datetime.now() - timedelta(days=30)
    
    # Query the Employee model for employees hired after the cutoff date
    newly_hired_employees = Employee.objects.filter(hire_date__gte=cutoff_date)
    total_newly_hired = newly_hired_employees.count()

    current_day = datetime.now().day

    employees_with_birthday = Employee.objects.filter(birth_date__day=current_day)

    # Filter employees who have reached their 10-year anniversary
    ten_year_anniversary_employees = Employee.objects.filter(
        hire_date__lte=timezone.now().date() - timedelta(days=365*10)
    ).exclude(status='Resigned')

    assets = ITAsset.objects.all()

    asset_count = ITAsset.objects.values('type').annotate(asset_count=Count('type'))

    # Get the current month and year
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    # Retrieve deployed assets within the current month
    deployed_asset = ITAsset.objects.filter(
        deployed_date__year=current_year,
        deployed_date__month=current_month,
        state='In use'
    )

    total_deployed_asset = ITAsset.objects.filter(
        state='In use'
    )

    # Retrieve assets in stock
    assets_in_stock = ITAsset.objects.filter(state='In stock')
    asset_type_counts_deployed = total_deployed_asset.values('type').annotate(count=Count('type'))
    asset_type_counts_in_stock = assets_in_stock.values('type').annotate(count=Count('type'))

    # Count the number of employees for each status
    type_counts = {}
    for type, _ in ITAsset.ASSET_TYPES:
        type_counts[type] = ITAsset.objects.filter(type=type).count()

    # Convert status counts to JSON format
    type_counts_json = json.dumps(type_counts)

    # Pass the status counts JSON to the template

    context = {
        'employees': employees,
        'employee_count': employee_count,
        'newly_hired_employees': newly_hired_employees,
        'total_newly_hired': total_newly_hired,
        'employees_with_birthday': employees_with_birthday,
        'ten_year_anniversary_employees': ten_year_anniversary_employees,
        'assets': assets,
        'asset_count': asset_count,
        'deployed_asset': deployed_asset,
        'assets_in_stock': assets_in_stock,
        'asset_type_counts_deployed': asset_type_counts_deployed,
        'asset_type_counts_in_stock': asset_type_counts_in_stock,
        'type_counts_json': type_counts_json
    }
    return render(request, 'home.html', context)
    

def employees(request):
    employees = Employee.objects.all()

    # Paginate the employees with 10 items per page
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'employee_list.html', context)

def itAsset(request):
    # Fetch all IT assets from the database
    assets = ITAsset.objects.all()

    # Paginate the assets with 20 items per page
    paginator = Paginator(assets, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'itassets.html', context)