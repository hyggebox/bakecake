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
                Toppings: ['не выбрано', 'Без'],
                Berries: ['нет'],
                Decors: [ 'нет']
            },
            Costs: {
                Levels: [0],
                Forms: [0],
                Toppings: [0, 0],
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
            DelivComments: ''
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

            axios.post('http://127.0.0.1:8000/api/cake', {
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
            .get('http://127.0.0.1:8000/api/cake')
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