# Trong thư mục của ứng dụng của bạn, tạo hoặc mở file forms.py

# Tạo hoặc thêm nội dung sau vào file forms.py
from django import forms

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')
