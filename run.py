from yvih import app

app.config['DEBUG'] = True
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

if __name__ == '__main__':
    app.run()
