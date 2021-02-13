from flask import Flask, Response, request
import requests
import urllib.parse
import redis
import html

app = Flask(__name__)
default_name = 'Dale Bewley'
cache = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route('/', methods=['GET', 'POST'])
def mainpage():
	name = default_name
	if request.method == 'POST':
		name = html.escape( request.form['name'], quote=True )

	header = '<html><head><title>Identidock</title></head><body>'
	body = '''<form method="POST">
				Hello <input type="text" name="name" value="{0}">
				<input type="submit" value="submit">
				</form>
				<p>You look like a:
				<img src="/monster/{1}"/>
				'''.format(name, urllib.parse.quote(name))
	footer = '</body></html>'

	return header + body + footer

@app.route('/monster/<name>')
def get_identicon(name):
	r = requests.get('http://dnmonster:8080/monster/' + html.escape( name, quote=True ) + '?size=80')
	image = r.content

	return Response(image, mimetype='image/png')

#@app.route('/monster/<name>')
#def get_identicon(name):
#    name = html.escape(name, quote=True)
    # Проверка наличия текущего значения переменной в кеше
#    image = cache.get(name)
    # При промахе кеша возвращает None. В этом случае изображение
    ## генерируется как обычно, а кроме того выводится некоторая отл-
    ### адочная информация
#    if image is None:
#        print("Cache miss", flush=True)
#        r = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
        #image = r.content
        # пиктограмма добавляется в кеш и связывается с именем
        #cache.set(name, image)

    #return Response(image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
