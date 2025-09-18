from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Employee, DynamicField
from .serializers import EmployeeSerializer

class EmployeeListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        dynamic_fields = list(DynamicField.objects.values('id', 'label', 'field_type'))
        return Response({
            'employees': serializer.data,
            'dynamic_fields': dynamic_fields
        }, status=status.HTTP_200_OK)


class EmployeeCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        dynamic_fields = DynamicField.objects.all()
        dynamic_data = {}
        for field in dynamic_fields:
            dynamic_data[field.label] = request.data.get(f'field_{field.id}', '')
        serializer = EmployeeSerializer(data={'dynamic_data': dynamic_data})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            emp = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            return Response({'success': False, 'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        dynamic_fields = DynamicField.objects.all()
        dynamic_data = {}
        for field in dynamic_fields:
            dynamic_data[field.label] = request.data.get(f'field_{field.id}', '')

        emp.dynamic_data = dynamic_data
        emp.save()
        return Response({'success': True}, status=status.HTTP_200_OK)


class EmployeeDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            emp = Employee.objects.get(id=pk)
            emp.delete()
            return Response({'success': True, 'id': pk}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'success': False, 'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
