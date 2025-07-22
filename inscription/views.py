from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import EtudiantForm
from django.conf import settings
from django.utils.html import strip_tags



def inscription_etudiant(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            etudiant = form.save()

            # Corps du message complet
            message_html = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, sans-serif;
                        color: #333;
                        background-color: #f9f9f9;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: auto;
                        background: white;
                        border-radius: 10px;
                        padding: 30px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    }}
                    h2 {{
                        color: #2c3e50;
                    }}
                    ul {{
                        padding-left: 20px;
                    }}
                    .highlight {{
                        background-color: #eaf4ff;
                        padding: 8px;
                        border-left: 4px solid #3498db;
                        margin: 10px 0;
                    }}
                    .footer {{
                        font-size: 0.9rem;
                        color: #666;
                        margin-top: 20px;
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Bonjour {etudiant.prenom} {etudiant.nom} ,</h2>
                    <p>🎉 <strong>Félicitations !</strong> Votre inscription à l’Aide Alimentaire Étudiante du Havre est bien enregistrée.</p>
                    <p><strong>Votre symbole : {etudiant.symbole.nom} {etudiant.symbole.icone} </strong> </p>

                    <div class="highlight">
                        <strong>📍 Activation sur place :</strong><br>
                        Salle Mandarine, Secours Catholique<br>
                        54 rue Michelet – Le Havre<br>
                        <strong>Le jeudi 3 octobre 2024 à partir de 16h30</strong>
                    </div>

                    <p>📅 Si vous ne pouvez pas venir à cette date, vous pouvez valider votre inscription aux dates suivantes, dès 17h30 :</p>
                    <ul>
                        <li>Jeudi 17 octobre 2024</li>
                        <li>Jeudi 24 octobre 2024</li>
                        <li>Jeudi 14 novembre 2024</li>
                        <li>Jeudi 28 novembre 2024</li>
                        <li>Jeudi 12 décembre 2024</li>
                        <li>Jeudi 19 décembre 2024</li>
                        <li>Jeudi 9 janvier 2025</li>
                        <li>Jeudi 23 janvier 2025</li>
                        <li>Jeudi 6 février 2025</li>
                        <li>Jeudi 27 février 2025</li>
                        <li>Jeudi 6 mars 2025</li>
                        <li>Jeudi 20 mars 2025</li>
                        <li>Jeudi 3 avril 2025</li>
                        <li>Jeudi 24 avril 2025</li>
                        <li><strong>Mercredi 30 avril 2025</strong> (exceptionnellement)</li>
                        <li>Jeudi 15 mai 2025</li>
                        <li>Jeudi 5 juin 2025</li>
                    </ul>

                    <p>📌  <strong>symbole de passage : </strong> {etudiant.symbole.nom} {etudiant.symbole.icone}   qui restera le même durant toutes vos études au Havre. Il vous servira pour connaître votre ordre de passage à chaque distribution.</p>

                    <p>🔔 Cet ordre de passage est publié la veille sur nos pages <strong>Facebook et Instagram : Young Caritas LH</strong>.</p>

                    <div class="highlight">
                        <strong>🎒 À apporter à chaque distribution :</strong><br>
                        - Votre carte d’étudiant<br>
                        - Une participation de <strong>4,10 €</strong> (en petite monnaie)<br>
                        - Un grand sac cabas + un sac isotherme (obligatoire pour les surgelés)
                    </div>

                    <p>🙌 Notre équipe de bénévoles Young Caritas vous accueillera avec le sourire pour vous expliquer le déroulement et répondre à vos questions.</p>

                    <p>✨ Très belle année universitaire au Havre et à très bientôt !</p>

                    <div class="footer">
                        — L’équipe des Young Caritas du Havre & l’Aumônerie Étudiante —
                    </div>
                </div>
            </body>
            </html>
            """

            # Envoie de l'email avec HTML :
            send_mail(
                subject="Bienvenue ! Votre inscription est confirmée",
                message=strip_tags(message_html),  # version texte simple fallback
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[etudiant.email],
                html_message=message_html
            )

            return render(request, 'inscription/succes.html')
    else:
        form = EtudiantForm()
    return render(request, 'inscription/inscription.html', {'form': form})


def accueil(request):
    return render(request, 'inscription/accueil.html')
