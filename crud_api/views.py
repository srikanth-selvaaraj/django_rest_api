from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogSerializer
from .models import Blog
from json import load


@api_view(['GET'])
def list_blogs(request):
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


@api_view(['POST'])
def create_blog(request):
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


@api_view(['GET'])
def get_blog(reqeust, pk):
    try:
        blog = Blog.objects.get(pk=pk)
        serialized_blog = BlogSerializer(blog, many=False)
        return Response({'response': serialized_blog.data}, status=status.HTTP_200_OK)
    except Blog.DoesNotExist:
        return Response({'response': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return (Response({'response': 'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR))


@api_view(['PUT', 'PATCH'])
def update_blog(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
        if request.method == 'PUT':
            updated_blog = BlogSerializer(instance=blog, data=request.data)
        else:
            updated_blog = BlogSerializer(instance=blog, data=request.data, partial=True)

        if updated_blog.is_valid():
            updated_blog.save()
            return Response({'response': 'Blog updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'response': updated_blog.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Blog.DoesNotExist:
        return Response({'response': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return (Response({'response': f'Something Went Wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR))


@api_view(['DELETE'])
def delete_blog(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
        blog.delete()
        return Response({'response': 'Blog updated successfully'}, status=status.HTTP_200_OK)
    except Blog.DoesNotExist:
        return Response({'response': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'response': 'Something Went Wrong '}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
