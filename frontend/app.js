// Cibler les éléments nécessaires
const playButton = document.getElementById('play-button');
const mainContent = document.getElementById('main-content');
const dashContent = document.getElementById('dashboard-content');
const loginForm = document.getElementById('login-form');
const chatContent = document.getElementById('chat-content');
const chatButton = document.getElementById('chat-button');
const homeButton = document.getElementById('home-button');
const dashboardButton = document.getElementById('dashboard-button');
const connexionButton = document.getElementById('connexion-button');
const signupButton = document.getElementById('signup-button');
const createAccountButton = document.getElementById('create-account-button'); // Créer un compte
const signupForm = document.getElementById('signup-form');
const backToLoginButton = document.getElementById('back-to-login');
const signupNavbarButton = document.getElementById('signup-navbar-button');
// Variable globale pour connaitre la vue actuelle et gerer l'historique
let currentView = 'home';

// Fonction pour basculer entre les vues
function changeView(view) {
    if (view === 'home') {
        mainContent.style.display = 'flex';
        loginForm.style.display = 'none';
        chatContent.style.display = 'none';
        dashContent.style.display = 'none';
        signupForm.style.display = 'none';
    } else if (view === 'login') {
        mainContent.style.display = 'none';
        loginForm.style.display = 'flex';
        chatContent.style.display = 'none';
        dashContent.style.display = 'none';
        signupForm.style.display = 'none';
    } else if (view === 'chat') {
        mainContent.style.display = 'none';
        loginForm.style.display = 'none';
        chatContent.style.display = 'grid';
        dashContent.style.display = 'none';
        signupForm.style.display = 'none';
    } else if (view === 'signup') {
        mainContent.style.display = 'none';
        loginForm.style.display = 'none';
        chatContent.style.display = 'none';
        dashContent.style.display = 'none';
        signupForm.style.display = 'flex';
    }
    currentView = view;
}


// Ajouter un événement au clic sur le bouton "PLAY"
playButton.addEventListener('click', () => {
	if (currentView !== 'login'){
		changeView('login');
		history.pushState({ view: 'login' }, '', '#login');}
});

connexionButton.addEventListener('click', () => {
	if (currentView !== 'login'){
		changeView('login');
		history.pushState({ view: 'login' }, '', '#login');}
});

// Ajouter un événement au clic sur le bouton "CHAT"
chatButton.addEventListener('click', () => {
	if (currentView !== 'chat'){
		changeView('chat');
		history.pushState({ view: 'chat' }, '', '#chat');}
})

homeButton.addEventListener('click', () => {
	if (currentView !== 'home'){
		changeView('home');
		history.pushState({ view: 'home' }, '', '#home');}
})

// Gérer les changements de l'historique
window.onpopstate = (event) => {
	const state = event.state;
	if (state && state.view)
		changeView(state.view);
	else
		changeView('home');
};

// Initialiser la vue en fonction de l'URL
window.addEventListener('load', () => {
    const hash = window.location.hash;
    if (hash === '#login') {
        changeView('login');
    } else if (hash === '#chat') {
        changeView('chat');
    } else if (hash === '#signup') {
        changeView('signup');
    } else {
        changeView('home');
    }
});

signupButton.addEventListener('click', () => {
    if (currentView !== 'signup') {
        changeView('signup');
        history.pushState({ view: 'signup' }, '', '#signup');
    }
});

backToLoginButton.addEventListener('click', () => {
    if (currentView !== 'login') {
        changeView('login');
        history.pushState({ view: 'login' }, '', '#login');
    }
});

signupNavbarButton.addEventListener('click', () => {
    if (currentView !== 'signup') {
        changeView('signup');
        history.pushState({ view: 'signup' }, '', '#signup');
    }
});


createAccountButton.addEventListener('click', async (event) => {
    event.preventDefault(); // Empêcher la soumission par défaut du formulaire

    const username = document.getElementById('new-username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('new-password').value.trim();

    // Valider les champs requis
    if (!username || !email || !password) {
        alert('Tous les champs sont obligatoires.');
        return;
    }

    // Optionnel : Valider le format de l'email avec une expression régulière
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Veuillez entrer une adresse e-mail valide.");
        return;
    }

    // Optionnel : Vérifier la force du mot de passe
    if (password.length < 8) {
        alert("Le mot de passe doit contenir au moins 8 caractères.");
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/api/users/signup/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Inscription réussie !');
        } else {
            alert(`Erreur : ${data.error}`);
        }
    } catch (error) {
        console.error('Erreur lors de la requête :', error);
        alert('Erreur de connexion au serveur.');
    }
});





const normalLoginButton = document.getElementById('normal-login-button');

normalLoginButton.addEventListener('click', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        alert('Veuillez remplir tous les champs.');
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
            credentials: 'include',  // S'assurer que les cookies sont envoyés avec la requête
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message);

            // Stocker le jeton d'accès dans le localStorage (ou sessionStorage)
            localStorage.setItem('access_token', data.access_token);

            // Mettre à jour la navbar après connexion réussie
            updateNavbar(data.username);
            changeView('home');
            history.pushState({ view: 'home' }, '', '#home');
        } else {
            const errorData = await response.json();
            alert(`Erreur : ${errorData.error}`);
        }
    } catch (error) {
        console.error('Erreur lors de la requête :', error);
        alert('Une erreur est survenue. Veuillez réessayer.');
    }
});






const login42Button = document.getElementById('login-42-button');
login42Button.addEventListener('click', () => {
    window.location.href = 'http://localhost:8000/42/login/';
});

const logoutButton = document.getElementById('logout-button');
const userInfoButton = document.getElementById('user-info-button');

// Fonction pour mettre à jour la barre de navigation selon l'état de connexion
function updateNavbar(username) {
    if (username) {
        // Utilisateur connecté
        document.getElementById('connexion-button').style.display = 'none';
        document.getElementById('signup-navbar-button').style.display = 'none';
        document.getElementById('logout-button').style.display = 'inline-block';
        document.getElementById('user-info-button').style.display = 'inline-block';
        document.getElementById('user-info-button').textContent = `Bonjour, ${username}`;
    } else {
        // Utilisateur déconnecté
        document.getElementById('connexion-button').style.display = 'inline-block';
        document.getElementById('signup-navbar-button').style.display = 'inline-block';
        document.getElementById('logout-button').style.display = 'none';
        document.getElementById('user-info-button').style.display = 'none';
    }
}

window.addEventListener('load', async () => {
    // Vérification du token d'authentification dans le stockage local
    const token = localStorage.getItem('access_token');
    if (token) {
        // L'utilisateur est connecté, mettez à jour la navbar
        updateNavbar('Utilisateur connecté');
        changeView('home');
        history.pushState({ view: 'home' }, '', '#home');
    } else {
        // L'utilisateur n'est pas connecté, afficher la page de login
        updateNavbar(null);
        changeView('login');
    }
});




// Action de déconnexion
logoutButton.addEventListener('click', async () => {
    try {
        const response = await fetch('http://localhost:8000/auth/logout/', {
            method: 'POST',
            credentials: 'include',
        });
        if (response.ok) {
            alert('Déconnexion réussie');
            updateNavbar(null); // Réinitialiser la navbar
            changeView('home');  // Retourner à l'écran d'accueil
        } else {
            alert('Erreur lors de la déconnexion');
        }
    } catch (error) {
        console.error('Erreur lors de la déconnexion:', error);
    }
});












