from django.shortcuts import render , redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.utils.encoding import smart_str 
from .models import Profile  
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login,logout
from app.models import UserSession
import secrets
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
import uuid
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import ForgotPasswordForm
import json

from django.contrib.auth import get_user_model

User = get_user_model()

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def generate_session_id():
    return str(uuid.uuid4())

def Email(request):

    context={}
    return render(request,'app/Email.html',context)
  


def homechat(request):
    profiles = Profile.objects.all()
    
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        context = {'profile': profile, 'profiles': profiles}
    else:
        context = {'profiles': profiles}

    return render(request, 'app/homechat.html', context)


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists. Please choose a different one.')
            elif email and User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists. Please choose a different one.')
            else:
                try:
                    
                    user = form.save(commit=False)
                    user.is_active = False  # Đặt trạng thái is_active của người dùng là False
                    user.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Xác nhận đăng ký tài khoản'
                    message = render_to_string('app/Email.html', {
                        'user': user,
                        'domain': current_site.domain,
                    })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.content_subtype = 'html'
                    email.send()
                    messages.success(request, 'Đăng ký thành công! Vui lòng kiểm tra email để xác nhận tài khoản.')

                   
                except Exception as e:
                    print(f"Error creating user or sending email: {e}")
                    messages.error(request, 'Failed to create user or send confirmation email. Please try again later.')
    context = {'form': form}
    return render(request, 'app/register.html', context)

def logoutPage(request):
    # Tìm tất cả các phiên đăng nhập chưa được đánh dấu là đã logout của người dùng hiện tại
    user_sessions = UserSession.objects.filter(user=request.user, logout_time__isnull=True)

    # Cập nhật thời gian logout cho tất cả các phiên
    for user_session in user_sessions:
        user_session.logout_time = timezone.now()
        user_session.save()

    # Thực hiện logout từ Django
    django_logout(request)

    # Chuyển hướng đến trang đăng nhập
    return redirect('login')


def loginPage(request):
    

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
           
            # Tạo một phiên đăng nhập mới cho người dùng
            new_session = UserSession.objects.create(user=user, session_token=generate_session_token())
          
            return redirect('homechat')  # Chuyển hướng sau khi xác thực và tạo phiên đăng nhập thành công
        else:
            error_message = "Mật khẩu hoặc tài khoảng không đúng."
            context = {'error_message': error_message}
            return render(request, 'app/login.html', context)
    return render(request, 'app/login.html')  # Trả về trang đăng nhập nếu xác thực không thành công
def create_user_session(user, session_token,session_id):
    
    new_session = UserSession.objects.create(user=user, session_token=session_token ,session_id=session_id)

    return new_session

# Hàm để cập nhật thông tin đăng xuất cho một phiên đăng nhập
def update_logout_time(session_id):
    try:
        session = UserSession.objects.get(session_id)
        session.logout_time = timezone.now()
        session.save()
        return True
    except UserSession.DoesNotExist:
        return False

# Hàm để lấy các phiên đăng nhập của một người dùng
def get_user_sessions(user):
    user_sessions = UserSession.objects.filter(user=user)

    return user_sessions

def generate_session_token():
    return secrets.token_hex(16) 







def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        context = {'profile': profile}
        return render(request, 'app/profile.html', context)
    except Profile.DoesNotExist:
       
        messages.info(request, 'Bạn chưa có Profile. Vui lòng tạo Profile của bạn.')
        return redirect('edit')  # Chuyển hướng đến trang tạo Profile

@login_required




def edit(request):
    user = request.user

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        image = request.FILES.get('image')
        aboutme = request.POST.get('aboutme')
        location = request.POST.get('location')
        gender = request.POST.get('gender')
        education = request.POST.get('education')
        religion = request.POST.get('religion')
        relationship_status = request.POST.get('relationship_status')
        email = request.POST.get('email')

        # Cập nhật các trường
        profile.location = location
        profile.first_name = first_name
        profile.last_name = last_name
        profile.phone = phone
        profile.birthday = birthday

        # Kiểm tra xem người dùng đã chọn ảnh hay chưa
        if image:
            profile.image = image
        else:
            # Nếu không, sử dụng ảnh mặc định
            default_image_path = 'images/avt.png'
            with default_storage.open(default_image_path, 'rb') as f:
                default_content = ContentFile(f.read())
                profile.image.save('avt.png', default_content)

        profile.aboutme = aboutme
        profile.gender = gender
        profile.education = education
        profile.religion = religion
        profile.relationship_status = relationship_status
        profile.email = email

        profile.save()

        return redirect('profile')

    context = {'profile': profile}
    return render(request, 'app/edit.html', context)






def confirm_registration(request, user):
    user_obj = get_object_or_404(User, id=user)
    
    # Thực hiện xác nhận đăng ký tại đây (ví dụ: cập nhật trạng thái xác nhận)
    user_obj.is_active = True  # Đây chỉ là ví dụ, bạn cần thay đổi dựa trên logic của bạn
    user_obj.save()

    return render(request, 'app/confirm_registration.html', {'user': user_obj})

import random
import string
def generate_confirmation_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

from .models import ConfirmationCode

def forgot_password(request):
    if request.method == 'POST':
        # Lấy tên đăng nhập từ form quên mật khẩu
        username = request.POST.get('username')
        print("Username:", username) 

        try:
            # Tìm người dùng với tên đăng nhập cung cấp
            user = User.objects.get(username=username)
            
            # Tạo mã xác nhận và thiết lập hạn chế thời gian
            confirmation_code = generate_confirmation_code()
            expiration_date = timezone.now() + timedelta(minutes=1)  # Ví dụ: Mã hết hạn sau 1 phút
            
            # Lưu mã xác nhận vào cơ sở dữ liệu cho người dùng
            confirmation_obj, created = ConfirmationCode.objects.get_or_create(user=user)
            confirmation_obj.confirmation_code = confirmation_code
            confirmation_obj.expiration_date = expiration_date
            confirmation_obj.save()

            # Gửi mã xác nhận tới email của người dùng
            mail_subject = 'Xác nhận yêu cầu đặt lại mật khẩu'
            message = f"Mã xác nhận của bạn là: {confirmation_code}"
            email_to_send = EmailMessage(mail_subject, message, to=[user.email])
            email_to_send.send()

            # Chuyển hướng người dùng đến trang xác nhận mã
            return redirect('confirm_reset', user_id=user.id)
         
        except User.DoesNotExist:
            # Xử lý khi không tìm thấy người dùng với tên đăng nhập cung cấp
            error_message = "Tên đăng nhập không tồn tại trong hệ thống."
            form = ForgotPasswordForm()
            context = {'form': form, 'error_message': error_message}
            return render(request, 'app/login.html', context)
    else:
        form = ForgotPasswordForm()
        context = {'form': form }
        return render(request, 'app/forgot_password.html', context)


# views.py



from django.utils import timezone

def confirm_reset(request, user_id):
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')

        try:
            user = User.objects.get(pk=user_id)
            confirmation_obj = ConfirmationCode.objects.get(user=user, confirmation_code=confirmation_code)
            current_time = timezone.now()
            # Kiểm tra xem mã xác nhận có hết hạn chưa
            expiration_date = confirmation_obj.expiration_date
            if expiration_date < current_time:
                error_message = "Mã xác nhận đã hết hạn."
                context = {'error_message': error_message, 'user_id': user_id}
                return render(request, 'app/confirm_reset.html', context)
            else:
            # Nếu mã xác nhận vẫn còn hạn, tiếp tục xử lý và chuyển hướng
                uidb64 = urlsafe_base64_encode(force_bytes(user_id))
                token = default_token_generator.make_token(user)
                return redirect('reset_password', uidb64=uidb64, token=token)
        except ConfirmationCode.DoesNotExist:
            try:
                user = User.objects.get(pk=user_id)
                confirmation_obj = ConfirmationCode.objects.get(user=user)
                expiration_date = confirmation_obj.expiration_date
            except ConfirmationCode.DoesNotExist:
                expiration_date = None

            

            error_message = "Mã xác nhận không hợp lệ."
            context = {'error_message': error_message, 'user_id': user_id, 'expiration_date': expiration_date}
            return render(request, 'app/confirm_reset.html', context)
    else:
        # Lấy thông tin về thời hạn hết hạn của mã xác nhận
        try:
            user = User.objects.get(pk=user_id)
            confirmation_obj = ConfirmationCode.objects.get(user=user)
            expiration_date = confirmation_obj.expiration_date
        except ConfirmationCode.DoesNotExist:
            expiration_date = None

        context = {'user_id': user_id, 'expiration_date': expiration_date}
        return render(request, 'app/confirm_reset.html', context)


def resend_confirmation_code(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # Tạo mã xác nhận mới và lưu vào cơ sở dữ liệu
    confirmation_code = generate_confirmation_code()
    expiration_date = timezone.now() + timedelta(minutes=1)
    confirmation_obj, created = ConfirmationCode.objects.get_or_create(user=user)
    confirmation_obj.confirmation_code = confirmation_code
    confirmation_obj.expiration_date = expiration_date
    confirmation_obj.save()

    # Gửi mã xác nhận mới tới email của người dùng
    mail_subject = 'Xác nhận yêu cầu đặt lại mật khẩu (mã mới)'
    message = f"Mã xác nhận mới của bạn là: {confirmation_code}"
    email_to_send = EmailMessage(mail_subject, message, to=[user.email])
    email_to_send.send()

    # Chuyển hướng người dùng đến trang xác nhận mã
    return redirect('confirm_reset', user_id=user.id)




def base(request):
    # Xác nhận người dùng đã đăng nhập
    if request.user.is_authenticated:
        # Lấy thông tin hồ sơ của người dùng
        profile = get_object_or_404(Profile, user=request.user)
    else:
        # Nếu người dùng chưa đăng nhập, gán giá trị None cho profile
        profile = None
    
    context = {'profile': profile}
    return render(request, 'app/base.html', context)


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Xử lý mật khẩu mới và cập nhật cho người dùng
            password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, 'Mật khẩu đã được thay đổi thành công.')
                return redirect('login') # Chuyển hướng về trang đăng nhập sau khi thay đổi mật khẩu
            else:
                messages.error(request, 'Mật khẩu không khớp.')
        else:
            return render(request, 'app/reset_password.html')  # Hiển thị form nhập mật khẩu mới
    else:
        messages.error(request, 'Liên kết đã hết hạn hoặc không hợp lệ.')
        return redirect('login')  # Hoặc chuyển hướng về trang đăng nhập với thông báo lỗi

from django.http import JsonResponse
from .models import Message

# Trong views.py
from django.http import JsonResponse
from .models import Message

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def save_message(request):
    if request.method == 'POST':
        message_content = request.POST.get('message', '')
        username = request.POST.get('username', '')
        is_sender = request.POST.get('is_sender', '') == 'true'

        # Lấy đối tượng User của người gửi và người nhận
        sender_user = User.objects.get(username=username)
        receiver_user = request.user

        # Lưu tin nhắn vào CSDL
        Message.objects.create(sender=sender_user, receiver=receiver_user, content=message_content)

        return JsonResponse({'status': 'success', 'message': 'Message saved successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})






# @login_required
# def save_message(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         message_content = data.get('message', '')
#         receiver_username = data.get('receiver', '')

#         # Lấy đối tượng User của người nhận
#         receiver_user = User.objects.get(username=receiver_username)

#         # Lưu tin nhắn vào CSDL
#         Message.objects.create(sender=request.user, receiver=receiver_user, content=message_content)

#         return JsonResponse({'status': 'success', 'message': 'Message saved successfully'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
from operator import attrgetter
@login_required
def get_chat_history(request):
    # Lấy tất cả tin nhắn gửi đến hoặc nhận từ người dùng hiện tại
    messages = Message.objects.filter(receiver=request.user) | Message.objects.filter(sender=request.user)
    
    messages = sorted(messages, key=attrgetter('timestamp'))
    message_data = []

    for msg in messages:
        sender_profile = Profile.objects.get(user=msg.sender)
        receiver_profile = Profile.objects.get(user=msg.receiver)

        # Xác định xem người dùng hiện tại có phải là người gửi hay không
        is_sender = msg.sender == request.user

        # Thêm thông tin người gửi và người nhận vào dữ liệu tin nhắn
        message_data.append({
            'message': msg.content,
            'isSender': is_sender,
            'sender_username': msg.sender.username,
            'sender_image_url': sender_profile.image.url if sender_profile.image else None,
            'receiver_username': msg.receiver.username,
            'receiver_image_url': receiver_profile.image.url if receiver_profile.image else None,
        })

    return JsonResponse({'messages': message_data})


def change_password_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            # Kiểm tra xác thực mật khẩu hiện tại
            if not request.user.check_password(current_password):
                messages.error(request, 'Mật khẩu hiện tại không đúng.')
                return render(request, 'app/change_password.html', {'error_message': 'Mật khẩu hiện tại không đúng.'})

            # Kiểm tra mật khẩu mới và xác nhận mật khẩu
            if new_password != confirm_password:
                messages.error(request, 'Mật khẩu mới và xác nhận mật khẩu không khớp.')
                return render(request, 'app/change_password.html', {'error_message': 'Mật khẩu mới và xác nhận mật khẩu không khớp.'})

            # Đặt mật khẩu mới và lưu lại
            request.user.set_password(new_password)
            request.user.save()

            messages.success(request, 'Mật khẩu đã được thay đổi thành công, vui lòng đăng nhập lại.')
            return redirect('homechat')

        return render(request, 'app/change_password.html')
    else : 
        return redirect('login')


def friend_invitation_view(request):
    user = request.user
    received_invitations = FriendInvitation.objects.filter(receiver=user)
    sent_invitations = FriendInvitation.objects.filter(sender=user)
    return render(request, 'app/dsloimoikb.html',
                  {'received_invitations': received_invitations, 'sent_invitations': sent_invitations})

def send_friend_invitation(request, receiver_id):
    # Kiểm tra xem lời mời đã tồn tại chưa
    if FriendInvitation.objects.filter(sender=request.user, receiver_id=receiver_id).exists():
        messages.warning(request, 'Bạn đã gửi lời mời kết bạn đến người này rồi.')
    else:
        # Tạo lời mời mới
        FriendInvitation.objects.create(sender=request.user, receiver_id=receiver_id)
        messages.success(request, 'Lời mời kết bạn đã được gửi thành công.')

    return redirect('friend_invitations')

def friend_requests(request):
    # Lấy ra danh sách lời mời kết bạn chưa được chấp nhận của người dùng hiện tại
    friend_requests_received = FriendRequest.objects.filter(receiver=request.user, accepted=False)
    context = {'friend_requests_received': friend_requests_received}

    return render(request, 'app/dsloimoikb.html', context)

@login_required
def friendship_view(request):
    user = request.user
    friendships = Friendship.objects.filter(user=user)
    return render(request, 'app/dsbb.html', {'friendships': friendships})

# danh sach ban be
def friend_list(request, FriendList=None):
    # Lấy đối tượng FriendList của người dùng hiện tại
    friend_list, created = FriendList.objects.get_or_create(user=request.user)
    # Lấy danh sách bạn bè
    friends = friend_list.friends.all()
    context = {'friends': friends}
    return render(request, 'app/dsbb.html', context)

def accept_friend_request(request, request_id):
    # Xác nhận một lời mời kết bạn
    friend_request = FriendRequest.objects.get(pk=request_id)
    if friend_request.receiver == request.user:
        friend_request.accepted = True
        friend_request.save()
        messages.success(request, 'Lời mời kết bạn đã được chấp nhận.')
    else:
        messages.warning(request, 'Không thể chấp nhận lời mời kết bạn này.')
    return redirect('friend_requests')

def list(request):
    users = User.objects.all()
    return render(request, 'app/dskb.html', {'users': users})

def friend(request):
    return render(request, 'app/friend.html')