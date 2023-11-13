from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogSerializer
from .models import Blog


class BlogList(APIView):
    """
    List all the blogs or create a new one
    """

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
            return Response({'response': 'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
