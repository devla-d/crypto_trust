from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone

from account.forms import AccountForm
from account.models import Account
from .decorators import manager_required
from users.models import Transactions,Notification,Card,Wallet,Trade,Bank,Kyc
from .models import OngoingTrade
from crypto_trust import utils

@manager_required
def index_(request):
    return render(request,'superadmin/index.html')



@manager_required
def users_(request):
    users = Account.objects.all().order_by('-last_login')
    #form = AccountForm()
    if request.POST:
        if request.POST.get('submit'):
            depoamount = int(request.POST.get('depoamount'))
            totamount  = int(request.POST.get('totamount'))
            pk = request.POST.get('user_pk')
            try:
                user = Account.objects.get(pk=pk)
                user.tot_balance = totamount
                user.deposit_balance = depoamount
                user.save()
                return JsonResponse({"msg":'success', "user_tot_bal":user.tot_balance,'user_depo_bal':user.deposit_balance})
            except Account.DoesNotExist:
                user = None
                return JsonResponse({'msg':"No Account Matching Query"})
        else:
            pk = request.POST.get('user_pk')
            try:
                user = Account.objects.get(pk=pk)
                return JsonResponse({"msg":'success','username':user.username,"user_pk" : user.id,
                "user_email":user.email,"user_phone":user.phone_number,"user_tot_bal":int(user.tot_balance),"user_amount_invested":int(user.tot_amount_invested),
                    "user_depo_bal":int(user.deposit_balance),
                    "user_with_bal":int(user.amount_withdraw),"user_ref":user.refferal,"user_ref_bal":user.ref_balance })
            except Account.DoesNotExist:
                user = None
                return JsonResponse({'msg':"No Account Matching Query"})
    return render(request,'superadmin/users.html',{'users':users})




#@manager_required
def login_user_account(request,user_pk):
    logout(request)
    user = Account.objects.get(pk=user_pk)
    login(request,user)
    messages.info(request,f"Log In As {user.username}")
    return redirect('dashboard')




@manager_required
def _withdraws_(request):
    withdrawals = Transactions.objects.filter(trans_type=utils.W).order_by('-date')
    if request.POST:
        print(request.POST.get('pk'))
        pk = int(request.POST.get('pk'))
        try:
            withdrawal = Transactions.objects.get(pk=pk)
            method = ''
            if withdrawal.card_detail:
                method = 'Card'
            elif withdrawal.bank_details:
                method = withdrawal.bank_details.ty_pe
            else:
                method = withdrawal.wallet_detail.coin_tpye
            with_date = withdrawal.date.date().isoformat()
            return JsonResponse({"msg":"success","with_user":withdrawal.user.username,
              "with_amount":withdrawal.amount,"with_method":method,
               "with_date":with_date,"with_status":withdrawal.status })
        except Transactions.DoesNotExist:
            return JsonResponse({"msg":"Error"})
    return render(request,'superadmin/withdraws.html',{"withdrawals":withdrawals})


@manager_required
def process_withdrawal(request,with_pk):
    if request.POST:
        submit = request.POST.get('ty_pe')
        try:
            withdrawal = Transactions.objects.get(pk=with_pk)
        except Transaction.DoesNotExist:
            withdrawal = None
        if withdrawal is not None:
            if submit == "approved":
                withdrawal.status = "approved"
                print(withdrawal.user.amount_withdraw)
                withdrawal.user.amount_withdraw += withdrawal.amount
                withdrawal.user.save()
                withdrawal.save()
                subject = "Transaction Approved"
                message = render_to_string('superadmin/with-email.html', {
                    'user': withdrawal.user,
                    'date': timezone.now(),
                    'amount': withdrawal.amount,
                    'status': "Approved",
                })
                withdrawal.user.save()
                withdrawal.save()
                Notification.objects.create(user=withdrawal.user,title="Transaction Approved", body=f" YOUR WITHDRAWAL OF ${withdrawal.amount} HAS BEEN APPROVED ")
                withdrawal.user.email_user(subject, message)
                return JsonResponse({"msg":"Withdrawal Approved"})
            elif submit == 'declined':
                withdrawal.status = "declined"
                subject = "Transaction Declined"
                message = render_to_string('superadmin/with-email.html', {
                    'user': withdrawal.user,
                    'date': timezone.now(),
                    'amount': withdrawal.amount,
                    'status': "Declined",
                })
                Notification.objects.create(user=withdrawal.user,title="Transaction Declined", body=f" YOUR WITHDRAWAL OF ${withdrawal.amount} HAS   FAILED YOU CAN CONTACT ADMIN FOR FURTHER INSTRUCTIONS")
                withdrawal.save()
                withdrawal.user.email_user(subject, message)
                withdrawal.save()
                return JsonResponse({"msg":"Withdrawal Declined"})
            else:
                return JsonResponse({"msg":"Unknow Error Occured"})           
        else:
            return JsonResponse({"msg":"No Withdrawal Matching Query"})
    else:
        return JsonResponse({'msg':"Get Request Not Accepted"})
        



@manager_required
def _deposit_(request):
    deposits = Transactions.objects.filter(trans_type=utils.D).order_by('-date')
    if request.POST:
        pk = int(request.POST.get('pk'))
        try:
            deposit = Transactions.objects.get(pk=pk)
            method = ''
            if deposit.card_detail:
                method = 'Card'
            elif deposit.bank_details:
                method = deposit.bank_details.ty_pe
            else:
                method = deposit.wallet_detail.coin_tpye
            deposit_date = deposit.date.date().isoformat()
            return JsonResponse({"msg":"success","depo_user":deposit.user.username,
              "depo_amount":deposit.amount,"depo_method":method,
               "depo_date":deposit_date,"depo_status":deposit.status })
        except Transactions.DoesNotExist:
            return JsonResponse({"msg":"Error"})
    return render(request,'superadmin/deposit.html',{"deposits":deposits})












@manager_required
def process_deposit(request,depo_pk):
    if request.POST:
        submit = request.POST.get('ty_pe')
        try:
            deposit = Transactions.objects.get(pk=depo_pk)
        except Transaction.DoesNotExist:
            deposit = None
        if deposit is not None:
            if submit == "approved":
                deposit.status = "approved"
                #print(deposit.user.amount_withdraw)
                deposit.user.deposit_balance += deposit.amount
                subject = "Transaction Approved"
                message = render_to_string('superadmin/deposite-email.html', {
                    'user': deposit.user,
                    'date': timezone.now(),
                    'amount': deposit.amount,
                    'status': "Approved",
                })
                deposit.user.save()
                deposit.save()
                Notification.objects.create(user=deposit.user,title="Transaction Approved", body=f" YOUR WITHDRAWAL OF ${deposit.amount} HAS BEEN APPROVED ")
                deposit.user.email_user(subject, message)
                return JsonResponse({"msg":"Deposit Approved"})
            elif submit == 'declined':
                deposit.status = "declined"
                subject = "Transaction Declined"
                message = render_to_string('superadmin/deposite-email.html', {
                    'user': deposit.user,
                    'date': timezone.now(),
                    'amount': deposit.amount,
                    'status': "Declined",
                })
                Notification.objects.create(user=deposit.user,title="Transaction Declined", body=f" YOUR WITHDRAWAL OF ${deposit.amount} HAS   FAILED YOU CAN CONTACT ADMIN FOR FURTHER INSTRUCTIONS")
                deposit.save()
                deposit.user.email_user(subject, message)
                deposit.save()
                return JsonResponse({"msg":"Deposit Declined"})
            else:
                return JsonResponse({"msg":"Unknow Error Occured"})           
        else:
            return JsonResponse({"msg":"No Deposit Matching Query"})
    else:
        return JsonResponse({'msg':"Get Request Not Accepted"})






@manager_required
def _trades_(request):
    trades = Trade.objects.all().order_by('-date')
    if request.POST:
        trade_pk = request.POST.get('trade_id')
        trade = Trade.objects.get(pk=trade_pk)
        date =  trade.date.date().isoformat()
        end_time = trade.end_date.time()
        return JsonResponse({"amount":trade.amount,"status":trade.status,"time":date,
            "type":trade.ty_pe,"symbol":trade.sysmbol,"exp_pay":trade.payout,"leverage":trade.leverage,
            "end_price":trade.end_amount(),"interval":trade.interval,"end_time":end_time})
    return render(request,'superadmin/trades.html',{"trades":trades})




@manager_required
def ongoin_trades(request):
    ongoin_trades_ = OngoingTrade.objects.all()
    if request.POST:
        trade_id = request.POST.get('trade_id')
        trade = OngoingTrade.objects.get(pk=trade_id)
        return JsonResponse({"amount":trade.amount,
            "symbol":trade.sysmbol,"leverage":trade.leverage,
            "interval":trade.interval,"pay":trade.pay,"trade_id":trade.id})
    return render(request,'superadmin/ongointrade.html',{'ongoin_trades_':ongoin_trades_})



@manager_required
def edit_ongoin_trade(request):
    if request.POST:
        submit = request.POST.get('ty_pe')
        amount = request.POST.get('amount')
        symbol = request.POST.get('symbol')
        interval = request.POST.get('interval')
        leverage = request.POST.get('leverage')
        pay = request.POST.get('pay')
        if submit == "old":
            trade_id = request.POST.get('trade_id')
            ongoin_trade = OngoingTrade.objects.get(pk=trade_id)
            ongoin_trade.amount = amount
            ongoin_trade.sysmbol = symbol
            ongoin_trade.interval = interval
            ongoin_trade.leverage = leverage
            ongoin_trade.pay = pay
            ongoin_trade.save()
            messages.info(request,"Updated")
            return redirect('super_ongoin_trades')
        elif submit == 'new':
            ongoin_trade , created = OngoingTrade.objects.get_or_create(amount=amount,sysmbol=symbol,interval=interval,
                leverage=leverage,pay=pay)
            ongoin_trade.save()
            messages.info(request,"Created Successful")
            return redirect('super_ongoin_trades')
        else:
            messages.info(request,"Error")
            return redirect('super_ongoin_trades')
    else:
        messages.info(request,"GET REQUEST NOT ACCEPTED")
        return redirect('super_ongoin_trades')





@manager_required
def documents_(request):
    kyc  = Kyc.objects.all()
    if request.POST:
        doc_id = request.POST.get('doc_id')
        try:
            doc = Kyc.objects.get(pk=doc_id)
            return JsonResponse({'msg':"done","doc_front":doc.document_front.url,'doc_back':doc.document_back.url,'username':doc.user.username,'doc_name':doc.name,'doc_number':doc.number,'country_issued':doc.country_issued,'ssn':doc.ssn,'status':doc.status})
        except Kyc.DoesNotExist:
            return JsonResponse({'msg':'error'})
    return render(request,'superadmin/doc.html',{'kyc':kyc})




@manager_required
def process_documents_(request):
    if request.POST:
        doc_id = request.POST.get('doc_id')
        status = request.POST.get('status')
        try:
            doc = Kyc.objects.get(pk=doc_id)
            doc.status = status
            if status == 'approved':
                doc.user.is_verified = True
                doc.user.save()
            doc.save()
            Notification.objects.create(user=request.user,title=f"Documents {status.capitalize()}", body=f" YOUR Document   HAS  BEEN {status.capitalize()} ")
            return JsonResponse({'msg':status})
        except Kyc.DoesNotExist:
            return JsonResponse({'msg':'ERROR'})
    return JsonResponse({'msg':'GET REQUST NOT ACCEPTED'})
