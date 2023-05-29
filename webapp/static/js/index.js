languages = {
    'en': {
        "rfid-text": "Scan your card to start!",
        "pin-text": "Press 'A' to continue",
        "blocked-text": "Your card has been blocked!",
        "balance": "Balance",
        "withdraw": "Withdraw",
        "cancel": "Cancel",
        "choice-menu-text": "Select an option:",
        "return": "Return",
        "wait-text" : "Hold on for a second...",
        "yes" : "Yes",
        "no" : "No",
        "bon-text" : "Would you like a receipt?",
        "end-text" : "Thank you for using our ATM!",
        "custom" : "custom",
        "increase" : "Increase *",
        "decrease" : "Decrease #",
        "wrong-pin-text" : "Wrong PIN, try again",
        "exceeded-text" : "You have exceeded your accounts balance"
    },
    'fr': {
        "rfid-text": "Passez votre carte pour commencer!",
        "pin-text": "Appuyez sur 'A' pour continuer",
        "blocked-text": "Votre carte a été bloquée !",
        "balance": "Solde",
        "withdraw": "Retirer",
        "cancel": "Annuler",
        "choice-menu-text": "Veuillez sélectionner une option :",
        "return": "Retour",
        "wait-text" : "Un instant s'il vous plaît...",
        "yes" : "Oui",
        "no" : "Non",
        "bon-text" : "Souhaitez-vous un reçu ?",
        "end-text" : "Merci d'avoir utilisé notre distributeur automatique !",
        "custom" : "personnalisé",
        "increase" : "Augmenter *",
        "decrease" : "Diminuer #",
        "wrong-pin-text": "Mauvais code PIN, réessayez",
        "exceeded-text": "Vous avez dépassé le solde de votre compte."
    },
    'de': {
        "rfid-text": "Legen Sie Ihre Karte ein, um zu beginnen!",
        "pin-text": "Drücken Sie 'A', um fortzufahren",
        "blocked-text": "Ihre Karte wurde gesperrt!",
        "balance": "Kontostand",
        "withdraw": "Abheben",
        "cancel": "Abbrechen",
        "choice-menu-text": "Bitte wählen Sie eine Option:",
        "return": "Zurück",
        "wait-text" : "Einen Moment bitte...",
        "yes" : "Ja",
        "no" : "Nein",
        "bon-text" : "Möchten Sie einen Beleg?",
        "end-text" : "Vielen Dank für die Nutzung unseres Geldautomaten!",
        "custom" : "individuell",
        "increase" : "Erhöhen *",
        "decrease" : "Verringern #",
        "wrong-pin-text": "Falsche PIN, bitte erneut versuchen",
        "exceeded-text": "Sie haben Ihr Kontoguthaben überschritten."
    },
    'nl': {
        "rfid-text": "Scan uw kaart om te beginnen!",
        "pin-text": "Druk op 'A' om door te gaan",
        "blocked-text": "Uw kaart is geblokkeerd!",
        "balance": "Saldo",
        "withdraw": "Opnemen",
        "cancel": "Annuleren",
        "choice-menu-text": "Selecteer een optie:",
        "return": "Terug",
        "wait-text" : "Een ogenblik geduld a.u.b...",
        "yes" : "Ja",
        "no" : "Nee",
        "bon-text" : "Wilt u een bon?",
        "end-text" : "Bedankt voor het gebruik van onze pinautomaat!",
        "custom" : "aangepast",
        "increase" : "Verhogen *",
        "decrease" : "Verlagen #",
        "wrong-pin-text": "Verkeerde PIN, probeer opnieuw",
        "exceeded-text": "U heeft uw accountsaldo overschreden."
    }
}

  
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function setLanguage(lang) {
    lang = lang || 'en'; // If lang is not provided, set it to 'en'
    document.cookie = `language=${lang}; path=/`; // Set the cookie for all paths
    language = lang;
    update();
}

function update() {
	const elementsToUpdate = document.querySelectorAll('.text');
	elementsToUpdate.forEach(function(element) {
		const update = languages[language][element.id];
		element.textContent = update;
	});
}

var language = getCookie('language');
if (language == null) {
    setLanguage('en'); // Set default language to 'en'
} else {
    update();
}


document.addEventListener('keypress', function(event) {
	if (event.key === 'C') {
	  window.location.href = '/';
	}
});