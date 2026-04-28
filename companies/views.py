from rest_framework import generics, status
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer
from .permissions import IsRecruiter

class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsRecruiter] # <--- THE GATEKEEPER

    def perform_create(self, serializer):
        # SECURELY attach the logged-in user as the owner
        # The user cannot fake this because it comes from the JWT token, not the JSON body!
        serializer.save(owner=self.request.user)