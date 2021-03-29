from django.shortcuts import render

# Create your views here.
from travler.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
import requests
from .custom_permission import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404

"""
 Home View
"""


def home(request):
    return HttpResponse('Welcome to home page')


"""
User Profile View
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userprofile(request, pk):
    try:
        user_profile = UserProfile.objects.get(id=pk)
        serializer = UserProfileSerializer(user_profile, many=False)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userprofile_create(request):
    account = request.user
    user_profile = UserProfile(user=account)
    serializer = PostSerializer(user_profile, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def userprofile_edit(request, pk):
    try:
        user_profile = UserProfile.objects.get(id=pk)
        if user_profile.user != request.user:
            return Response('you do not have permission to edit this profile')
        else:
            serializer = UserProfileSerializer(instance=user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def userprofile_delete(request, pk):
    try:
        user_profile = UserProfile.objects.get(id=pk)
        if user_profile.user != request.user:
            return Response('you do not have permission to delete this profile')
        else:
            user_profile.delete()
            return Response('Profile was successfully deleted !!')
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


"""
Post api View
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def post_view(request, pk):
    """
    view a Post.
    """
    post = get_object_or_404(Post, id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def post_create(request):
    """
    Create a new Post.
    """
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
# only the publishers have the permission to edit their post
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def post_update(request, pk):
    """
    Update an existing Post.
    """
    post = get_object_or_404(Post, id=pk)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response('Post successfully updated')
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def post_delete(request, pk):
    """
    Delete an existing Post.
    """
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return Response('Post successfully deleted!!')


"""
Messages View
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_read(request, pk):
    try:
        recipient = Message.objects.get(id=pk)
        if request.user != recipient.recipient or recipient.sender:
            return Response('you do not have permission to read this message !!')
        else:
            serializer = MessageSerializer(recipient, many=False)
            return Response(serializer.data)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message_sent(request):
    account = request.user
    sender = Message(user=account)
    serializer = MessageSerializer(sender, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def message_edit(request, pk):
    try:
        message = Message.objects.get(id=pk)

        if message.sender != request.user:
            return Response('you do not have permission to edit this message !!')
        else:
            serializer = MessageSerializer(instance=message, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def message_delete(request, pk):
    try:
        message = Message.objects.get(id=pk)
        if message.sender != request.user:
            return Response('you do not have permission to delete this message!! ')
        else:
            message.delete()
            return Response('Message was successfully deleted !!')
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def visit_view(request, pk):
    """
    view a visit.
    """
    try:
        visit = Visit.objects.get(id=pk)
        serializer = VisitSerializer(visit, many=False)
        return Response(serializer.data)
    except Visit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def visit_create(request):
    """
    Create a new visit.
    """
    account = request.user
    visit = Visit(user=account)
    serializer = VisitSerializer(visit, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def visit_update(request, pk):
    """
    Update visit.
    """
    try:
        visit = Visit.objects.get(id=pk)
        if visit.user != request.user:
            return Response('you do not have permission to edit this user visit')
        else:
            serializer = WorkPlaceSerializer(instance=visit, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('Visit successfully updated')
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Visit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def visit_delete(request, pk):
    try:
        visit = Visit.objects.get(id=pk)
        visit.delete()
        return Response('visit successfully deleted!!')
    except Visit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


"""
Location View
"""


@api_view(['GET'])
def location(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    url = 'http://ip-api.com/json/'
    temp = requests.get(url.format(ip)).json()
    location = Location.objects.create(country=temp['country'], city=temp['city'], long=temp['lat'], lat=temp['lon'])
    
    serializer = LocationSerializer(location, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def location_create(request):
    try:
        account = request.user
        loca = Location(user=account)
        serializer = LocationSerializer(loca, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def location_update(request, pk):
    try:
        loca = Location.objects.get(id=pk)
        if loca.user != request.user:
            return Response('you do not have permission to edit this Location !!')
        else:
            serializer = LocationSerializer(instance=loca, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def location_delete(request, pk):
    try:
        loca = Location.objects.get(id=pk)
        if loca.user != request.user:
            return Response('you do not have permission to delete this location !!')
        else:
            loca.delete()
            return Response('Location successfully deleted!!')
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


"""
work place api View
"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def work_place_view(request, pk):
    """
    view a work place.
    """
    try:
        work_place = WorkPlace.objects.get(id=pk)
        serializer = WorkPlaceSerializer(work_place, many=False)
        return Response(serializer.data)
    except WorkPlace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def work_place_create(request):
    """
    Create a new work place.
    """
    account = request.user
    work_place = WorkPlace(user=account)
    serializer = WorkPlaceSerializer(work_place, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def work_place_update(request, pk):
    """
    Update work place.
    """
    try:
        work_place = WorkPlace.objects.get(id=pk)
        if work_place.user != request.user:
            return Response('you do not have permission to edit this user work place')
        else:
            serializer = WorkPlaceSerializer(instance=work_place, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response('Work place successfully updated')
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except WorkPlace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def work_place_delete(request, pk):
    """
    Delete a work place.
    """
    try:
        work_place = WorkPlace.objects.get(id=pk)
        if work_place.user != request.user:
            return Response('you do not have permission to delete this user work place !!')
        else:
            work_place.delete()
            return Response('Work Place successfully deleted!!')
    except WorkPlace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)