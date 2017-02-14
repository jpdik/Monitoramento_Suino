# coding: utf-8
import json
import os
import requests
import dropbox

from flask import Flask, Response
from flask import request

app = Flask(__name__)

TOKEN = 'clRIL4yey9UAAAAAAAAIU64daZXrSn5UG4ACrkNEaJP7v0gA5qtvdx47--9mVuYp'

#NOT_ALLOWED_EXTENSIONS = set(['mp3', 'wma', 'wav', 'm4a', 'mov', 'avi', 'mpg', 'mpeg', 'ogg'])

client = dropbox.client.DropboxClient(TOKEN) 

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader(__name__, 'templates'))

def get_size(fobj):
    if fobj.content_length:
        return fobj.content_length

    try:
        pos = fobj.tell()
        fobj.seek(0, 2)  #seek to end
        size = fobj.tell()
        fobj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass

    # in-memory file object that doesn't support seeking or tell
    return 0  #assume small enough

#def arquivo_negado(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1] in NOT_ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
  if request.method == 'GET':
    info = client.metadata('/')
    template = env.get_template('index.html')
    return template.render(arquivos=info['contents'])  
  else:
    return json.dumps({'erro': 'Método inválido'})


@app.route('/<nome>', methods=['GET'])
def exibirArquivo(nome):
  if request.method == 'GET':
    try:
      f, metadata = client.get_file_and_metadata(nome)
      csv = f.read()
      return csv
    except dropbox.rest.ErrorResponse as err:
      template = env.get_template('erro.html')
      return template.render(erro='O arquivo foi movido ou removido.',nome=nome)

if __name__ == "__main__":
  app.run(debug=True)
