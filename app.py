from flask import Flask, render_template, request

app = Flask(__name__)

def password_strength(user_input):
    has_upper = False
    has_lower = False
    has_digit = False
    has_symbols = False
    symbols = '!@#$%^&*"£'
    counter = 0

    # 1) checks length of password
    if len(user_input) < 8:
        return 'Password is too short! Must be at least 8 characters.'

    # 2) upper case check
    for i in user_input:
        if i.isupper():
            has_upper = True
            break
    if not has_upper:
        return 'Password must contain at least 1 uppercase letter'

    # 3) lower case check
    for i in user_input:
        if i.islower():
            has_lower = True
            break
    if not has_lower:
        return 'Password must contain at least 1 lower letter'

    # 4) digit check
    for i in user_input:
        if i.isdigit():
            has_digit = True
            break
    if not has_digit:
        return 'Password must contain digits'

    # 5) Symbols check
    for i in user_input:
        if i in symbols:
            has_symbols = True
            break
    if not has_symbols:
        return 'Password must contain at least 1 special character'

    # Check overall strength
    if has_upper and has_lower and has_digit and has_symbols:
        return 'Your password is strong!'
    elif has_upper and has_lower and has_digit:
        return 'Your password is medium'
    else:
        return 'Your password is weak!'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['password']
        result = password_strength(user_input)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)


if __name__ == '__main__':
    app.run(debug=True)


