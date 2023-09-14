from flask import Flask, render_template, url_for, redirect, request
import requests
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier

rs = requests.session()
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return render_template('numberbook.html')


@app.route('/error')
def err():
    return render_template('error.html')

@app.route('/search',methods=['POST', 'GET'])
def search():
    data = request.form.to_dict()
    number_value = data['num']
    derctry = 0
    first_op = number_value[0]
    if first_op == '0':
        print('without 0')
        return redirect(url_for('err'))
    for _ in number_value:
        derctry += 1
    if derctry == 9:
        split_number = f'+966{number_value}'
        parse_number = phonenumbers.parse(split_number)
        loc = geocoder.description_for_number(parse_number, "en")
        company = carrier.name_for_number(parse_number, 'en')
        send = rs.get(f"http://caller-id.saedhamdan.com/index.php/UserManagement/search_number?number={number_value}&country_code=SA", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})
        try:
            numname = send.json()['result'][0]['name']
            if numname == '':
                print('err1')
                return redirect(url_for(err))
        except Exception as bug:
            print(f'err2( {bug} )')
            return redirect(url_for('err'))
        return render_template('datanum.html', number=number_value, loc=loc ,username=numname, company=company)
    else:
        print(f'Wrong {derctry} have to be 9')
        return redirect(url_for('err'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0' port='5000')