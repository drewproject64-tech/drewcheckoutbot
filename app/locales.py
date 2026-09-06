from __future__ import annotations

TEXTS = {
    "en": {
        "welcome": "Welcome to Drew FX VIP 🚀\n\nPlease select your language:",
        "language_saved": "Language saved. Welcome to Drew FX VIP.",
        "join_vip": "Choose your Drew FX VIP plan:",
        "payment_choose": "Choose a plan to continue:",
        "no_subscription": "📋 You do not have an active Drew FX VIP subscription.",
        "contact_admin": "👤 Contact Drew FX admin:\n{contact}",
        "payment_title": "💳 Drew FX VIP Payment",
        "payment_instructions": "💳 Drew FX VIP Payment\n\nPlan: {plan}\nAmount: ${amount:.2f} USDT\nNetwork: {network}\n\nSend exactly ${amount:.2f} USDT to:\n\n{wallet}\n\nAfter payment, send your payment screenshot here.\nThen send the transaction hash.\n\nYour payment will remain pending until an admin verifies it.",
        "send_screenshot": "Please send the payment screenshot as an image/photo.",
        "screenshot_received": "✅ Screenshot received.\n\nNow send your USDT transaction hash as a text message.",
        "invalid_tx": "Please send a valid transaction hash as text (8–255 characters).",
        "duplicate_tx": "❌ This transaction hash has already been submitted. Please contact the admin if you believe this is an error.",
        "payment_submitted": "✅ Payment submitted successfully.\n\nPayment ID: #{payment_id}\nStatus: Pending admin review\n\nYou will receive a message after verification.",
        "approval": "✅ Payment approved!\n\nWelcome to Drew FX VIP.\n\nJoin the VIP channel:\n{channel}\n\nAfter joining, contact:\n{contact}\n\nPlan: {plan}\nExpires: {expires}\nGrace until: {grace}",
        "rejection": "❌ Payment rejected.\n\nReason: {reason}\n\nPlease contact the admin if you believe this was a mistake.",
        "subscription": "📋 My Subscription\n\nPlan: {plan}\nStatus: {status}\n\nExpires: {expires}\nGrace until: {grace}\n\nTime remaining: approximately {days} day(s)",
        "renewal": "⏰ Your Drew FX VIP subscription expires in {days} day(s).\n\nPlease renew before your subscription ends to avoid losing access.",
        "grace": "⚠️ Your Drew FX VIP subscription has expired.\n\nYou have {days} extra day(s) to renew before your VIP access is removed.",
        "removed": "❌ Your Drew FX VIP subscription and grace period have ended.\n\nYour VIP access has been removed.\nPlease renew if you would like to continue.",
        "restart": "Welcome to Drew FX VIP 🚀\n\nPlease select your language:",
        "unauthorized": "You are not authorized to use this action.",
        "invalid_plan": "That plan is no longer available. Please return to the menu and try again.",
        "approved_admin": "✅ Payment #{payment_id} approved by admin {admin_id}.",
        "rejected_admin": "❌ Payment #{payment_id} rejected by admin {admin_id}.",
    },
    "it": {
        "welcome": "Benvenuto in Drew FX VIP 🚀\n\nSeleziona la tua lingua:",
        "language_saved": "Lingua salvata. Benvenuto in Drew FX VIP.",
        "join_vip": "Scegli il tuo piano Drew FX VIP:", "payment_choose": "Scegli un piano per continuare:",
        "no_subscription": "📋 Non hai un abbonamento Drew FX VIP attivo.",
        "contact_admin": "👤 Contatta l'amministratore Drew FX:\n{contact}",
        "payment_instructions": "💳 Pagamento Drew FX VIP\n\nPiano: {plan}\nImporto: ${amount:.2f} USDT\nRete: {network}\n\nInvia esattamente ${amount:.2f} USDT a:\n\n{wallet}\n\nDopo il pagamento, invia qui lo screenshot.\nPoi invia l'hash della transazione.\n\nIl pagamento resterà in sospeso fino alla verifica.",
        "send_screenshot": "Invia lo screenshot del pagamento come foto/immagine.", "screenshot_received": "✅ Screenshot ricevuto.\n\nOra invia l'hash della transazione USDT.",
        "invalid_tx": "Invia un hash di transazione valido come testo (8–255 caratteri).", "duplicate_tx": "❌ Questo hash è già stato inviato. Contatta l'amministratore se ritieni sia un errore.",
        "payment_submitted": "✅ Pagamento inviato con successo.\n\nID pagamento: #{payment_id}\nStato: In attesa di verifica admin\n\nRiceverai un messaggio dopo la verifica.",
        "approval": "✅ Pagamento approvato!\n\nBenvenuto in Drew FX VIP.\n\nUnisciti al canale VIP:\n{channel}\n\nDopo l'ingresso, contatta:\n{contact}\n\nPiano: {plan}\nScade: {expires}\nPeriodo di tolleranza fino a: {grace}",
        "rejection": "❌ Pagamento rifiutato.\n\nMotivo: {reason}\n\nContatta l'amministratore se ritieni sia un errore.",
        "subscription": "📋 Il mio abbonamento\n\nPiano: {plan}\nStato: {status}\n\nScade: {expires}\nTolleranza fino a: {grace}\n\nTempo rimanente: circa {days} giorno/i",
        "renewal": "⏰ Il tuo abbonamento Drew FX VIP scade tra {days} giorno/i.\n\nRinnova prima della scadenza per evitare la perdita dell'accesso.",
        "grace": "⚠️ Il tuo abbonamento Drew FX VIP è scaduto.\n\nHai {days} giorni extra per rinnovare prima della rimozione.",
        "removed": "❌ Il tuo abbonamento e il periodo di tolleranza sono terminati.\n\nL'accesso VIP è stato rimosso.\nRinnova per continuare.",
        "restart": "Benvenuto in Drew FX VIP 🚀\n\nSeleziona la tua lingua:", "unauthorized": "Non sei autorizzato a usare questa azione.", "invalid_plan": "Questo piano non è più disponibile.",
        "approved_admin": "✅ Pagamento #{payment_id} approvato dall'admin {admin_id}.", "rejected_admin": "❌ Pagamento #{payment_id} rifiutato dall'admin {admin_id}.",
    },
    "fr": {
        "welcome": "Bienvenue sur Drew FX VIP 🚀\n\nVeuillez sélectionner votre langue :", "language_saved": "Langue enregistrée. Bienvenue sur Drew FX VIP.",
        "join_vip": "Choisissez votre forfait Drew FX VIP :", "payment_choose": "Choisissez un forfait pour continuer :", "no_subscription": "📋 Vous n'avez aucun abonnement Drew FX VIP actif.",
        "contact_admin": "👤 Contacter l'administrateur Drew FX :\n{contact}", "payment_instructions": "💳 Paiement Drew FX VIP\n\nForfait : {plan}\nMontant : ${amount:.2f} USDT\nRéseau : {network}\n\nEnvoyez exactement ${amount:.2f} USDT à :\n\n{wallet}\n\nAprès le paiement, envoyez la capture d'écran ici.\nPuis envoyez le hash de transaction.\n\nLe paiement restera en attente jusqu'à vérification.",
        "send_screenshot": "Veuillez envoyer la capture du paiement comme photo/image.", "screenshot_received": "✅ Capture reçue.\n\nEnvoyez maintenant le hash de votre transaction USDT.",
        "invalid_tx": "Envoyez un hash de transaction valide (8–255 caractères).", "duplicate_tx": "❌ Ce hash a déjà été soumis. Contactez l'administrateur si nécessaire.",
        "payment_submitted": "✅ Paiement envoyé avec succès.\n\nID de paiement : #{payment_id}\nStatut : Vérification admin en attente\n\nVous recevrez un message après vérification.",
        "approval": "✅ Paiement approuvé !\n\nBienvenue sur Drew FX VIP.\n\nRejoignez le canal VIP :\n{channel}\n\nAprès avoir rejoint, contactez :\n{contact}\n\nForfait : {plan}\nExpire : {expires}\nGrâce jusqu'au : {grace}",
        "rejection": "❌ Paiement refusé.\n\nMotif : {reason}\n\nContactez l'administrateur si vous pensez qu'il s'agit d'une erreur.",
        "subscription": "📋 Mon abonnement\n\nForfait : {plan}\nStatut : {status}\n\nExpire : {expires}\nGrâce jusqu'au : {grace}\n\nTemps restant : environ {days} jour(s)",
        "renewal": "⏰ Votre abonnement Drew FX VIP expire dans {days} jour(s).\n\nRenouvelez avant l'expiration pour éviter de perdre l'accès.",
        "grace": "⚠️ Votre abonnement Drew FX VIP a expiré.\n\nVous avez {days} jour(s) supplémentaires pour renouveler.", "removed": "❌ Votre abonnement et votre période de grâce sont terminés.\n\nVotre accès VIP a été supprimé.\nRenouvelez pour continuer.",
        "restart": "Bienvenue sur Drew FX VIP 🚀\n\nVeuillez sélectionner votre langue :", "unauthorized": "Vous n'êtes pas autorisé à utiliser cette action.", "invalid_plan": "Ce forfait n'est plus disponible.", "approved_admin": "✅ Paiement #{payment_id} approuvé par l'admin {admin_id}.", "rejected_admin": "❌ Paiement #{payment_id} refusé par l'admin {admin_id}.",
    },
    "de": {
        "welcome": "Willkommen bei Drew FX VIP 🚀\n\nBitte Sprache auswählen:", "language_saved": "Sprache gespeichert. Willkommen bei Drew FX VIP.", "join_vip": "Wähle deinen Drew FX VIP Plan:", "payment_choose": "Wähle einen Plan, um fortzufahren:", "no_subscription": "📋 Du hast kein aktives Drew FX VIP Abonnement.", "contact_admin": "👤 Drew FX Admin kontaktieren:\n{contact}",
        "payment_instructions": "💳 Drew FX VIP Zahlung\n\nPlan: {plan}\nBetrag: ${amount:.2f} USDT\nNetzwerk: {network}\n\nSende genau ${amount:.2f} USDT an:\n\n{wallet}\n\nNach der Zahlung sende den Screenshot hier.\nDanach den Transaktions-Hash.\n\nDie Zahlung bleibt ausstehend, bis ein Admin sie prüft.", "send_screenshot": "Bitte sende den Zahlungsscreenshot als Foto/Bild.", "screenshot_received": "✅ Screenshot erhalten.\n\nSende jetzt den USDT-Transaktions-Hash.", "invalid_tx": "Bitte einen gültigen Transaktions-Hash als Text senden (8–255 Zeichen).", "duplicate_tx": "❌ Dieser Transaktions-Hash wurde bereits eingereicht. Kontaktiere den Admin bei einem Fehler.",
        "payment_submitted": "✅ Zahlung erfolgreich eingereicht.\n\nZahlungs-ID: #{payment_id}\nStatus: Admin-Prüfung ausstehend\n\nDu erhältst nach der Prüfung eine Nachricht.", "approval": "✅ Zahlung genehmigt!\n\nWillkommen bei Drew FX VIP.\n\nVIP-Kanal beitreten:\n{channel}\n\nDanach kontaktieren:\n{contact}\n\nPlan: {plan}\nAblauf: {expires}\nKulanz bis: {grace}", "rejection": "❌ Zahlung abgelehnt.\n\nGrund: {reason}\n\nKontaktiere den Admin, wenn du glaubst, dass dies ein Fehler ist.", "subscription": "📋 Mein Abonnement\n\nPlan: {plan}\nStatus: {status}\n\nAblauf: {expires}\nKulanz bis: {grace}\n\nVerbleibende Zeit: ca. {days} Tag(e)", "renewal": "⏰ Dein Drew FX VIP Abonnement läuft in {days} Tag(en) ab.\n\nBitte vor Ablauf verlängern.", "grace": "⚠️ Dein Drew FX VIP Abonnement ist abgelaufen.\n\nDu hast {days} zusätzliche Tag(e) zum Verlängern.", "removed": "❌ Dein Abonnement und die Kulanzzeit sind abgelaufen.\n\nDein VIP-Zugang wurde entfernt.\nBitte verlängern, um fortzufahren.", "restart": "Willkommen bei Drew FX VIP 🚀\n\nBitte Sprache auswählen:", "unauthorized": "Du bist für diese Aktion nicht autorisiert.", "invalid_plan": "Dieser Plan ist nicht mehr verfügbar.", "approved_admin": "✅ Zahlung #{payment_id} von Admin {admin_id} genehmigt.", "rejected_admin": "❌ Zahlung #{payment_id} von Admin {admin_id} abgelehnt.",
    },
}


def get_text(key: str, language: str, **kwargs: object) -> str:
    lang = language if language in TEXTS else "en"
    template = TEXTS[lang].get(key, TEXTS["en"].get(key, key))
    return template.format(**kwargs)
