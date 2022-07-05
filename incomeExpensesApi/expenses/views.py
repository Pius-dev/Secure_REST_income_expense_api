from django.shortcuts import render
from .models import Expense
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializer import ExpenseSerializer
from rest_framework import permissions
from .permissions import IsOwner

class ExpenseListAPIView(ListCreateAPIView):
    serializer_class=ExpenseSerializer
    queryset = Expense.objects.all()
    permissions = (permissions.IsAuthenticated,)

    # overide a class
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.user)

class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=ExpenseSerializer
    queryset = Expense.objects.all()
    permissions = (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"

    # overide a class
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.user)