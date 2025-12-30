// ============================================
//  FONCTIONS COMMUNES - PAGE D'ACCUEIL
// ============================================

function updateModeLabel() {
    const toggle = document.getElementById('autoToggle');
    const label = document.getElementById('modeLabel');
    
    if (toggle && label) {
        if (toggle.checked) {
            label.textContent = 'Grisage Auto';
            label.style.color = '#4CAF50';
        } else {
            label.textContent = 'Grisage Manuel';
            label.style.color = '#FF9800';
        }
    }
}

// Lancer le jeu solo depuis les radio buttons des cartes
function startSolo() {
    const radioChecked = document.querySelector('input[name="grisage"]:checked');
    if (radioChecked) {
        window.location.href = '/jeu?auto_grey=' + radioChecked.value;
    }
}

// Lancer le jeu duo depuis les radio buttons des cartes
function startDuo(difficulty) {
    const radioChecked = document.querySelector('input[name="grisage"]:checked');
    if (radioChecked) {
        window.location.href = '/choisir_mode_duo?difficulty=' + difficulty + '&auto_grey=' + radioChecked.value;
    }
}

// Lancer le jeu depuis le toggle de la navbar
function launchGame(mode) {
    const autoToggle = document.getElementById('autoToggle');
    if (!autoToggle) return;
    
    const autoGrey = autoToggle.checked;
    
    if (mode === 'solo') {
        window.location.href = '/jeu?auto_grey=' + autoGrey;
    } else if (mode === 'duo-easy') {
        window.location.href = '/choisir_mode_duo?difficulty=easy&auto_grey=' + autoGrey;
    } else if (mode === 'duo-hard') {
        window.location.href = '/choisir_mode_duo?difficulty=hard&auto_grey=' + autoGrey;
    }
}

//Initialiser le toggle au chargement de la page
window.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('autoToggle')) {
        updateModeLabel();
    }
});

// ============================================
//  FONCTIONS COMMUNES - MODAL
// ============================================

function initModal() {
    const modal = document.getElementById("info-modal");
    const modalImg = document.getElementById("modal-img");
    const modalTitle = document.getElementById("modal-title");
    const modalDesc = document.getElementById("modal-desc");
    const closeBtn = document.querySelector(".close-modal");

    if (!modal) return null;

    if (closeBtn) {
        closeBtn.onclick = function() {
            modal.style.display = "none";
        }
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    return { modal, modalImg, modalTitle, modalDesc };
}
