from flask import Flask,flash
from flask import render_template,url_for,redirect
from flask import request,session
import os
import json,datetime
import random
import pymysql.cursors

app = Flask(__name__)

app.secret_key = os.urandom(24)

db = pymysql.connect(
	host='localhost',
	user='root',
	password='MaurArmel17+',
	db='etudiants',
	charset='utf8mb4',
	cursorclass=pymysql.cursors.DictCursor
)


"""
	page d'accueil
	si auth reussie info stocké dans session
"""
@app.route("/",methods=['POST','GET'])
@app.route("/connexion",methods=['POST','GET'])
def connexion():

	if request.method == 'POST':
		u = request.form['username']
		p = request.form['password']
		
		auth = auth_user(u,p)
		if len(auth) == 1:
			if auth[0]['super'] == 1:
				session['id'] = auth[0]['id']
				session['uname'] = auth[0]['uname']
				return redirect('index')
			else:
				return redirect('connexion')
		else:
			return redirect('connexion')
	else:
		deconnexion()
	return render_template('pages/connexion.html')
	


"""
	info page index
"""
@app.route("/index")
@app.route("/index",methods=['POST','GET'])
def index():
	if len(session) == 0:
		return redirect('connexion')
	i_ref = recup_ref()
	i_promo = recup_promo()
	i_appr = recup_apprenants()

	return render_template('pages/index.html',info=session,i_ref=i_ref,i_promo=i_promo,i_appr=i_appr)



@app.route('/ajouter_apprenant',methods=['POST','GET'])
def ajouter_apprenant():
	annee_actuelle = datetime.datetime.now()
	annee_actuelle = annee_actuelle.strftime("%Y")

	matAppr = annee_actuelle + "-" + uid() + "-" + uid()
	
	i_promo_annee = recup_promo_annee()

	if request.method == 'POST':
		matAppr = matAppr
		prenomAppr = request.form['prenomAppr']
		nomAppr = request.form['nomAppr']
		dateNaissAppr = request.form['dateNaissAppr']
		idPromoAppr = request.form['idPromoAppr']
		
		if matAppr == '' and prenomAppr == '' and nomAppr == '' and dateNaissAppr == '' and idPromoAppr == '':
		 	return "tous les info d'ajout de promotion sont obligatoires"
		else:
		 	if dateNaissAppr >= annee_actuelle:
		 		return "date de nqissance doit etre inferieur a l'annee actuelle"
		 	else:
		 		insert_appr(matAppr,prenomAppr,nomAppr,dateNaissAppr,idPromoAppr)
		 	return redirect('index')
	return render_template('pages/ajouter_apprenant.html',info=session,i_promo=i_promo_annee,matricule=matAppr)



"""generation du matricule"""
def uid():
	chars = "abcdefghijklmnopqrstuvwxyziABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
	uid = ""
	length = 4
	while len(uid) != length:
	    uid = uid + random.choice(chars) 
	    if len(uid) == length:
	        return uid
	return "error"



@app.route('/ajouter_promotion',methods=['POST','GET'])
def ajouter_promotion():
	i_promo = recup_promo()
	i_ref = recup_ref()
	if request.method == 'POST':
		nomPromo = request.form['nomPromo']
		dateDebutPromo = request.form['dateDebutPromo']
		dateFinPromo = request.form['dateFinPromo']
		idRefPromo = request.form['idRefPromo']

		if nomPromo == '' and dateDebutPromo == '' and dateFinPromo == '' and idRefPromo == '':
			return "tous les info d'ajout de promotion sont obligatoires"
		else:
			if dateDebutPromo >= dateFinPromo:
				return "date de debut sup à date fin"

			insert_promo(nomPromo,dateDebutPromo,dateFinPromo,idRefPromo)
			return redirect('index')
	return render_template('pages/ajouter_promotion.html',info=session,i_ref=i_ref)



@app.route('/ajouter_referentiel',methods=['POST','GET'])
def ajouter_referentiel():

	if request.method == 'POST':
		ref_nom = request.form['nomRef']
		ref_desc = request.form['descRef']
		date_ = datetime.datetime.now()
		date_ = date_.strftime("%Y-%m-%d")
		if ref_nom == '' or ref_desc == '':
			return "saisir le nom et ou la desc"
		else:
			insert_referentiel(ref_nom,ref_desc,date_)
			return redirect('index')

	return render_template('pages/ajouter_referentiel.html',info=session)



"""
	recuperation des referentiels depuis la base de donnee
"""
def recup_ref():
	cursor = db.cursor()
	sql = "SELECT * FROM referentiels_"
	cursor.execute(sql)
	i_ref = cursor.fetchall()
	db.commit()
	return i_ref

"""
	recuperation des referentiels WHERE
"""

def recup_ref_where(id):
	cursor = db.cursor()
	sql = "SELECT * FROM referentiels_ WHERE id = {}".format(id)
	cursor.execute(sql)
	i_ref = cursor.fetchall()
	db.commit()
	return i_ref



"""
	recuperation des promotions depuis la base de donnee
"""
def recup_promo():
	cursor = db.cursor()
	sql = "SELECT * FROM promotions_"
	cursor.execute(sql)
	i_promo = cursor.fetchall()
	db.commit()
	return i_promo

"""
	recuperation des promotions WHERE id = X
"""
def recup_promo_where(id):
	cursor = db.cursor()
	sql = "SELECT * FROM promotions_ WHERE id = {}".format(id)
	cursor.execute(sql)
	i_promo = cursor.fetchall()
	db.commit()
	return i_promo



"""
	recuperation des promotions where annee date de fin superieur à la date actuelle
	on ne peut pas ajouter un apprenant dans une promotion passée 
"""
def recup_promo_annee():
	date_actuelle = datetime.datetime.now()
	date_actuelle = date_actuelle.strftime("%Y-%m-%d")
	cursor = db.cursor()
	sql = "SELECT * FROM promotions_ WHERE dateFin > '{}'".format(date_actuelle)
	cursor.execute(sql)
	i_promo_annee = cursor.fetchall()
	db.commit()
	return i_promo_annee



"""
	recuperation des apprenants depuis la base de donnee
"""
def recup_apprenants():
	cursor = db.cursor()
	sql = "SELECT apprenants_.id,apprenants_.matricule,apprenants_.prenom,apprenants_.nom,apprenants_.dateNaiss,apprenants_.status,promotions_.nom as promo,referentiels_.nom as ref FROM apprenants_,promotions_,referentiels_ WHERE apprenants_.id_promo=promotions_.id AND referentiels_.id = promotions_.id_ref"
	cursor.execute(sql)
	i_appr = cursor.fetchall()
	db.commit()
	return i_appr


"""
	recuperation des apprenants WHERE id = X
"""
def recup_apprenants_where(id):
	cursor = db.cursor()
	sql = "SELECT * FROM apprenants_ WHERE id = {}".format(id)
	cursor.execute(sql)
	i_appr = cursor.fetchall()
	db.commit()
	return i_appr



"""
	recuperation des apprenants depuis la base de donnee
"""
def recup_id_promo_apprenants(id_pro_appr):
	cursor = db.cursor()
	sql = "SELECT nom FROM promotions_ WHERE id={}".format(id_pro_appr)
	cursor.execute(sql)
	nom_promo_appr = cursor.fetchall()
	db.commit()
	return nom_promo_appr


"""
	recuperation du status apprenants
"""
def recup_status_apprenant(id):
	cursor = db.cursor()
	sql = "SELECT status FROM apprenants_ WHERE id={}".format(id)
	cursor.execute(sql)
	status = cursor.fetchall()
	db.commit()
	return status

"""
	recuperation du status promotion
"""
def recup_status_promotion(id):
	cursor = db.cursor()
	sql = "SELECT status FROM promotions_ WHERE id={}".format(id)
	cursor.execute(sql)
	status = cursor.fetchall()
	db.commit()
	return status



"""
	deconnexion
"""
@app.route("/deconnexion")
def deconnexion():
	session.clear()
	return redirect('connexion')



"""
	Authentification administrateur
"""
def auth_user(u,p):
	cursor = db.cursor()
	sql = "SELECT * FROM users_ WHERE uname='{}' AND pass='{}'".format(u,p)
	cursor.execute(sql)
	result = cursor.fetchall()
	db.commit()

	return result



"""
	email administrateur existe 
"""
def e_existe(e):
	cursor = db.cursor()
	sql = "SELECT email FROM users_ WHERE email='{}'".format(e)
	cursor.execute(sql)
	result = cursor.fetchall()
	db.commit()

	return result



"""
	Inscription administrateur
"""
@app.route("/inscription",methods=['POST','GET'])
def inscription(u=None,e=None,p=None):

	if request.method == 'POST':
		u = request.form['uname']
		e = request.form['email']
		p = request.form['pass']

		if u == '' or e == '' or p == '':
			return render_template("pages/inscription.html",msg="les champs sont obligatoires")

		e_exist = e_existe(e)
		if len(e_exist) != 0:
		 	return render_template("pages/inscription.html",msg="email existe")

		u_exist = auth_user(u,p)
		if len(u_exist) != 0:
			return render_template("pages/inscription.html",msg="ce username est deja utilié")
		else:
			cursor = db.cursor()
			sql = "INSERT INTO users_(uname,email,pass) VALUES('{}','{}','{}')".format(u,e,p)
			cursor.execute(sql)
			db.commit()
			return render_template("pages/inscription.html",msg="Inscription reussie")
	else:
		return render_template("pages/inscription.html",msg="erreur methode get")

	return render_template("pages/inscription.html")






#################################################

#				    INSERTIONS

#################################################

def insert_appr(mat,pr,nom,dn,ipr):
	cursor = db.cursor()
	sql = "INSERT INTO apprenants_(matricule,prenom,nom,dateNaiss,id_promo) VALUES('{}','{}','{}','{}','{}')".format(mat,pr,nom,dn,ipr)
	cursor.execute(sql)
	db.commit()


def insert_promo(nom,dateDebut,dateFin,id_ref):
	cursor = db.cursor()
	sql = "INSERT INTO promotions_(nom,dateDebut,dateFin,id_ref) VALUES('{}','{}','{}','{}')".format(nom,dateDebut,dateFin,id_ref)
	cursor.execute(sql)
	db.commit()


def insert_referentiel(n,d,date):
	cursor = db.cursor()
	sql = "INSERT INTO referentiels_(nom,descript,dateCreation) VALUES('{}','{}','{}')".format(n,d,date)
	cursor.execute(sql)
	db.commit()





#################################################

#					 LISTER

#################################################

@app.route("/lister_apprenant")
def lister_apprenant():
	return render_template("pages/lister_apprenant.html",info=session,i_appr=recup_apprenants())


@app.route("/lister_promotion")
def lister_promotion():
	return render_template("pages/lister_promotion.html",info=session,i_promo=recup_promo())


@app.route("/lister_referentiel")
def lister_referentiel():
	return render_template("pages/lister_referentiel.html",info=session,i_ref=recup_ref())



#################################################

#					SUPPRESSION

#################################################

@app.route("/supprimer_apprenant/<int:id>")
def supprimer_apprenant(id):
	cursor = db.cursor()
	sql = "DELETE FROM apprenants_ WHERE id ={}".format(id)
	cursor.execute(sql)
	db.commit()
	return redirect('index')


@app.route("/supprimer_promotion/<int:id>")
def supprimer_promotion(id):
	cursor = db.cursor()
	sql = "DELETE FROM promotions_ WHERE id ={}".format(id)
	cursor.execute(sql)
	db.commit()
	return redirect('index')


@app.route("/supprimer_referentiel/<int:id>")
def supprimer_referentiel(id):
	cursor = db.cursor()
	sql = "DELETE FROM referentiels_ WHERE id ={}".format(id)
	cursor.execute(sql)
	db.commit()
	return redirect('index')










#################################################

#			    CHANGEMENT STATUS

#################################################

@app.route("/desactiver_apprenant/<int:id>")
def desactiver_apprenant(id):
	cursor = db.cursor()
	status_actuel = recup_status_apprenant(id)
	status_actuel = status_actuel[0]['status']
	if status_actuel == 1:
		new_status = 0
	else:
		new_status = 1;

	sql = "UPDATE apprenants_ SET status = {} WHERE id = {}".format(new_status,id)
	cursor.execute(sql)
	db.commit()
	return redirect('index')

@app.route("/desactiver_promotion/<int:id>")
def desactiver_promotion(id):
	cursor = db.cursor()
	status_actuel = recup_status_promotion(id)
	status_actuel = status_actuel[0]['status']
	if status_actuel == 1:
		new_status = 0
	else:
		new_status = 1;

	sql = "UPDATE promotions_ SET status = {} WHERE id = {}".format(new_status,id)
	cursor.execute(sql)
	db.commit()
	return redirect('index')








#################################################

#			        MODIFIER 

#################################################

@app.route("/modifier_referentiel/<int:id>",methods=['POST','GET'])
def modifier_referentiel(id):
	i_ref = recup_ref_where(id)[0]

	if request.method == 'POST':
		nomRef = request.form['nomRef']
		descRef = request.form['descRef']

		if nomRef == '' and descRef == '':
			return "les champs sont obligatoires"
		

		cursor = db.cursor()
		sql = """ UPDATE referentiels_ SET nom = "{}", descript = "{}" WHERE id = '{}' """.format(nomRef,descRef,id)
		cursor.execute(sql)
		db.commit()
		return render_template("pages/lister_referentiel.html",info=session,i_ref=recup_ref())
	
	return render_template('pages/modifier_referentiel.html',info=session,i_ref=i_ref)




@app.route("/modifier_promotion/<int:id>",methods=['POST','GET'])
def modifier_promotion(id):
	i_promo = recup_promo_where(id)[0]
	i_ref = recup_ref()

	if request.method == 'POST':
		nomPromo = request.form['nomPromo']
		dateDebutPromo = request.form['dateDebutPromo']
		dateFinPromo = request.form['dateFinPromo']
		idRefPromo = request.form['idRefPromo']

		if nomPromo == '' and dateDebutPromo == '' and dateFinPromo == '' and idRefPromo == '' :
			return "tous les champs sont obligatoires"			

		cursor = db.cursor()
		sql = "UPDATE promotions_ SET nom='{}', dateDebut='{}', dateFin='{}', id_ref='{}' WHERE id='{}'".format(nomPromo, dateDebutPromo, dateFinPromo, idRefPromo,id)
		cursor.execute(sql)
		db.commit()
		return render_template("pages/lister_promotion.html",info=session,i_promo=recup_promo())

	return render_template('pages/modifier_promotion.html',info=session,i_promo=i_promo,i_ref=i_ref)




@app.route("/modifier_apprenant/<int:id>",methods=['POST','GET'])
def modifier_apprenant(id):
	i_appr = recup_apprenants_where(id)[0]
	i_promo = recup_promo()
	
	if request.method == 'POST':
		prenomAppr = request.form['prenomAppr']
		nomAppr = request.form['nomAppr']
		dateNaissAppr = request.form['dateNaissAppr']
		idPromoAppr = request.form['idPromoAppr']

		if prenomAppr == '' and nomAppr == '' and dateNaissAppr == '' and idPromoAppr == '' :
			return "tous les champs sont obligatoires"

		cursor = db.cursor()
		sql = "UPDATE apprenants_ SET prenom='{}', nom='{}', dateNaiss='{}', id_promo='{}' WHERE id='{}'".format(prenomAppr,nomAppr,dateNaissAppr,idPromoAppr,id)
		cursor.execute(sql)
		db.commit()		
		return render_template("pages/lister_apprenant.html",info=session,i_appr=recup_apprenants())

	return render_template('pages/modifier_apprenant.html',info=session,i_promo=i_promo,i_appr=i_appr)


if __name__ == '__main__':
	app.run(debug=True)