from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id_Author', 'name']

class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id_Editorial', 'name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id_Genre', 'name']

class BookSerializer(serializers.ModelSerializer):
    id_Author = AuthorSerializer()
    id_Genre = GenreSerializer()
    id_Editorial = EditorialSerializer()
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Book
        fields = ['id_Book', 'title', 'id_Author', 'id_Genre', 'id_Editorial', 'description', 'price', 'stock', 'avg_rating']

    def create(self, validated_data):
            author_data = validated_data.pop('id_Author', None)
            genre_data = validated_data.pop('id_Genre', None)
            editorial_data = validated_data.pop('id_Editorial', None)

            # Crear o recuperar las instancias relacionadas
            author = self.get_or_create_author(author_data)
            genre = self.get_or_create_genre(genre_data)
            editorial = self.get_or_create_editorial(editorial_data)

            # Verificar si el libro ya existe
            if Book.objects.filter(title=validated_data['title']).exists():
                raise serializers.ValidationError({"detail": "Este libro ya está registrado."})

            # Crear el libro con los datos relacionados
            book = Book.objects.create(
                id_Author=author,
                id_Genre=genre,
                id_Editorial=editorial,
                **validated_data
            )
            return book

    '''            try:
                author = Author.objects.get(name=author_data['name'])
                genre = Genre.objects.get(name=genre_data['name'])
                editorial = Editorial.objects.get(name=editorial_data['name'])
            except (Author.DoesNotExist, Genre.DoesNotExist, Editorial.DoesNotExist):
                # Si no se encuentra, crear nuevos registros
                author = Author.objects.create(**author_data)
                genre = Genre.objects.create(**genre_data)
                editorial = Editorial.objects.create(**editorial_data)

            # Verificar si el libro ya existe
            existing_book = Book.objects.filter(title=validated_data['title']).first()
            if existing_book:
                raise serializers.ValidationError({"detail": "Este libro ya está registrado."})

            # Crear el libro con los IDs obtenidos o nuevos si no existían
            book = Book.objects.create(
                id_Author=author,
                id_Genre=genre,
                id_Editorial=editorial,
                **validated_data
            )
            return book
        '''

    
    def update(self, instance, validated_data):
        author_data = validated_data.get('id_Author', None)
        genre_data = validated_data.get('id_Genre', None)
        editorial_data = validated_data.get('id_Editorial', None)
                # Actualizar relaciones si es necesario
        if author_data:
            instance.id_Author = self.get_or_create_author(author_data)
        if genre_data:
            instance.id_Genre = self.get_or_create_genre(genre_data)
        if editorial_data:
            instance.id_Editorial = self.get_or_create_editorial(editorial_data)

        # Actualizar otros campos
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)

        instance.save()

        return instance

    def get_or_create_author(self, author_data):
        return Author.objects.get_or_create(name=author_data['name'])[0]

    def get_or_create_genre(self, genre_data):
        return Genre.objects.get_or_create(name=genre_data['name'])[0]

    def get_or_create_editorial(self, editorial_data):
        return Editorial.objects.get_or_create(name=editorial_data['name'])[0]
    '''
            if author_data:
                author_serializer = AuthorSerializer(instance.id_Author, data=author_data)
                if author_serializer.is_valid(raise_exception=True):
                    author_serializer.save()

            if genre_data:
                genre_serializer = GenreSerializer(instance.id_Genre, data=genre_data)
                if genre_serializer.is_valid(raise_exception=True):
                    genre_serializer.save()

            if editorial_data:
                editorial_serializer = EditorialSerializer(instance.id_Editorial, data=editorial_data)
                if editorial_serializer.is_valid(raise_exception=True):
                    editorial_serializer.save()

            instance.description = validated_data.get('description', instance.description)
            instance.price = validated_data.get('price', instance.price)
            instance.stock = validated_data.get('stock', instance.stock)

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()

            return instance
    '''
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'dni']
class UserLibrotekaSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'dni'] 

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['email'], 
            validated_data['password']
        )
        return user        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'dni')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], 
            email=validated_data['email'], 
            password=validated_data['password'],
            dni=validated_data.get('dni') 
        )
        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Role
        fields = ['id', 'name', 'description']     



class UsersLibrotekaSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UsersLibroteka
        fields = ['username', 'first_name', 'last_name', 'dni', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class OrderSerializer(serializers.ModelSerializer):
    # books = serializers.JSONField()
    class Meta:
        model = Order
        fields = '__all__'

        # fields = ['id_Order_Status', 'id_User', 'date', 'books', 'total', 'books_amount']


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'


# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = LoginSerializer(data=data)
        
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)
#             return JsonResponse({'message': 'Login successful', 'user': {'username': user.username, 'email': user.email}})
#         return JsonResponse(serializer.errors, status=400)
#     return JsonResponse({'message': 'Method not allowed'}, status=405)

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'id_user', 'id_book', 'created_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'id_user', 'id_book', 'rating', 'created_at', 'updated_at']