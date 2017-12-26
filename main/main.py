import csv
import datetime

from main.extract_symbols import recognize_captcha


def run_main():
    symbols = {}
    recognition_result = {'true': 0, 'total': 0}
    with open('dataset.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            image = row[0]
            true_captcha = row[1]
            true_captcha_symbols = list(true_captcha)

            print(datetime.datetime.now())
            predicted_captcha = recognize_captcha(image, 'noise')
            predicted_captcha_symbols = list(predicted_captcha)
            print(predicted_captcha)

            i = 0
            for symbol in true_captcha_symbols:
                if symbol not in symbols.keys():
                    symbols[symbol] = {'true': 0, 'total': 0, 'wrong': set()}
                if symbol == predicted_captcha_symbols[i]:
                    symbols[symbol]['true'] += 1
                else:
                    symbols[symbol]['wrong'].add(predicted_captcha_symbols[i])
                symbols[symbol]['total'] += 1
                i += 1
            if true_captcha == predicted_captcha:
                recognition_result['true'] += 1
            recognition_result['total'] += 1

    print('--------------------------------------------------')
    print(symbols)
    print(recognition_result)

