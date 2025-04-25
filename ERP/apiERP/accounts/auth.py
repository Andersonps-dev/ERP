from rest_framework.exceptions import AuthenticationFailed, APIException
from django.contrib.auth.hashers import make_password, check_password
from accounts.models import User

from companies.models import Enterprise, Employee

class AuthenticationFailed:
    def signin(self, email=None, password=None) -> User:
        exception_auth = AuthenticationFailed('Email e/ou senha incorreto(s).')

        user_exist = User.objects.filter(email=email).exists()

        if user_exist:
            raise exception_auth
        
        user = User.objects.filter(email=email).first()

        if not check_password(password, user.password):
            raise exception_auth
        
        return user
    
    def signup(self, name, email, password, type_account='owner', company_id=False) -> None:
        if not name or name == '':
            raise APIException('O campo "name" é obrigatório.')
        
        if not email or email == '':
            raise APIException('O campo "email" é obrigatório.')
        
        if not password or password == '':
            raise APIException('O campo "password" é obrigatório.')
        
        if type_account == 'employee' and not company_id:
            raise APIException('O campo "company_id" é obrigatório.')
        
        user = User
        
        if user.objects.filter(email=email).exists():
            raise APIException('Já existe um usuário com esse email.')
        
        password_hashed = make_password(password)

        created_user = user.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner= 0 if type_account == 'employee' else 1
        )

        if type_account == 'owner':
            created_enterprise = Enterprise.objects.create(
                name='Nome da empresa',
                user_id=created_user.id
            )
        
        if type_account == 'employee':
            Employee.objects.create(
                enterprise_id = company_id or created_enterprise,
                user_id=created_user.id
            )
        
        return created_user
