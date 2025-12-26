from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Freelancer, Lead, CallStatus
from .serializer import UserSerializer, Leads, Freelance, CallStatusSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings   
from serpapi import GoogleSearch
from rest_framework_simplejwt.tokens import RefreshToken



class CreateUser(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")

        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "token": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Freelancer_details(request):
    skills = request.data.get('skills')
    if not skills:
        return Response({'error': "skills are required"}, status=status.HTTP_400_BAD_REQUEST)

    freelancer_data = {
        "user": request.user.id,  # use authenticated user
        "skills": skills,
    }

    serializer = Freelance(data=freelancer_data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_bussines_details(request):
    if not request.user or not request.user.is_authenticated:
        return Response({"error": "user is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        freelancer = Freelancer.objects.get(user=request.user)
    except Freelancer.DoesNotExist:
        return Response({"error": "Freelancer profile not found. Please complete your profile first."}, status=status.HTTP_400_BAD_REQUEST)

    location = request.data.get('location')
    query = request.data.get('business')
    if not location or not query:
        return Response({"error": "location and business query required"}, status=status.HTTP_400_BAD_REQUEST)

    if not hasattr(settings, 'MAP_API_KEY') or not settings.MAP_API_KEY:
        return Response({"error": "API key not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        params = {
            'engine': 'google_maps',
            'q': f'{query} in {location}',
            'type': 'search',
            'api_key': settings.MAP_API_KEY,
            'num': 10,
        }

        print(f"Searching with params: {params}") 
        search = GoogleSearch(params)
        results = search.get_dict()

        print(f"SerpApi response keys: {list(results.keys())}")

        # Determine which results to use
        business_results = None
        for key in ['local_results', 'local_pack', 'organic_results', 'search_results', 'results']:
            if key in results and results[key]:
                business_results = results[key]
                break

        if not business_results:
            # fallback to any list-of-dict with 'name' or 'title'
            for key, value in results.items():
                if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                    if any('title' in item or 'name' in item for item in value):
                        business_results = value
                        break

        if not business_results:
            return Response({
                "error": "No business data found for this search",
                "debug": {
                    "response_keys": list(results.keys()),
                    "query": f"{query} in {location}",
                    "api_key_set": bool(settings.MAP_API_KEY)
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        business_data = []

        for biz in business_results:
            if not isinstance(biz, dict):
                print(f"Skipping non-dict result: {biz}")
                continue

            lead_data = {
                'name': biz.get("title") or biz.get("name") or biz.get("business_name") or '',
                'phone': biz.get("phone") or biz.get("telephone") or '',
                'email': biz.get("email") or '',
                'rating': biz.get("rating") or biz.get("stars") or '',
                'address': biz.get("address") or biz.get("location") or biz.get("snippet") or '',
                'website': biz.get("website") or biz.get("link") or '',
                # removed 'claimed' because model does not have it
                'freelancer': freelancer  # add freelancer here
            }

            serializer = Leads(data= lead_data, context = {'freelancer': freelancer})
            if serializer.is_valid():
                lead_instance = serializer.save()
                business_data.append(serializer.data)
            else:
                print(f"Lead validation errors: {serializer.errors}")


        if not business_data:
            return Response({"error": "No valid business data could be processed"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": business_data}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"SerpApi error: {str(e)}")
        return Response({"error": f"Error fetching business data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class delete_lead(generics.DestroyAPIView):
    serializer_class = Leads
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        freelancer = Freelancer.objects.get(user=self.request.user)
        return Lead.objects.filter(freelancer=freelancer)
    






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_leads(request):
    try:
        freelancer = Freelancer.objects.get(user=request.user)
    except Freelancer.DoesNotExist:
        return Response(
            {"error": "Freelancer profile not found. Please complete your profile first."},
            status=status.HTTP_400_BAD_REQUEST
        )

    leads = Lead.objects.filter(freelancer=freelancer)

    data = []
    for lead in leads:
        data.append({
            'id': lead.id,
            "name": lead.name,
            "phone": lead.phone,
            "email": lead.email,
            "address": lead.address,
            "website": lead.website,
            "rating": lead.rating,
            "freelancer": freelancer.id,  # ✅ return ID instead of object
        })

    return Response(data, status=status.HTTP_200_OK) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_details(request):
    try:
        profile = Freelancer.objects.filter(user=request.user)
    except Freelancer.DoesNotExist:
        return Response({"error" : "Freelance profile not found. please complete your profile first"}, status=status.HTTP_400_BAD_REQUEST)
    
    data = []

    for profile_data in profile:
        data.append({
            'id' : profile_data.id,
            'user' : profile_data.user.username,
            'skills' : profile_data.skills,
        })

    return Response(data, status=status.HTTP_200_OK)

    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_profile_details(request):
    user = request.user 
    username = request.data.get('username')
    password = request.data.get("password")

    if username:
        user.username = username
    if password:
        user.set_password(password)
    user.save()

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def toggle_call_status(request, lead_id):
    try:
        lead = Lead.objects.get(id=lead_id, freelancer__user=request.user)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)

    call_status, created = CallStatus.objects.get_or_create(lead=lead)

    if request.method == 'GET':
        serializer = CallStatusSerializer(call_status)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CallStatusSerializer(call_status, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Call status updated", "called": serializer.data['called']})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
