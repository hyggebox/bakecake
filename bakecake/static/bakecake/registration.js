Vue.createApp({
    components: {
        VForm: VeeValidate.Form,
        VField: VeeValidate.Field,
        ErrorMessage: VeeValidate.ErrorMessage,
    },
    data() {
        return {
            RegSchema: {
                reg: (value) => {
                    if (value) {
                        return true;
                    }
                    return 'Поле не заполнено';
                },
                email_format: (value) => {
                    const regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат email нарушен';
                    }
                    return true;
                },
                password_format: (value) => {
                    const regex = /^[a-zA-Z0-9]+$/
                    if (!value) {
                        return true;
                    }
                    if ( !regex.test(value)) {

                        return '⚠ Формат пароля нарушен';
                    }
                    return true;
                }
            },
            Step: 'Email',
            RegInput: '',
            EnteredNumber: ''
        }
    },
    methods: {
        RegSubmit() {
            if (this.Step === 'Email') {
                this.Step = 'Password'

                console.log('Введённый email:', this.RegInput)
                this.EnteredNumber = this.RegInput
                this.RegInput = ''
            }
            else {
                this.Step = 'Finish'
                console.log('Введённый пароль:', this.RegInput, 'Регистрация успешна')
                this.RegInput = 'Регистрация успешна'
            }
        },
        ToRegStep1() {
            this.Step = 'Email'
            this.RegInput = this.EnteredNumber
        },
        Reset() {
            this.Step = 'Email'
            this.RegInput = ''
            EnteredNumber = ''
        }
    }
}).mount('#RegModal')