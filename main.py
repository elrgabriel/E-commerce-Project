from flask import Flask, render_template, request, redirect, url_for, flash, jsonify  # type: ignore
from flask_cors import CORS
from model import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
CORS(app) #Permitir requisições de outros lugares
db.init_app(app)
with app.app_context():
        db.create_all()

#Tentativa API e Angular.

@app.route('/api/usuarios', methods=['POST'])
def api_register_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data received'}), 400  # Caso não receba dados no formato JSON
    print(data)
    email = data.get('email')
    password = data.get('password')
    nome = data.get('nome')
    apelido = data.get('apelido')
    morada = data.get('morada')
    distrito = data.get('distrito')

    # Verifique se os campos essenciais estão presentes
    if not email or not password or not nome or not apelido or not morada or not distrito:
        return jsonify({'error': 'Todos os campos são obrigatórios'}), 400

    # Verifica se o e-mail já está registrado
    existing_user = Users.query.filter_by(user_email=email).first()
    if existing_user:
        return jsonify({'error': 'Usuário já registrado'}), 400

    # Adiciona o novo usuário ao banco de dados
    new_user = Users(
        user_email=email,
        user_password=password,
        user_name=nome,
        user_last_name=apelido,
        user_address=morada,
        user_district=distrito
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário registrado com sucesso'}), 201



#Adicionando outro EndPoint para verificar se o usuário já existe.
@app.route('/api/usuarios/login', methods=['POST'])
def api_login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Procura o usuário pelo e-mail
    user = Users.query.filter_by(user_email=email).first()
    if not user or user.user_password != password:
        return jsonify({'error': 'E-mail ou senha inválidos'}), 401

    # Retorna uma mensagem de sucesso
    return jsonify({'message': 'Login realizado com sucesso', 'user_id': user.id}), 200


#Tentativa API e Angular.

# Retornar todos os produtos da base de dados
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    produtos = Products.query.all()
    produtos_json = [
        {
            'id': produto.id,
            'product_name': produto.product_name,
            'product_price': produto.product_price,
            'product_image': produto.product_image
        } for produto in produtos
    ]
    return jsonify(produtos_json)

# Retornar todos os usuários da base de dados
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Users.query.all()
    usuarios_json = [
        {
            'id': usuario.id,
            'user_email': usuario.user_email,
            'user_name': usuario.user_name,
            'user_last_name': usuario.user_last_name,
            'user_address': usuario.user_address,
            'user_district': usuario.user_district
        } for usuario in usuarios
    ]
    return jsonify(usuarios_json)


@app.route('/')
@app.route('/home')
def index():
    products = Products.query.all()
    return render_template('index.html', items = products)

@app.route('/404')
def error():
    return render_template('404.html')

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["login_email"]
        password = request.form["login_password"]

        search_user = Users.query.filter_by(user_email = email).first()
        
        print(search_user.user_email)
        print(search_user.user_password)
        print(email)
        print(password)
        if search_user.user_email == email and search_user.user_password == password:
            print("You're are logged in")
            return redirect(url_for("ProfilePage",user_id = search_user.id))
    return render_template('loginPage.html')

@app.route('/register', methods = ["GET", "POST"])
def register():

    if request.method == "POST":
        email = request.form["register_email"]
        user_re_email = request.form["register_re_email"]
        password = request.form["register_password"]
        user_re_password = request.form["register_re_password"]
        nome = request.form["register_nome"]
        apelido = request.form["register_apelido"]
        morada = request.form["register_morada"]
        distrito = request.form["register_distrito"]

        new_user = Users.query.filter_by(user_email = email).first()
        
        if new_user is None:

            check_email = email == user_re_email
            check_password = password == user_re_password

            print(f"Check email: {check_email}, Check password: {check_password}")

            if check_email and check_password:
                add_user = Users(
                    user_email = email,
                    user_password = password,
                    user_name = nome,
                    user_last_name = apelido,
                    user_address = morada,
                    user_district = distrito
                    )
                db.session.add(add_user)
                db.session.commit()
                print("Registo Bem Sucedido!")
                registered_user = Users.query.filter_by(user_email = email).first()
                return redirect(url_for("ProfilePage",user_id = registered_user.id))
            else:
                print("Email ou password não correspondem.")
        else:
            print("Usuário já registado")
    return render_template('RegistryPage.html')

@app.route('/ProfilePage/<int:user_id>')
def ProfilePage(user_id):
    current_user = Users.query.get_or_404(user_id)
    return render_template('ProfilePage.html', user = current_user)

@app.route('/ProductSingle/<int:product_id>')
def product_single(product_id):
    product = Products.query.get_or_404(product_id) 
    return render_template('ProductSingle.html', item = product)

@app.route('/Cart')
def CartPage():
    return render_template('CartPage.html')

@app.route('/CompletePurchase')
def CompletePurchase():
    return render_template('CompletePurchase.html')



if __name__ == "__main__":
    app.run(debug=True)


