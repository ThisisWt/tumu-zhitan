from django.shortcuts import render
from django import forms
from utils.GetImg import DownloadClimateImg
import os

class ClimateDownloadForm(forms.Form):
    target = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'id': 'MyTarget', 'placeholder': "请输入", 'class': 'form-control'}),
        error_messages={"required": "该字段不能为空"},
        label='目标'
    )


def test(request):
    title = "CLIMATE"
    if request.method == 'GET':
        return render(request, 'test.html')
    elif request.method == 'POST':
        path = r"/utils/GetImg.py"
        os.system(path)
        return render(request, 'test.html')


# Create your views here.


