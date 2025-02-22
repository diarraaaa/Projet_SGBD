from flask import Flask, render_template,session
from python import app
from python.Fonctions import add_eleve, add_prof, timeline_client,connect_eleve,timeline_prof,connect_prof,ajouter_devoir,info_salle

@app.route('/')
def index():
    return render_template('Main.html')

@app.route('/ConnexionEleve')
def Connexion():
    return render_template('ConnexionEleve.html')

@app.route('/InscriptionEleve')
def Inscription():
    return render_template('InscriptionEleve.html')

@app.route('/ConnexionProf')
def ConnexionP():
    return render_template('ConnexionP.html')

@app.route('/InscriptionProf')
def InscriptionP():
    return render_template('InscriptionP.html')

@app.route('/Profil')
def Profil():
    return render_template('Profil.html')

@app.route('/ajout_client', methods=['POST'])
def Ajouter_client_route():
     return add_eleve()

@app.route('/ajout_prof', methods=['POST'])
def Ajouter_prof_route():
     return add_prof()

@app.route('/infosalle', methods=['POST'])
def Infosalle_route():
     return info_salle()

@app.route('/seconnecter', methods=['POST'])
def Connecter_eleve():
     return connect_eleve()

@app.route('/seconnecterprof', methods=['POST'])
def Connecter_prof():
     return connect_prof()


@app.route('/ajoutdevoir')
def AjoutAdmin_route():
    return render_template('Ajoutdevoir.html',sess_username=session['username'])

@app.route('/ajouterun_devoir', methods=['POST'])
def Ajoutdevoir_route():
    return ajouter_devoir()
    
@app.route('/timeline')
def timeline_route():
    return timeline_client()

@app.route('/timelineP')
def timelineprof_route():
    return timeline_prof()

if __name__ == '__main__':
    app.run(debug=True)
