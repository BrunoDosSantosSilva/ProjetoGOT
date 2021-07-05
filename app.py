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

class got_personagens(got.Model):
    id = got.Column(got.Integer,primary_key=True)
    nome = got.Column(got.String(30),nullable=False)
    imagem_url = got.Column(got.String(2000),nullable=False)
    descricao = got.Column(got.String(2000),nullable=False)

    def __init__(self, nome,descricao,imagem_url):
        self.nome = nome
        self.descricao = descricao
        self.imagem_url = imagem_url
        

    @staticmethod
    def read_all():
        return got_personagens.query.order_by(got_personagens.id.asc()).all()

    @staticmethod
    def read_single(registro_id):
        return got_personagens.query.get(registro_id)

    def save(self):
        got.session.add(self)
        got.session.commit()

    def update(self, new_data):
        self.nome = new_data.nome  
        self.imagem_url = new_data.imagem_url
        
        self.save()

    def delete(self):
        got.session.delete(self)
        got.session.commit()


@app.route('/')

def index ():
    return render_template('index.html')

#Read

@app.route('/read')

def read_all():
    registros = got_personagens.read_all()

    return render_template('read_all.html',registros=registros)

@app.route ('/read/<registro_id>')
def read_single(registro_id):
    registro = got_personagens.read_single(registro_id)
    print (registro)
    return render_template('read_single.html', registro = registro)

#Create
@app.route('/create', methods=('GET', 'POST'))
def create():
    id_atribuido = None

    if request.method =='POST':
        form = request.form

        registro = got_personagens(form['nome'],form['imagem_url'],form['descricao'])
        registro.save()

        id_atribuido = registro.id

    return render_template('create.html',id_atribuido=id_atribuido)





@app.route('/update/<registro_id>', methods=('GET', 'POST'))
def update(registro_id):
    sucesso = None
    registro = got_personagens.read_single(registro_id)
    if request.method == 'POST':
        form = request.form
        new_data = got_personagens(form['nome'],form['descricao'], form['imagem_url'])
        registro.update(new_data)
        sucesso = True
    return render_template('update.html', registro=registro, sucesso=sucesso)




@app.route('/delete/<registro_id>')

def delete(registro_id):

    registro = got_personagens.read_single(registro_id)

    return render_template('delete.html', registro=registro)

@app.route('/delete/<registro_id>/confirmed')
def delete_confirmed(registro_id):
    sucesso = None

    registro = got_personagens.read_single(registro_id)

    if registro:
        registro.delete()
        sucesso = True
    return render_template('delete.html',registro=registro, registro_id=registro_id, sucesso=sucesso)


if __name__ =="__main__":
    app.run(debug=True)
