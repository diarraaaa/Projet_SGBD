from flask import Flask, jsonify, render_template, request ,session
import pymysql,os,re

app = Flask(__name__)

# Function to connect to the database using PyMySQL
def connectdatabase():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='diarra',
            password='passer',
            database='projet'
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Connection error: {e}")
        return None
def nettoyer_nom_fichier(nom_fichier):
    # Remplacer les caractères spéciaux par des tirets
    nom_fichier_nettoye = re.sub(r'[^\w.-]', '-', nom_fichier)
    return nom_fichier_nettoye
    
def add_eleve():
    try:
       
        nom = request.form['nom']
        prenom = request.form['prenom']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        classe = request.form['classe']


    
        conn = connectdatabase()
        if conn is None:
            return jsonify({'error': 'Impossible de se connecter à la base de données'})

        cursor = conn.cursor()

        
        verification_email = "SELECT * FROM eleve WHERE mail=%s"
        cursor.execute(verification_email, (email,))
        email_present = cursor.fetchone()

        
        verification_username = "SELECT * FROM eleve WHERE username=%s"
        cursor.execute(verification_username, (username,))
        username_present = cursor.fetchone()

    
        if email_present:
            error_message = 'Email déjà utilisé'
            return render_template('InscriptionEleve.html', error_message=error_message)

        if username_present:
            error_message = "Nom d'utilisateur non disponible"
            return render_template('InscriptionEleve.html', error_message=error_message)

        requete = "INSERT INTO eleve(nom, prenom, username, mail, password,classe) VALUES (%s, %s, %s, %s, %s,%s)"
        values = (nom, prenom, username, email, password,classe)
        cursor.execute(requete, values)
        conn.commit()
        cursor.close()
        conn.close()

     
        success_message = 'Inscription réussie'
        return render_template('InscriptionEleve.html', success_message=success_message)

   
    except pymysql.MySQLError as error:
        print(f"Database error: {error}")
        return jsonify({'error': str(error)})
    except KeyError:
        return jsonify({'error': 'Missing required fields'})

def add_prof():
    try:
       
        nom = request.form['nom']
        prenom = request.form['prenom']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = connectdatabase()
        if conn is None:
            return jsonify({'error': 'Impossible de se connecter à la base de données'})

        cursor = conn.cursor()

       
        verification_email = "SELECT * FROM prof WHERE mail=%s"
        cursor.execute(verification_email, (email,))
        email_present = cursor.fetchone()

        verification_username = "SELECT * FROM prof WHERE username=%s"
        cursor.execute(verification_username, (username,))
        username_present = cursor.fetchone()

   
        if email_present:
            error_message = 'Email déjà utilisé'
            return render_template('InscriptionP.html', error_message=error_message)

        if username_present:
            error_message = "Nom d'utilisateur non disponible"
            return render_template('InscriptionP.html', error_message=error_message)

        
        requete = "INSERT INTO prof(nom, prenom, username, mail, password) VALUES (%s, %s, %s, %s, %s)"
        values = (nom, prenom, username, email, password)
        cursor.execute(requete, values)
        conn.commit()
        cursor.close()
        conn.close()

        success_message = 'Inscription réussie'
        return render_template('InscriptionP.html', success_message=success_message)

    except pymysql.MySQLError as error:
        print(f"Database error: {error}")
        return jsonify({'error': str(error)})
    except KeyError:
        return jsonify({'error': 'Missing required fields'})
    
def connect_eleve():
    try:
            username=request.form['username']
            password=request.form['password']
            conn=connectdatabase()
            curseur=conn.cursor()
            #verifier si il est présent dans la base
            verification_client="Select * from eleve where username=%s and password=%s "
            curseur.execute(verification_client,(username,password))
            user_present=curseur.fetchone()

            #afficher ds messages en fonction de sa présence ou non
            if  user_present:
                 session['username']=username
                 return timeline_client()
            else:
                error_message = 'Informations érronnées'
                return render_template('Connexion.html', error_message=error_message)
                 
            #gerer les erreurs
    except pymysql.MySQLError as error:
        print(f"Database error: {error}")
        return jsonify({'error': str(error)})
    except KeyError:
        return jsonify({'error': 'Missing required fields'})

def connect_prof():
    try:
            username=request.form['username']
            password=request.form['password']
            conn=connectdatabase()
            curseur=conn.cursor()
            #verifier si il est présent dans la base
            verification_client="Select * from prof where username=%s and password=%s "
            curseur.execute(verification_client,(username,password))
            user_present=curseur.fetchone()

            #afficher ds messages en fonction de sa présence ou non
            if  user_present:
                 session['username']=username
                 return timeline_prof()
            else:
                error_message = 'Informations érronnées'
                return render_template('ConnexionP.html', error_message=error_message)
                 
            #gerer les erreurs
    except pymysql.MySQLError as error:
        print(f"Database error: {error}")
        return jsonify({'error': str(error)})
    except KeyError:
        return jsonify({'error': 'Missing required fields'})

def timeline_client():
     sess_username=session.get('username')
     connectdatabase()
     conn=connectdatabase()
     curseur=conn.cursor()
     curseur.execute("Select * from devoirprof where classe=(Select classe from eleve where username=%s)",(sess_username,))
     devoirs=curseur.fetchall()
     conn.commit()
     curseur.close()
     conn.close()
     return render_template('Timeline.html',sess_username=sess_username,devoirs=devoirs)


def info_salle():
     sess_username=session.get('username')
     connectdatabase()
     conn=connectdatabase()
     curseur=conn.cursor()
     nom=request.form['id']
     curseur.execute("Select * from devoirprof where nom=%s",(nom,))
     infodevoirs=curseur.fetchall()
     conn.commit()
     curseur.close()
     conn.close()
     return render_template('InfoSalle.html',sess_username=sess_username,infodevoirs=infodevoirs)

def timeline_prof():
     sess_username=session.get('username')
     connectdatabase()
     conn=connectdatabase()
     curseur=conn.cursor()
     conn.commit()
     curseur.close()
     conn.close()
     return render_template('TimelineP.html',sess_username=sess_username)

def nettoyer_nom_fichier(filename):
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename

def ajouter_devoir():
    try:
        # Connect to the database
        conn = connectdatabase()
        if not conn:
            return "Database connection failed.", 500

        # Define the directory for saving files
        repertoire = os.path.join('python', 'static', 'images')  # Use os.path.join for cross-platform compatibility
        if not os.path.exists(repertoire):
            print(f"Creating directory: {repertoire}")
            os.makedirs(repertoire)

        # Collect all form data
        nom = request.form.get('nom')
        description = request.form.get('description')
        type_devoir = request.form.get('typedevoir')
        classe = request.form.get('classe')
        fichier = request.files.get('fichier')  # Use request.files for file uploads
        prof = request.form.get('id')
        date = request.form.get('date')

        # Debug: Print form data
        print(f"Nom: {nom}")
        print(f"Description: {description}")
        print(f"Type: {type_devoir}")
        print(f"Classe: {classe}")
        print(f"Prof: {prof}")
        print(f"File: {fichier}")

        # Validate file upload
        if not fichier or fichier.filename == '':
            errorfichier = "No file uploaded."
            return render_template("Ajoutdevoir.html", errorfichier=errorfichier)

        # Validate file extension
        allowed_extensions = {'pdf', 'docx', 'doc'}
        file_extension = fichier.filename.rsplit('.', 1)[1].lower() if '.' in fichier.filename else ''
        if file_extension not in allowed_extensions:
            errorfichier = "File format not accepted. Only PDF, DOCX, and DOC are allowed."
            return render_template("Ajoutdevoir.html", errorfichier=errorfichier)

        # Clean the filename
        fichier_filename = nettoyer_nom_fichier(fichier.filename)
        print(f"Cleaned filename: {fichier_filename}")

        # Save the file to the directory
        file_path = os.path.join(repertoire, fichier_filename)
        print(f"Saving file to: {file_path}")
        fichier.save(file_path)

        # Verify if the file was saved
        if not os.path.exists(file_path):
            errorfichier = "Failed to save the file."
            return render_template("Ajoutdevoir.html", errorfichier=errorfichier)

        # Get the relative path for the database
        chemin1 = os.path.join('static', 'images', fichier_filename)
        print(f"Relative path for database: {chemin1}")

        # Insert data into the database
        curseur = conn.cursor()
        requete = '''
            INSERT INTO devoirprof (nom, description, type, classe, chemin, prof,date)
            VALUES (%s, %s, %s, %s, %s, %s,%s)
        '''
        values = (nom, description, type_devoir, classe, chemin1, prof,date)
        curseur.execute(requete, values)
        conn.commit()

        # Close the cursor and connection
        curseur.close()
        conn.close()

        # Success message
        success_message = "Devoir ajouté avec succès."
        return render_template("Ajoutdevoir.html", success_message=success_message)

    except pymysql.MySQLError as error:
        # Handle database errors
        print(f"Database error: {error}")
        if conn:
            conn.rollback()
            curseur.close()
            conn.close()
        return jsonify({'error': str(error)}), 500

    except KeyError:
        # Handle missing form fields
        return jsonify({'error': 'Missing required fields'}), 400

    except Exception as e:
        # Handle other exceptions
        print(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
