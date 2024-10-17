from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
# ViewSets for different models
from django.db.models import Q, Avg
from rest_framework.permissions import AllowAny
from knox.models import AuthToken
# from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import json
from .models import *
from .serializer import *

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class EditorialViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UsersLibrotekaViewSet(viewsets.ModelViewSet):
    queryset = UsersLibroteka.objects.all()
    serializer_class = UsersLibrotekaSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class LibrosView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        books = Book.objects.all()
        books_data = BookSerializer(books, many=True).data
        return Response(books_data, status=status.HTTP_200_OK)
    

class BusquedaLibrosView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        criterio = request.GET.get('criterio')
        value = request.GET.get('value')

        if not criterio or not value:
            return Response({'error': 'Criterio y valor son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        if criterio == 'author':
            books = Book.objects.filter(id_Author__name__icontains=value)
        elif criterio == 'genre':
            books = Book.objects.filter(id_Genre__name__icontains=value)
        elif criterio == 'editorial':
            books = Book.objects.filter(id_Editorial__name__icontains=value)
        elif criterio == 'title':
            books = Book.objects.filter(title__icontains=value)
        else:
            return Response({'error': 'Criterio de búsqueda no válido'}, status=status.HTTP_400_BAD_REQUEST)
        if not books.exists():
            return Response({'message': 'No se encontraron libros que coincidan con la búsqueda'}, status=status.HTTP_200_OK)  
        books_data = BookSerializer(books, many=True).data
        return Response(books_data, status=status.HTTP_200_OK)

class GetBooksByAuthorOrGenreOrTitleView(View):
    def get(self, request, *args, **kwargs):
        criterio = kwargs.get('criterio')
        value = kwargs.get('value')
        if criterio == 'author':
            books = Book.objects.filter(id_Author__name__icontains=value)
        elif criterio == 'genre':
            books = Book.objects.filter(id_Genre__name__icontains=value)
        elif criterio == 'editorial':
            books = Book.objects.filter(id_Editorial__name__icontains=value)
        else:
            return JsonResponse({'error': 'Invalid search criterion'}, status=400)
        data = [{'title': book.title, 
                 'author': book.id_Author.name, 
                 'genre': book.id_Genre.name, 
                 'editorial': book.id_Editorial.name,
                 'description': book.description,
                 'price': book.price,
                 'stock': book.stock} for book in books]
        return JsonResponse(data, safe=False)
   
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = UsersLibroteka.objects.get(email=email)
                if check_password(password, user.password):
                    return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except UsersLibroteka.DoesNotExist:
                return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Login API
# @csrf_exempt

# class LoginAPI(KnoxLoginView):
#     permission_classes = [permissions.AllowAny]

    # def post(self, request, format=None):
    #     serializer = AuthTokenSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     login(request, user)
    #     return super().post(request, format=None)
# ---
    # def post(self, request, format=None):
    #     serializer = AuthTokenSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     login(request, user)
    #     return super(LoginAPI, self).post(request, format=None)
    # def login_view(request):
    #     if request.method == 'POST':
    #         data = json.loads(request.body)
    #         email = data.get('email')
    #         password = data.get('password')
# --       
    #     try:
    #         user = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         return JsonResponse({'message': 'Invalid email or password'}, status=401)
        
    #     user = authenticate(username=user.username, password=password)
        
    #     if user is not None:
    #         login(request, user)
    #         return JsonResponse({'message': 'Login successful', 'user': {'username': user.username, 'email': user.email}})
    #     else:
    #         return JsonResponse({'message': 'Invalid email or password'}, status=401)
    #     return JsonResponse({'message': 'Method not allowed'}, status=405)

class RoleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]

class RoleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]        


class UsersLibrotekaListCreate(APIView):
    def get(self, request):
        users = UsersLibroteka.objects.all()
        serializer = UsersLibrotekaSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsersLibrotekaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateOrderView(APIView):
    def post(self, request):
        user_email = request.data.get('id_User')
        user = get_object_or_404(UsersLibroteka, email=user_email)
        try:
            user = UsersLibroteka.objects.get(email=user_email)
        except UsersLibroteka.DoesNotExist:
            # logger.error(f"User {user_email} does not exist.")
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        order_status_str = request.data.get('id_Order_Status')
        try:
            order_status = OrderStatus.objects.get(status=order_status_str)
        except OrderStatus.DoesNotExist:
            # logger.error(f"Order status {order_status_str} does not exist.")
            return Response({"message": "Order status does not exist"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'id_Order_Status': order_status.id_Order_Status,
            'id_User': user.email,
            'date': request.data.get('date'),
            'books': request.data.get('books'),
            'total': request.data.get('total'),
            'books_amount': request.data.get('books_amount')
        }

        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # logger.error(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         email = data.get('email')
#         password = data.get('password')
        
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return JsonResponse({'message': 'Invalid email or password'}, status=401)
        
#         user = authenticate(username=user.username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return JsonResponse({'message': 'Login successful', 'user': {'username': user.username, 'email': user.email}})
#         else:
#             return JsonResponse({'message': 'Invalid email or password'}, status=401)
#     return JsonResponse({'message': 'Method not allowed'}, status=405)

class FavoriteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
        if created:
            return Response({'message': 'Added to favorites'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Already in favorites'}, status=status.HTTP_200_OK)

    def delete(self, request):
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
        favorite = Favorite.objects.filter(user=request.user, book=book).first()
        if favorite:
            favorite.delete()
            return Response({'message': 'Removed from favorites'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Not in favorites'}, status=status.HTTP_404_NOT_FOUND)


class BookRatingView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_book_avg_rating(serializer.data['id_book'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        rating = get_object_or_404(Rating, pk=pk)
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Actualizar el promedio de valoraciones
            update_book_avg_rating(serializer.data['id_book'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rating = get_object_or_404(Rating, pk=pk)
        book_id = rating.id_book.id_Book  # Guardar el ID del libro antes de eliminar la valoración
        rating.delete()
        # Actualizar el promedio de valoraciones después de eliminar
        update_book_avg_rating(book_id)
        return Response(status=status.HTTP_204_NO_CONTENT)



def update_book_avg_rating(book):
    avg_rating = Rating.objects.filter(id_book=book).aggregate(Avg('rating'))['rating__avg'] or 0
    book.avg_rating = avg_rating
    book.save()
