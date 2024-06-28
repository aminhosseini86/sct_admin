from flask import Flask, render_template, request, jsonify, redirect, url_for, g
from menu import Menu
import requests
import jdatetime

app = Flask(__name__)


def menu_search(name, menu):
    try:
        return int("".join(str(i + 1) for i in range(len(menu)) if menu[i]['link'] == name))
    except:
        return 1


@app.before_request
def before_request():
    menu = Menu()
    menu_list = menu.generate()

    g.active_menu = menu_search(request.path, menu_list)


@app.context_processor
def context_processor():
    menu = Menu()
    return dict(menu={'items': menu.generate(), 'active': g.active_menu})


@app.route('/')
def index():
    g.active_menu = 1
    return render_template('index.html')


@app.route('/device_action', methods=['POST'])
def device_action():
    post_data = request.get_json()
    if post_data['command'] == 'R0':
        res = requests.post(
            url='http://127.0.0.1:8091/api/v1/iot/devices/' + post_data['qr'] + '/' + (
                'lock' if post_data['data']['0'] == '1' else 'unlock'),
            headers={
                'Authorization': '$2y$12$XkZr2ko0b5wpPp5vLQQfAum8fcLjil0Pq/FjeZJb7gRh2d9mOfw0W'
            })
    elif post_data['command'] == 'S5' or post_data['command'] == 'S7' or \
            ['command'] == 'S4' or post_data['command'] == 'V0':
        print(post_data['data'])
        res = requests.post(
            url='http://127.0.0.1:8080/request-command',
            json={'imei': post_data['imei'], 'data': post_data['data'],
                  'command': post_data['command'], 'tracking_code': 'AdminPanel'}
        )
    return jsonify({'description': 'start'}), res.status_code


@app.route('/get-device-details/<qr>/<imei>/')
def get_device_details(qr, imei):
    device = requests.get(url='http://127.0.0.1:8080/last-data/' + imei)
    try:
        data = device.json()['devices'][imei]
        date, time = data['timestamp'].split(' ')
        date = date.split('-')
        data['timestamp'] = jdatetime.date.fromgregorian(
            day=int(date[2]), month=int(date[1]), year=int(date[0])).strftime("%Y-%m-%d") + " " + time
    except:
        data = None
    return render_template('device_details.html', device=data, imei=imei, qr=qr)


@app.route('/devices')
def devices():
    devices = requests.get(url='http://127.0.0.1:8091/api/v1/iot/devices/list', headers={
        'Authorization': '$2y$12$XkZr2ko0b5wpPp5vLQQfAum8fcLjil0Pq/FjeZJb7gRh2d9mOfw0W'
    })
    return render_template('devices.html', devices=devices.json()['data'])


if __name__ == '__main__':
    app.run()
