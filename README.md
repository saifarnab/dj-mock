# Mock Api Service 

```bash
  sudo apt install python3.12-full python3.12-dev
```

Create new environment
```python
python3.12 -m venv your_env_name
```

Install required packages
```
source your_env_name/bin/activate
pip install -r requirements.txt
```


## Setup configuration in (.env) file .


```python manage.py migrate```

run this command in Django shell.
```
from back_office_user.models import Permission, Role, BackOfficeUser
from common.models import UCBBranch
permission = Permission.objects.create(name="Can Create User",code="can_create_user", is_active=True)
role = Role.objects.create(name="super_user")
role.permission.add(permission)
branch = UCBBranch.objects.create(branch_code="123456789", branch_name="Head Office")
```
### Then run : createsuperuser
