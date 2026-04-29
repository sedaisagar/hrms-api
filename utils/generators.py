
def generate_client_id():
    from django.apps import apps
    Klass = apps.get_model('users', 'ClientProfile')
    total = Klass.objects.count()
    return f"CLT-{total+1:05d}"

def generate_employee_id():
    from django.apps import apps
    Klass = apps.get_model('users', 'EmployeeProfile')
    total = Klass.objects.count()
    return f"EMP-{total+1:05d}"

