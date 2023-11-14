from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import BlogSerializer
from .serializers import RegisterSerializer
from .models import Blog
from django.contrib.auth import authenticate, login, logout


class BlogList(APIView):
    """
    List all the blogs or create a new one
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        try:
            blogs = Blog.objects.all()
            if blogs:
                serialized_blogs = BlogSerializer(blogs, many=True)
                return Response({'response': serialized_blogs.data}, status=status.HTTP_200_OK)
            else:
                return Response({'response': 'No blogs Found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # log e
            return Response({'response': f'Something Went Wrong - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            blog = BlogSerializer(data=request.data)
            if blog.is_valid():
                blog.save()
                return Response({'response': 'Blog created successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'response': blog.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # log e
            return Response({'response': 'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlogActions(APIView):
    """
    Return a single blog, update and delete blog
    """

    def get_blog(self, pk):
        return Blog.objects.get(pk=pk)

    def get(self, request, pk):
        try:
            blog = self.get_blog(pk)
            serialized_blog = BlogSerializer(blog, many=False)
            return Response({'response': serialized_blog.data}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'response': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'response': 'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            blog = BlogSerializer(data=request.data)
            if blog.is_valid():
                blog.save()
                return Response({'response': 'Blog created successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'response': blog.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # log e
            return Response({'response': 'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            blog = self.get_blog(pk)
            updated_blog = BlogSerializer(instance=blog, data=request.data)

            if updated_blog.is_valid():
                updated_blog.save()
                return Response({'response': 'Blog updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'response': updated_blog.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist:
            return Response({'response': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'response': 'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            blog = self.get_blog(pk)
            updated_blog = BlogSerializer(instance=blog, data=request.data, partial=True)

            if updated_blog.is_valid():
                updated_blog.save()
                return Response({'response': 'Blog updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'response': updated_blog.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Blog.DoesNotExist:
            return Response({'response': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'response': 'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            blog = self.get_blog(pk)
            blog.delete()
            return Response({'response': 'Blog deleted successfully'}, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({'response': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'response': 'Something Went Wrong '}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):
    """
    User authentication with JWT
    """

    def post(self, request):
        try:
            if 'email' not in request.data or 'password' not in request.data:
                return Response({'response': 'Credentials is must to login'}, status=status.HTTP_400_BAD_REQUEST)

            email = request.data['email']
            password = request.data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'response': 'Logged in successfully',
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token)
                }, status=status.HTTP_200_OK)

            return Response({'response': 'email or password is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'response': 'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Logout(APIView):
    """
    Log out the user
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'response': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'response': f'Something Went Wrong - {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Register(APIView):
    """
    User registration
    """

    def post(self, request):
        user = RegisterSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({'response': 'Registered successfully'}, status=status.HTTP_201_CREATED)

        return Response({'response': user.errors}, status=status.HTTP_400_BAD_REQUEST)
