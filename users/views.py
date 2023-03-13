from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from .serializers import UserSerializer 
from rest_framework.response import Response
from .models import *
from bit68.models import *
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):


    def get(self, request):
        return render(request)
    
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    
    

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
#@login_required()
def add_to_cart(request, name, email):

    user_id  = User.objects.get(email= email)
    product = Product.objects.get(name= name)
    cart_item, status  = CartItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_cart, status  = Cart.objects.get_or_create(user=user_id, ordered=False)
    user_cart.items.add(cart_item)
    user_cart.total_price=user_cart.get_cart_total()
    
    user_cart.save()

    return HttpResponse('item added to cart')

def place_order(request, email):
#     field_name_list = []

#     user = User.objects.get(email= email)
#     cart  = Cart.objects.get(user_id= user.id)
#     cart_items = CartItem.objects.get(id= cart.id)
#     cart_items = cart_items.values(*field_name_list)
#     final_data = []
#     for elem in qs:
#         print(type(elem))
#         print(elem)
#     for v in elem.values():
#         final_data.append(v)
    # order_item, status  = OrderItem.objects.get_or_create()

    # # create order associated with the user
    # user_cart, status  = Order.objects.get_or_create(user=user_id)
    # user_cart.items.add(cart_item)
    # if status:
    #     user_cart.save()
    
    return HttpResponse('item added to cart')
