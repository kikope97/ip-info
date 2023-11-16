from flask import Flask, render_template, request
import requests
import ipinfo

app = Flask(__name__)
ipinfo_token = '5f895d9f632bbc'
handler = ipinfo.getHandler(ipinfo_token)

def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except Exception as e:
        return str(e)

def get_ip_info(ip):
    try:
        details = handler.getDetails(ip)
        return details.all
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    public_ip = get_public_ip()
    if request.method == 'POST':
        user_ip = request.form.get('ip_address')
        ip_info = get_ip_info(user_ip)
        if isinstance(ip_info, dict):
            ip_info_list = [(key, value) for key, value in ip_info.items()]
        else:
            ip_info_list = [(user_ip, ip_info)]
        return render_template('index.html', ip=public_ip, user_ip=user_ip, ip_info=ip_info_list)
    return render_template('index.html', ip=public_ip)

if __name__ == '__main__':
    app.run(debug=True)