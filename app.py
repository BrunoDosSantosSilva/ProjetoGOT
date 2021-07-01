from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

user='ojnjbeia'
password='h9tsZudNolQRRx8cNOSBoWpBY71wMxTb'
host='tuffi.db.elephantsql.com'
database='ojnjbeia'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

got = SQLAlchemy(app)

class GOT_Personagens(got.model):
    id= got.Column(got.Integer,primary_key=True)
    nome=got.Column(got.String(30),nullable=False)
    imagem_url= got.Column(got.String(2000),nullable=False)
    descricao=got.Column(got.String(2000),nullable=False)

    def __init__(self, nome,imagem_url,descricao):
        self.nome = nome
        self.imagem_url = imagem_url
        self.descricao = descricao

    @staticmethod
    def read_all():
        return GOT_Personagens.query.order_by(GOT_Personagens.id.asc()).all()

    @staticmethod
    def read_single(registro_id):
        return GOT_Personagens.query.get(registro_id)

@app.route('/')

def index ():
    return render_template('index.html')

#Read

@app.route('/read')

def read_all():
    registros = GOT_Personagens.read_all()

    return render_template('read_all.html',registros=registros)

@app.route ('/read/<registro_id>')
def read_single(registro_id):
    registro = GOT_Personagens.read_single(registro_id)
    print (registro)
    return render_template('read_single.html', registro = registro)

#Create
@app.route('/create', methods=('GET', 'POST'))
def create():
    id_atribuido = None

    if request.method =='POST':
        form = request.form

        registro = GOT_Personagens(form['nome'],form['imagem_url'])
        registro.save()

        id_atribuido = registro.id

    return render_template('create.html',id_atribuido=id_atribuido)

if __name__ =="__main__":
    app.run(debug=True)
