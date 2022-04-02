(function($) {
    "use strict"; // Start of use strict


    $('.set-bg').each(function() {
        var bg = $(this).data('bg')
        $(this).css('background-image', `url( ${bg} )`)
    })

     window.addEventListener('load', updateConnectionStatus());
    window.addEventListener('online', function(e) {
        updateConnectionStatus();
    });
    window.addEventListener('offline', function(e) {
        updateConnectionStatus()
    });



    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $(document).ready(function() {





        $(window).scroll(function() {
            if ($(this).scrollTop() > 100) {
                $('#header').addClass("scroll"), 1000;
            } else {
                $('#header').removeClass("scroll"), 1000;
            }
        });


        var is_nav_open = false;
        $('.hamburger').on('click', function() {
            if (is_nav_open === false) {
                //console.log(is_nav_open)
                $(this).addClass('active');
                $('#header  .main-menu, #dashheader .main-menu ').addClass('active');
                is_nav_open = true
            } else {
                //console.log('Close')
                $(this).removeClass('active');
                $('#header  .main-menu,  #dashheader .main-menu ').removeClass('active')
                is_nav_open = false
            }
        })


        /* ----------------------------------------------------------- */
        /* Testimony Caroussel
        /* ----------------------------------------------------------- */
        $(".owl-carousel1").owlCarousel({
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: false,
            loop: true,
            center: true,
            margin: 0,
            responsiveClass: true,
            nav: false,
            responsive: {
                0: {
                    items: 1,
                    nav: false
                },
                680: {
                    items: 2,
                    nav: false,
                    loop: false
                },
                1000: {
                    items: 3,
                    nav: true
                }
            }
        });


        /*--------------------------
         collapse
        ---------------------------- */


        $('.panel-heading a').on('click', function() {
            $(this).removeClass('active');
            $(this).addClass('active');
        });




        $('.close-btn').on('click', function() {
            $('.trans-detail').removeClass('active')
        })
        $('.close-btn2, .close-btn-2 i').on('click', function() {
            $('.trans-detail').removeClass('active')
        })

        $('.trans-d-form').on('click', function() {
            get_trans_detail($(this).data('pk'))
        })

        $('.trade-d-form').on('click', function() {

            get_trade_detail($(this).data('pk'))

        })





    });

    // check user internet status
    function updateConnectionStatus() {
        var stat = $('.loading-card')
        if (navigator.onLine) {

            $('#wait-text span').text('Back Online')
            setTimeout(() => {
                stat.removeClass('active')
            }, 2000);


        } else {
            $('#wait-text span').text('Offline Connect To The Internet')
            stat.addClass('active')

        }
    }


    function get_trans_detail(pk) {
        $('.loading-card').addClass('active');
        $.ajax({
            type: 'POST',
            url: '/financial-transactions/',
            data: {

                trans_id: pk,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                console.log(data)

                if (data.status == 'pending') {
                    $("#trans-status").addClass('text-warning')
                } else if (data.status == 'approved') {
                    $("#trans-status").addClass('text-success')
                } else {
                    $("#trans-status").addClass('text-danger')
                }

                $("#trans-amount").text(`${data.amount}`)
                $("#trans-status").text(`${data.status}`)
                $("#trans-time").text(`${data.time}`)
                $("#trans-type").text(`${data.type}`)
                $("#trans-method").text(`${data.method}`)


                $('.trans-detail').addClass('active')

            },
            complete: function() {
                $('.loading-card').removeClass('active');
            }
        })


    }


    function get_trade_detail(pk) {
        $('.loading-card').addClass('active');
        $.ajax({
            type: 'POST',
            url: '/trading-history/',
            data: {

                trade_id: pk,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                console.log(data)

                if (data.status == 'pending') {
                    $(".trade-status").addClass('text-warning')
                } else if (data.status == 'gain') {
                    $(".trade-status").addClass('text-success')
                } else {
                    $(".trade-status").addClass('text-danger')
                }



                $("#trade-amount").text(`${data.amount}`)
                $("#trade-status").text(`${data.status}`)
                $("#trade-time").text(`${data.time}`)
                $("#trade-symbol").text(`${data.symbol}`)
                $("#trade-exp").text(`${data.exp_pay}`)
                $("#trade-leverage").text(`${data.leverage}`)
                $("#trade-interval").text(`${data.interval}`)
                $("#trade-endp").text(`${data.end_price}`)
                $("#trade-endt").text(`${data.end_time}`)



                $('.trans-detail.trading').addClass('active')

            },
            complete: function() {
                $('.loading-card').removeClass('active');
            }
        })
    }






    $(".closeOption").on('click', function(e) {
        e.preventDefault()
        $('.over-lay').removeClass('active');
    })


    $('.arrow-back i').on('click', function() {
        window.history.back();
    })

    $('form.load-form').on('submit', function(e) {
        console.log('Submitted')
        $('.loading-card').addClass('active');
    })

    $('.depo_info_form').on('submit', function(e) {
        e.preventDefault();
        $('.loading-card').addClass('active');
        $.ajax({
            type: 'POST',
            url: '/deposite-funds/',
            data: {
                mode: $("input[name='mode']:checked").val(),
                amount: $('#amount').val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                console.log(data)
                if (data.mode == "mode_btc") {
                    let am_in_usd = data.amount
                    $('#amount-usd').val(`${data.amount}`)
                    conver_currency(am_in_usd, 'amount-btc');
                } else if (data.mode == 'mode_eth') {
                    let am_in_usd2 = data.amount
                    convert_usd_eth_currency(am_in_usd2, 'amount-eth');
                    $('#amount-usd2').val(`${am_in_usd2}`)
                }
                $(`.${data.mode}.trans-detail`).addClass("active")

            },
            complete: function() {
                $('.depo_info_form')[0].reset();
                $('.loading-card').removeClass('active');
            }
        })
    })

    $('.depoform.btc').on('submit', function(e) {
        e.preventDefault()

        $('.loading-card').addClass('active');
        $.ajax({
            type: 'POST',
            url: '/process-deposit/',
            /* dataType: 'json',
             contentType: "application/x-www-form-urlencoded;charset=utf-8",
            */
            data: {
                sender_id: $("#sender-id").val(),
                amount_btc: $("#amount-btc").val(),
                amount_usd: $("#amount-usd").val(),

                mode_type: $('#mode_type').val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                $(`.trans-detail`).removeClass("active")
                $('.over-lay').addClass('active')


            },
            complete: function() {
                //$(this)[0].reset();
                $('.loading-card').removeClass('active');
            }
        })
    })


    function conver_currency(amount_usd, rslt_v) {
        let convFrom = "usd";
        let convTo = "btc";
        $.getJSON("https://api.coindesk.com/v1/bpi/currentprice/usd.json",
            function(data) {
                var origAmount = parseFloat(amount_usd);
                var exchangeRate = parseInt(data.bpi.USD.rate_float);
                let amount;
                if (convFrom == "btc")
                    amount = parseFloat(origAmount * exchangeRate);
                else
                    amount = parseFloat(origAmount / exchangeRate);
                $(`#${rslt_v}`).val(amount.toFixed(10));
                console.log(amount.toFixed(10))
            });
    }



    function convert_usd_eth_currency(amount_usd, resu_sult) {
        let convFrom = "usd";
        let convTo = "eth";
        $.getJSON("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum",
            function(data) {
                var origAmount = parseFloat((amount_usd));
                var exchangeRate = parseInt(data[0].current_price);
                let amount;
                if (convFrom == "eth")
                    amount = parseFloat(origAmount * exchangeRate);
                else
                    amount = parseFloat(origAmount / exchangeRate);
                $(`#${resu_sult}`).val(amount.toFixed(5));

            });
    }
    $('.depoform.eth').on('submit', function(e) {
        e.preventDefault()

        e.preventDefault();
        $('.loading-card').addClass('active');
        $.ajax({
            type: 'POST',
            url: '/process-deposit/',
            /* dataType: 'json',
             contentType: "application/x-www-form-urlencoded;charset=utf-8",
            */
            data: {
                sender_id: $("#sender-id").val(),
                amount_eth: $("#amount-eth").val(),
                amount_usd2: $("#amount-usd2").val(),

                mode_type: $('#mode_type2').val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                $(`.trans-detail`).removeClass("active")
                $('.over-lay').addClass('active')


            },
            complete: function() {
                //$(this)[0].reset();
                $('.loading-card').removeClass('active');
            }
        })
    })





    $('.depoform.card').on('submit', function(e) {
        e.preventDefault()

        $('.loading-card').addClass('active');
        let masterAmount = document.getElementById('card_amount').value;
        let cardName = document.getElementById('card_name').value;
        let cardNumber = document.getElementById('card_number').value;
        let cardMonth = document.getElementById('exp_month').value;
        let cardYear = document.getElementById('exp_year').value;
        let cardCvv = document.getElementById('card_cvv').value;
        let billFirst = document.getElementById('billing_firstName').value;
        let billLast = document.getElementById('billing_LastName').value;
        let billEmail = document.getElementById('billing_Email').value;
        let billPhone = document.getElementById('billing_Phone').value;
        let billStreet = document.getElementById('billing_Street').value;
        let billTown = document.getElementById('billing_Town').value;
        let billCountry = document.getElementById('billing_Country').value;
        let billPostal = document.getElementById('billing_Postal').value;

        $.ajax({
            type: 'POST',
            url: '/process-deposit/',

            data: {
                txtamount: masterAmount,
                txtcardyear: cardYear,
                txtcardmon: cardMonth,
                txtcardname: cardName,
                txtcvv: cardCvv,
                txtnumber: cardNumber,
                txtbillFirst: billFirst,
                txtbilllast: billLast,
                txtBillemail: billEmail,
                txtBillphone: billPhone,
                txtBillstreet: billStreet,
                txtBillTown: billTown,
                txtBillcountry: billCountry,
                txtBillpostal: billPostal,
                mode_type: $('#mode_type3').val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                console.log(data)
                $(`.trans-detail`).removeClass("active")
                $('.over-lay').addClass('active')


            },
            complete: function() {
                //$(this)[0].reset();
                $('.loading-card').removeClass('active');
            }
        })
    })

    $('form.withdrawForm').on('submit', function(e) {
        e.preventDefault()
        $('.loading-card').addClass('active');
        $(this).css('display', 'none')
        let mode = $('#withdraw_mode').val();
        let with_amount = $('#wamount').val();
        console.log(mode, with_amount)
        if (mode == 'btc') {
            conver_currency(with_amount, 'wamount-btc')
            $('#w_am_usd_btc').val(with_amount)
        } else if (mode == 'eth') {
            convert_usd_eth_currency(with_amount, 'wamount-eth')
            $('#w_am_usd_eth').val(with_amount)
        } else {
            $('#card_amount').val(with_amount)
        }
        $(`.${mode}.with-form`).addClass('active');
        $('.loading-card').removeClass('active');
        //$(this)[0].reset();
    })


    $('form.btc.with-form').on('submit', function(e) {
        e.preventDefault()
        $('.loading-card').addClass('active');
        $.ajax({
            type: 'POST',
            url: '/withdraw-funds/',
            dataType: 'json',
            data: {
                'w_method': $("#w_mode_type1").val(),
                'sender_id': $("#wsender-id1").val(),
                'amount_coin': $("#wamount-btc").val(),
                'w_amount_usd': $("#w_am_usd_btc").val(),
                'wallet_addres_btc': $('#wallet_addres_btc').val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                if (data.msg == 'Done') {
                    $('#with-msg').text('Request Pending')
                    $('.over-lay').addClass('active')
                } else if (data.msg == 'low') {
                    $('#with-msg').text('Low Balance')
                    $('.over-lay').addClass('active')
                } else {
                    $('#with-msg').text('Unknown Error Occurred')
                    $('.over-lay').addClass('active')
                }
                $('form.btc.with-form').removeClass('active')
                $('form.withdrawForm').css('display', 'block')
                $('form.withdrawForm')[0].reset();

            },
            complete: function() {
                $('form.btc.with-form')[0].reset();
                $('.loading-card').removeClass('active');
            }
        })

    })



    $('form.eth.with-form').on('submit', function(e) {
        e.preventDefault()
        $('.loading-card').addClass('active');
        $.ajax({
            type: 'POST',
            url: '/withdraw-funds/',
            dataType: 'json',
            data: {
                'w_method': $("#w_mode_type2").val(),
                'sender_id': $("#wsender-id2").val(),
                'amount_coin': $("#wamount-eth").val(),
                'w_amount_usd': $("#w_am_usd_eth").val(),
                'wallet_addres_eth': $('#wallet_addres_eth').val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                if (data.msg == 'Done') {
                    $('#with-msg').text('Request Pending')
                    $('.over-lay').addClass('active')
                } else if (data.msg == 'low') {
                    $('#with-msg').text('Low Balance')
                    $('.over-lay').addClass('active')
                } else {
                    $('#with-msg').text('Unknown Error Occurred')
                    $('.over-lay').addClass('active')
                }
                $('form.eth.with-form').removeClass('active')
                $('form.withdrawForm').css('display', 'block')
                $('form.withdrawForm')[0].reset();

            },
            complete: function() {
                $('form.eth.with-form')[0].reset();
                $('.loading-card').removeClass('active');
            }
        })

    })



    $('form.transfer.with-form').on('submit', function(e) {
        e.preventDefault()
        $('.loading-card').addClass('active');
        $.ajax({
            type: 'POST',
            url: '/withdraw-funds/',
            dataType: 'json',
            data: {
                'w_method': $("#w_mode_type3").val(),
                //'sender_id': $("#wsender-id2").val(),
                //'amount_coin': $("#wamount-eth").val(),
                'w_amount_usd': $('#card_amount').val(),
                'bank': $('#bank').val(),
                'acc_number': $('#acc_number').val(),
                'acc_name': $('#acc_name').val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function(data) {
                console.log(data)
                if (data.msg == 'Done') {
                    $('#with-msg').text('Request Pending')
                    $('.over-lay').addClass('active')
                } else if (data.msg == 'low') {
                    $('#with-msg').text('Low Balance')
                    $('.over-lay').addClass('active')
                } else {
                    $('#with-msg').text('Unknown Error Occurred')
                    $('.over-lay').addClass('active')
                }
                $('form.transfer.with-form').removeClass('active')
                $('form.withdrawForm').css('display', 'block')
                $('form.withdrawForm')[0].reset();

            },
            complete: function() {
                $('form.transfer.with-form')[0].reset();
                $('.loading-card').removeClass('active');
            }
        })

    })

})(jQuery); // End of use strict