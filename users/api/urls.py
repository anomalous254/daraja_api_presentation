from django.urls import path
from .views import HandleCallBackView, STKPushView, PaymentStatusView


urlpatterns = [
    path('mpesa/stkpush/', STKPushView.as_view(), name='make_stkpush'),
    path('mpesa/zoomit/', HandleCallBackView.as_view(), name='handle_callback'),
    path('mpesa/status/<str:transaction_id>', PaymentStatusView.as_view(), name='transaction_status'),
]