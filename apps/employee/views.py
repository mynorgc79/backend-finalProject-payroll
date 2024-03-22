from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.shortcuts import render


""" SERIALIZERS """
from .serializers import  EmployeeSerializer, SalaryIncreaseSerializer, DepartmentSerializer, EmployeeDocumentSerializer, FamilyMemberSerializer, JobPositionSerializer, RequestAbsenceSerializer
from apps.user.serializers import UserSerializer

""" MODELS """
from .models import EmployeeDocument, FamilyMember, Employee, SalaryIncrease, Department, JobPositionModel, RequestAbsenceModel
from apps.company.models import Company
from apps.user.models import User


class EmployeeDocumentsViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeDocumentSerializer


    def get_queryset(self):
        # Filtrar los documentos por is_active=True
        queryset = EmployeeDocument.objects.filter(is_active=True)
        return queryset
    

    def create(self, request, *args, **kwargs):
        # Validar si el empleado existe
        employee_id = request.data.get('employee')
        if not Employee.objects.filter(id=employee_id).exists():
            return Response({'error': 'El empleado especificado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class FamilyMembersViewSet(viewsets.ModelViewSet):
    serializer_class = FamilyMemberSerializer


    def get_queryset(self):
        # Filtrar los miembros de la familia por is_active=True
        queryset = FamilyMember.objects.filter(is_active=True)
        return queryset
    

    def create(self, request, *args, **kwargs):
        # Validar si el empleado existe
        employee_id = request.data.get('employee')
        if not Employee.objects.filter(id=employee_id).exists():
            return Response({'error': 'El empleado especificado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        # Filtrar empleados de una empresa específica
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = Employee.objects.filter(company=company_id)
        else:
            queryset = Employee.objects.all()
        return queryset
    
    

    def create(self, request, *args, **kwargs):

        employee_data = request.data.get('employee', {})

        user_data = employee_data.pop('user', {})

        user_instance = User(email=user_data.get('email'), username=user_data.get('username'))
        user = user_instance.create_user(email=user_data.get('email'), username=user_data.get('username'))

        employee_data['user'] = user.id

        employee_serializer = EmployeeSerializer(data=employee_data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SalaryIncreaseViewSet(viewsets.ModelViewSet):
    queryset = SalaryIncrease.objects.all()
    permission_classes = [permissions.AllowAny] #Cambiar a IsAuthenticated
    serializer_class = SalaryIncreaseSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [permissions.AllowAny] #Cambiar a IsAuthenticated
    serializer_class = DepartmentSerializer

    # Filtrar departamentos por empresa
    def get_queryset(self):
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = Department.objects.filter(company=company_id)
        else:
            queryset = Department.objects.all()
        return queryset


    def create(self, request, *args, **kwargs):
        
        company_id = request.data.get('company')
        if not Company.objects.filter(id=company_id).exists():
            return Response({'error': 'La empresa especificada no existe'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class JobPositionViewSet(viewsets.ModelViewSet):
    serializer_class = JobPositionSerializer
    permission_classes = [permissions.AllowAny] #Cambiar a IsAuthenticated


    def get_queryset(self):
        # Filtrar los jobPosition by is_active
        queryset = JobPositionModel.objects.filter(is_active=True)
        return queryset
    

    def create(self, request, *args, **kwargs):
         return super().create(request, *args, **kwargs)


class RequestAbsenceViewSet(viewsets.ModelViewSet):
    queryset = RequestAbsenceModel.objects.all()
    serializer_class = RequestAbsenceSerializer
    permission_classes = [permissions.AllowAny] #Cambiar a IsAuthenticated


    def create(self, request, *args, **kwargs):
        # Validar si el empleado existe
        employee_id = request.data.get('employee')
        if not Employee.objects.filter(id=employee_id).exists():
            return Response({'error': 'El empleado especificado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

