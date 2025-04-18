from .models import Order, OrderItem
import os
import importlib.util
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404

# 載入 ECPay SDK
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "ecpay", "ecpay_payment_sdk.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EcpayPayment:
    @staticmethod
    def create_order_payment(request, order_id):
        """
        建立綠界訂單 - 簡化版本
        """
        order = get_object_or_404(Order, id=order_id)

        # 固定使用 ngrok 網址
        domain = 'https://432e-211-23-144-132.ngrok-free.app'

        # 建立綠界SDK實體
        ecpay_payment_sdk = module.ECPayPaymentSdk(
            MerchantID='3002607',  # 測試用 MerchantID
            HashKey='pwFHCqoQZGmho4w6',  # 測試用 HashKey
            HashIV='EkRm7iFT261dpevs'  # 測試用 HashIV
        )

        # 將Decimal轉為整數
        total_amount = int(float(order.total))

        # 簡單的訂單編號
        merchant_trade_no = f"SE{order.id}{int(datetime.now().timestamp())}"[
            :20]

        # 基本參數設定 - 只保留必要的參數
        order_params = {
            'MerchantTradeNo': merchant_trade_no,
            'MerchantTradeDate': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'PaymentType': 'aio',
            'TotalAmount': 6666,
            'TradeDesc': 'Simple Order',
            'ItemName': '商品訂單',
            'ReturnURL': f'{domain}/ecpay-payment-return/',
            # 'ClientBackURL': f'{domain}/order/{order.id}/',
            'ClientBackURL': 'https://www.google.com.tw/?hl=zh_TW',  # 交易成功後 按下返回商店會去的url
            'ChoosePayment': 'Credit',
            'EncryptType': 1,
            'CustomField1': str(order.id),  # 自訂欄位，為了付款成功後，回傳之後取得這筆訂單的id
        }

        try:
            # 測試環境
            action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'

            # 產生綠界訂單參數並生成HTML表單
            params = ecpay_payment_sdk.create_order(order_params)
            trade_info = ecpay_payment_sdk.gen_html_post_form(
                action_url, params)

        except Exception as e:
            print(f"生成綠界訂單錯誤: {str(e)}")
            trade_info = f"<p>訂單建立失敗</p>"

        return render(request, 'store/ecpay_payment.html', {'trade_info': trade_info})


@csrf_exempt
def ecpay_payment_return(request):
    """
    綠界回傳付款結果 (ReturnURL)
    """
    if request.method == 'POST':
        # 接收綠界回傳的付款資訊
        payment_data = request.POST.dict()
        print("綠界付款結果(這是綠界回傳的資料):", payment_data)
        print("綠界付款結果RtnCode(這是綠界回傳的資料):", payment_data.get('RtnCode'))
        print("FUCK YOUUUUUUUUUUUU")
        # 交易成功時更新訂單狀態
        if payment_data.get('RtnCode') == '1':
            order_id = payment_data.get('CustomField1')
            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    order.status = 'Accepted'
                    order.save()
                except Order.DoesNotExist:
                    pass

        # 回應綠界
        return HttpResponse('1|OK')

    return HttpResponse('Not Allowed', status=405)
