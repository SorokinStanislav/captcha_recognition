from main.extract_symbols import recognize_captcha


def run_extra():
    image = 'extraset/color.png'
    recognize_captcha(image, 'usual')

    image = 'extraset/aerograph.png'
    recognize_captcha(image, 'corn')

    image = 'extraset/corn.png'
    recognize_captcha(image, 'corn')

    image = 'extraset/mail.png'
    recognize_captcha(image, 'mail')

    image = 'extraset/splash.png'
    recognize_captcha(image, 'splashing')

    image = 'extraset/sponge.png'
    recognize_captcha(image, 'mail')

    image = 'extraset/stones.png'
    recognize_captcha(image, 'stones')
