from rest_framework.views import APIView
from users.models import MPesaTransaction
from daraja_api.core import DarajaAPI
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema



class STKPushView(APIView):

    @swagger_auto_schema(auto_schema=None) 
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')


        transaction = MPesaTransaction.objects.create(
            user=request.user,
            phone_number=phone_number,
            amount=amount
        )
    
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        stk_push_url ='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

        daraja = DarajaAPI(
            url=url, 
            consumer_key= config('DARAJA_API_CONSUMER_KEY') , 
            consumer_secret=config('DARAJA_API_CONSUMER_SECRET'), 
            passkey=config('DARAJA_API_PASS_KEY'),
            shortcode=config('DARAJA_API_SHORT_CODE'),
            phone_number=phone_number
            )
                                                                                                         
        response = daraja.send_stk_push(url=stk_push_url)
        response_code = response.get('ResponseCode')
       
        # Success
        if response_code == '0':
            # Update transaction with the CheckoutRequestID if present
            transaction_id = response.get("CheckoutRequestID")
            transaction.transaction_id = transaction_id
            transaction.save()

            return Response(response, status=status.HTTP_200_OK)
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

       

class HandleCallBackView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(auto_schema=None) 
    def post(self, request, *args, **kwargs):
        # Assuming request.data contains the M-Pesa callback data
        mpesa_post_data = request.data
      
        
        try:
            # Extract necessary fields
            result_code = mpesa_post_data['Body']['stkCallback']['ResultCode']
        
            if result_code == 0:

                checkout_request_id = mpesa_post_data['Body']['stkCallback']['CheckoutRequestID']
                callback_metadata = mpesa_post_data['Body']['stkCallback']['CallbackMetadata']['Item']

                # Extract individual items from CallbackMetadata
                mpesa_receipt_number = next((item['Value'] for item in callback_metadata if item['Name'] == 'MpesaReceiptNumber'), None)
                transaction_date = next((item['Value'] for item in callback_metadata if item['Name'] == 'TransactionDate'), None)


                transaction = MPesaTransaction.objects.filter(transaction_id=checkout_request_id).first()

                if transaction:
                    transaction.transaction_date  = datetime.strptime(str(transaction_date), "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                    transaction.status = 'Success'
                    transaction.mpesa_receipt_number  = mpesa_receipt_number 
                    transaction.save()

                    return Response({"message": "Callback processed successfully"}, status=status.HTTP_200_OK)
            
            if result_code != 0:
                checkout_request_id = mpesa_post_data['Body']['stkCallback']['CheckoutRequestID']
                transaction = MPesaTransaction.objects.filter(transaction_id=checkout_request_id).first()
                if transaction:
                    transaction.status = 'Failed'
                    transaction.save()
                
            return Response({"message": "Callback process failed!"}, status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError as e:
            return Response({"error": "Invalid callback data"}, status=status.HTTP_400_BAD_REQUEST)
        



class PaymentStatusView(APIView):
    @swagger_auto_schema(auto_schema=None) 
    def get(self, request, transaction_id):
        transaction = MPesaTransaction.objects.filter(transaction_id=transaction_id).first()
        
        if not transaction:
            return Response({"status": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Return the current status of the transaction
        return Response({"status": transaction.status}, status=status.HTTP_200_OK)
