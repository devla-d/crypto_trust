from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from datetime import timedelta,datetime


from crypto_trust import utils


from .models import Transactions,Notification,Card,Wallet,Trade,Bank,Kyc
from .forms import KycForm,UserUpdateForm
from superadmin.models import OngoingTrade


@login_required
def index_(request):
    return render(request, 'user/dashboard.html')



@login_required
def trading_history_(request):
    trades = Trade.objects.filter(user=request.user).order_by('-date')
    if request.POST:
        user = request.user
        trade_pk = request.POST.get('trade_id')
        print(trade_pk)
        trade = Trade.objects.get(user=user,pk=trade_pk)
        date =  trade.date.date().isoformat()
        return JsonResponse({"amount":trade.amount,"status":trade.status,"time":date,
            "type":trade.ty_pe,"symbol":trade.sysmbol,"exp_pay":trade.payout,"leverage":trade.leverage,
            "end_price":trade.end_amount(),"interval":trade.interval,"end_time":trade.end_date})
    return render(request,'user/trading-history.html',{"trades":trades})


@login_required
def withdraw_(request):
    if request.user.is_verified == False:
        messages.info(request,"Verify Your Account")
        return redirect('verification')
    if request.POST:
        user = request.user
        method = request.POST.get('w_method')
        #sender_id =  request.POST.get('sender_id')
        amount_coin =  request.POST.get('amount_coin')
        w_amount_usd =  int(request.POST.get('w_amount_usd'))
        if w_amount_usd > user.tot_balance:
            return JsonResponse({"msg":'low'})
        else:
            if method == 'BTC':
                wallet_addres_btc = request.POST.get('wallet_addres_btc')
                wallet = Wallet.objects.create(wallet_address=wallet_addres_btc,
                    coin_tpye="BTC", amount_in_coin= amount_coin )
                transaction = Transactions(user=user,amount=w_amount_usd,trans_type=utils.W,
                    wallet_detail=wallet)
                transaction.save()
                user.tot_balance -=  w_amount_usd
                user.save()
                return JsonResponse({'msg':'Done'})
            elif method == 'ETH':
                wallet_addres_eth = request.POST.get('wallet_addres_eth')
                wallet = Wallet.objects.create(wallet_address=wallet_addres_eth,
                    coin_tpye="ETH", amount_in_coin= amount_coin )
                transaction = Transactions(user=user,amount=w_amount_usd,trans_type=utils.W,
                    wallet_detail=wallet)
                transaction.save()
                user.tot_balance -=  w_amount_usd
                user.save()
                return JsonResponse({'msg':'Done'})
            elif method == 'Bank Transfer':
                w_amount_usd =  int(request.POST.get('w_amount_usd'))
                bank_type =   request.POST.get('bank')
                acc_number =  request.POST.get('acc_number')
                acc_name =  request.POST.get('acc_name')
                bank = Bank.objects.create(acc_name=acc_name,acc_num=acc_number,ty_pe=bank_type)
                transaction = Transactions(user=user,amount=w_amount_usd,trans_type=utils.W,
                    bank_details=bank)
                transaction.save()
                user.tot_balance -=  w_amount_usd
                user.save()
                return JsonResponse({'msg':'Done'})        
            else:
                return JsonResponse({'msg':'error'})
    return render(request,'user/withdraw.html')




@login_required
def transactions_(request):
    user = request.user
    transactions = Transactions.objects.filter(user=user).order_by('-date')
    if request.POST:
        user = request.user
        trans_id = request.POST.get('trans_id')
        transaction = Transactions.objects.get(user=user,pk=trans_id)
        method = ''
        if transaction.card_detail:
            method = "Card"
        elif transaction.bank_details:
            method = transaction.bank_details.ty_pe
        else:
            method = transaction.wallet_detail.coin_tpye
        date =  transaction.date.date().isoformat()
        return JsonResponse({"amount":transaction.amount,"status":transaction.status,"time":date,
            "type":transaction.trans_type,"method":method})
    return render(request,'user/transactions.html',{'transactions':transactions})




@login_required
def deposit_(request):
    if request.POST:
        mode = request.POST.get('mode')
        amount = request.POST.get('amount')
        depo_info = {"mode":mode,"amount":amount}
        expire_at = datetime.today() + timedelta(minutes=5)
        utils.set_expirable_var(request.session,'depo_info',depo_info,expire_at)
        print(request.session['depo_info'])
        return JsonResponse({"mode":mode,"amount":amount})
    return render(request,'user/deposit.html')



#@csrf_exempt
def process_deposit(request):
    mode_type = request.POST.get('mode_type')
    print(mode_type)
    if mode_type == 'mode_btc':
        amount_btc = request.POST.get('amount_btc')
        amount_usd = request.POST.get('amount_usd')
        transaction = Transactions(user= request.user, amount=amount_usd,trans_type=utils.D)
        wallet = Wallet.objects.create(coin_tpye='BTC',amount_in_coin=amount_btc)
        transaction.wallet_detail = wallet
        transaction.save()
        return JsonResponse({'msg':"Request Pending"})
    elif  mode_type == "mode_eth":
        amount_eth = request.POST.get('amount_eth')
        amount_usd = request.POST.get('amount_usd2')
        transaction = Transactions(user= request.user, amount=amount_usd,trans_type=utils.D)
        wallet = Wallet.objects.create(coin_tpye='ETH',amount_in_coin=amount_eth)
        transaction.wallet_detail = wallet
        transaction.save()
        return JsonResponse({'msg':"Request Pending"})
    elif  mode_type == 'mode_card':
        masterAmount = request.POST.get('txtamount')
        cardName = request.POST.get('txtcardname')
        cardNumber = request.POST.get('txtnumber')
        cardMonth = request.POST.get('txtcardmon')
        cardYear = request.POST.get('txtcardyear')
        cardCvv = request.POST.get('txtcvv')
        billFirst = request.POST.get('txtbillFirst')
        billLast = request.POST.get('txtbilllast')
        billEmail = request.POST.get('txtBillemail')
        billPhone = request.POST.get('txtBillphone')
        billStreet = request.POST.get('txtBillstreet')
        billTown = request.POST.get('txtBillTown')
        billCountry = request.POST.get('txtBillcountry')
        billPostal = request.POST.get('txtBillpostal')
        user = request.user
        card = Card.objects.create(
            name_on_card = cardName,card_number=cardNumber,exp_month=cardMonth,
            exp_year = cardYear,cvv=cardCvv,first_name=billFirst,last_name=billLast,
            email=billEmail,phone=billPhone,street_address=billStreet,
            town_city=billTown,country=billCountry,postal_code=billPostal
        )
        transaction = Transactions(user= request.user, amount=masterAmount,trans_type=utils.D)
        transaction.card_detail = card
        transaction.save()
        return JsonResponse({"msg":"request pending"})
    else:
        return JsonResponse({"error":"UNKNOWN ERROR OCCURED"})

@login_required
def trade_(request):
    if request.POST:
        user = request.user
        ty_pe = request.POST.get('trade_ty_pe')
        amount = int(request.POST.get("amount"))
        leverage = request.POST.get('leverage')
        interval = int(request.POST.get('interval'))
        sysmbol = request.POST.get('symbol')
        status  = "pending"
        end_date = timezone.now() + timedelta(minutes=interval)
        if user.deposit_balance > amount:
            trade = Trade(user=user,ty_pe=ty_pe,amount=amount,leverage=leverage,interval=interval,
                        sysmbol=sysmbol,status=status,end_date=end_date)
            trade.save()
            user.deposit_balance -= amount
            user.tot_amount_invested += amount
            user.save()
            return JsonResponse({'msg':"Trading Successfull"})
        else:
            return JsonResponse({'msg':"Insufficient Balance"})
    return render(request,'user/trade.html')







@login_required
def verification_(request):
    try:
        doc = Kyc.objects.get(user=request.user)
    except Kyc.DoesNotExist:
        doc = None
    user = request.user
    if request.POST:
        form = KycForm(request.POST,request.FILES)
        if form.is_valid():
            if doc:
                name = form.cleaned_data['name']
                number = form.cleaned_data['number'] 
                country_issued = form.cleaned_data['country_issued'] 
                ssn = form.cleaned_data['ssn'] 
                document_front = form.cleaned_data['document_front'] 
                document_back = form.cleaned_data['document_back']



                doc.name = name
                doc.number = number
                doc.country_issued = country_issued
                doc.ssn = ssn
                doc.document_front = document_front
                doc.document_back = document_back
                doc.user = user
                doc.status = 'Proccessing'
                doc.save()
                messages.info(request,("Document Submited"))
                return redirect('verification')



            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            #user.is_verified = True
            #user.save()sss
            messages.info(request,("Document Submited"))
            return redirect('verification')
        else:
            messages.info(request,("UNKNOWN ERROR OCCURED"))
            return redirect('verification')
    return render(request,'user/verification.html',{'doc':doc})





@login_required
def account_(request):
    user = request.user
    if request.POST:
        form = UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request,'Account Updated')
            return redirect('account')
        else:
            return JsonResponse({"err":form.error})
    else:
        form = UserUpdateForm(instance=user)
    return render(request,'user/account.html',{"form":form})





@login_required
def notification_(request):
    user = request.user
    notification = Notification.objects.filter(user=user).order_by('-date')
    return render(request,'user/notifications.html',{"notification":notification})




@login_required
def process_trade(request):
    if request.POST:
        trade_id = request.POST.get('trade_id')
        user = request.user
        try:
            trade = Trade.objects.get(pk=trade_id)
        except Trade.DoesNotExist:
            trade = None
        if trade:
            try:
                ongoingtrade = OngoingTrade.objects.get(amount=trade.amount,sysmbol=trade.sysmbol,interval=trade.interval,leverage=trade.leverage)
            except OngoingTrade.DoesNotExist:
                ongoingtrade = None
            if ongoingtrade:
                trade.status = "gain"
                trade.payout = ongoingtrade.pay
                user.tot_balance += ongoingtrade.pay
                user.save()
                trade.save()
                return JsonResponse({'msg':"Trading Gain"})
            else:
                trade.status = "loss"
                trade.payout = ongoingtrade.pay
                trade.save()
                return JsonResponse({'msg':"Trade Loss"})
        else:
            return JsonResponse({'msg':"Error"})
    else:
        return JsonResponse({'msg':"GET REQUEST NOT ACCEPTED"})
