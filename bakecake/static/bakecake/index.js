Vue.createApp({
    name: "App",
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            schema1: {
                lvls: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' количество уровней';
                },
                form: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' форму торта';
                },
                topping: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' топпинг';
                }
            },
            schema2: {
                name: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' имя';
                },
                phone: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' телефон';
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат почты нарушен';
                    }
                    return true;
                },
                phone_format:(value) => {
                    const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат телефона нарушен';
                    }
                    return true;
                },
                email: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' почту';
                },
                address: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' адрес';
                },
                date: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' дату доставки';
                },
                time: (value) => {
                    if (value) {
                        return true;
                    }
                    return ' время доставки';
                }
            },
            DATA: {
                Levels: ['не выбрано'],
                Forms: ['не выбрано'],
                Toppings: ['не выбрано'],
                Berries: ['нет'],
                Decors: [ 'нет']
            },
            Costs: {
                Levels: [0],
                Forms: [0],
                Toppings: [0],
                Berries: [0],
                Decors: [0],
                Words: 0
            },
            Levels: 0,
            Form: 0,
            Topping: 0,
            Berries: 0,
            Decor: 0,
            Words: '',
            Comments: '',
            Designed: false,

            Name: '',
            Phone: null,
            Email: null,
            Address: null,
            Dates: null,
            Time: null,
            DelivComments: '',
        }
    },
    methods: {
        ToStep4() {
            this.Designed = true
            setTimeout(() => this.$refs.ToStep4.click(), 0);
        },
        SubmitOrder() {
            //Тут выведен в консоль объект, описывающий заказ полностью. Сработает только после прохождения валидации 2ой формы:
            console.log(JSON.stringify({
                Cost: this.Cost,
                Levels: this.DATA.Levels[this.Levels],
                Form: this.DATA.Forms[this.Form],
                Topping: this.DATA.Toppings[this.Topping],
                Berries: this.DATA.Berries[this.Berries],
                Decor: this.DATA.Decors[this.Decor],
                Words: this.Words,
                Comments: this.Comments,
                Name: this.Name,
                Phone: this.Phone,
                Email: this.Email,
                Address: this.Address,
                Dates: this.Dates,
                Time: this.Time,
                DelivComments: this.DelivComments,
            }, null ,2))
            
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

            function payCake(orderId, csrftoken) {
                var pay_sum = Number(document.getElementById('showSum').innerHTML)
                var widget = new cp.CloudPayments();

                widget.pay('auth',
                    {
                        publicId: 'test_api_00000000000000000000001', //id из личного кабинета
                        description: 'Оплата товаров в super-cake.herokuapp.com', //назначение
                        amount: pay_sum, //сумма
                        currency: 'RUB', //валюта
                        accountId: 'user@example.com', //идентификатор плательщика (необязательно)
                        invoiceId: '1234567', //номер заказа  (необязательно)
                        email: 'user@example.com', //email плательщика (необязательно)
                        skin: "mini",
                        data: {
                            myProp: 'myProp value'
                        }
                    },
                    {
                        onSuccess: function(options) {

                        },
                        onFail: function (reason, options) { // fail
                            //действие при неуспешной оплате
//                            window.location.replace("/fail");
                        },
                        onComplete: function (paymentResult, options) { //Вызывается как только виджет получает от api.cloudpayments ответ с результатом транзакции.
                            //например вызов вашей аналитики Facebook Pixel
                            axios
                                .put(
                                    '/api/cake',
                                    {orderId: orderId},
                                    {headers: {"X-CSRFToken": csrftoken}}
                                ).then(window.location.replace("/success"));
                        }
                    }

                )


            }

            const csrftoken = getCookie('csrftoken');

            axios
                .post('/api/cake', {
                    Cost: this.Cost,
                    Levels: this.DATA.Levels[this.Levels],
                    Form: this.DATA.Forms[this.Form],
                    Topping: this.DATA.Toppings[this.Topping],
                    Berries: this.DATA.Berries[this.Berries],
                    Decor: this.DATA.Decors[this.Decor],
                    Words: this.Words,
                    Comments: this.Comments,
                    Name: this.Name,
                    Phone: this.Phone,
                    Email: this.Email,
                    Address: this.Address,
                    Dates: this.Dates,
                    Time: this.Time,
                    DelivComments: this.DelivComments,
                },
                {headers: {"X-CSRFToken": csrftoken}})
                .then(response =>{
                    payCake(response.data, csrftoken)
                });

        }
    },
    computed: {
        Cost() {
            let W = this.Words ? this.Costs.Words : 0
            return this.Costs.Levels[this.Levels] + this.Costs.Forms[this.Form] +
                this.Costs.Toppings[this.Topping] + this.Costs.Berries[this.Berries] +
                this.Costs.Decors[this.Decor] + W
        }
    },
    mounted() {
        axios
            .get('/api/cake')
            .then(response => {
                this.DATA["Levels"] = this.DATA["Levels"].concat(response.data.levels_names)
                this.Costs["Levels"] = this.Costs["Levels"].concat(response.data.levels_prices)
                this.DATA["Forms"] = this.DATA["Forms"].concat(response.data.shapes_names)
                this.Costs["Forms"] = this.Costs["Forms"].concat(response.data.shapes_prices)
                this.DATA["Toppings"] = this.DATA["Toppings"].concat(response.data.toppings_names)
                this.Costs["Toppings"] = this.Costs["Toppings"].concat(response.data.toppings_prices)
                this.DATA["Berries"] = this.DATA["Berries"].concat(response.data.berries_names)
                this.Costs["Berries"] = this.Costs["Berries"].concat(response.data.berries_prices)
                this.DATA["Decors"] = this.DATA["Decors"].concat(response.data.decors_names)
                this.Costs["Decors"] = this.Costs["Decors"].concat(response.data.decors_prices)
            })
    }
}).mount('#VueApp')