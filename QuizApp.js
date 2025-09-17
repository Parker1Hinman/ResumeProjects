let allDecks = {};
let deckNames = [];
let currentCardIndex = 0;
let currentDeckName = null;

const navbar = document.querySelector('.nav');
const deckInventory = document.querySelector('.deckInventoryPage');
const deckContainer = document.getElementById('viewDeckContainer');
const nameDeckContainer = document.getElementById('nameDeckContainer');
const addCardContainer = document.getElementById('addCardContainer');
const cancelButtonContainer = document.getElementById('cancelButtonContainer');

function blur() {
    deckInventory.classList.toggle('blurred');
    navbar.classList.toggle('blurred');
}

function visible(item) {
    item.classList.toggle('hidden');
    item.classList.toggle('centered');
}

const createDeckButton = document.getElementById('createDeckButton');
createDeckButton.addEventListener('click', () => {
    deckInventory.classList.toggle('hidden');
    navbar.classList.toggle('hidden');
    visible(nameDeckContainer);
    blur();
});

const confirmName = document.getElementById('confirmDeckNameButton');
confirmName.addEventListener('click', () => {
    visible(nameDeckContainer);
    visible(addCardContainer);
    
    const deckNameInput = document.getElementById('deckName');
    let newDeckName = deckNameInput.value;
    allDecks[newDeckName] = {};
    deckNames.push(newDeckName);

    deckNameInput.value = '';
});

const addCardButton = document.getElementById('addCardButton');
addCardButton.addEventListener('click', () => {
    const keyInputBox = document.getElementById('termInputBox');
    const valueInputBox = document.getElementById('definitionInputBox');
    
    const keyInputBoxValue = keyInputBox.value;
    const valueInputBoxValue = valueInputBox.value;

    let newestDeck = deckNames[deckNames.length - 1];
    allDecks[newestDeck][keyInputBoxValue] = valueInputBoxValue;

    keyInputBox.value = '';
    valueInputBox.value = '';
});

const finishDeckButton = document.getElementById('finishDeckButton');
finishDeckButton.addEventListener('click',() => {
    const createDeck = document.createElement('div');
    createDeck.textContent = deckNames[deckNames.length - 1];
    createDeck.classList.add('deck','centeredDeck');
    createDeck.setAttribute('data-deck', createDeck.textContent);
    deckContainer.appendChild(createDeck);

    visible(addCardContainer);
    deckInventory.classList.toggle('hidden');
    navbar.classList.toggle('hidden');
    blur();

    createDeck.addEventListener('click', (event) => {
        const pageLocation = document.getElementById('pageLocation');
        pageLocation.textContent = 'Review';
        const cardContainer = document.querySelector('.cardContainer');
        cardContainer.classList.toggle('hidden');
        deckContainer.style.display = 'none';
        deckInventory.classList.toggle('hidden');
        const selectedDeckName = event.currentTarget.getAttribute('data-deck');
        currentDeckName = event.currentTarget.getAttribute('data-deck');
        currentCardIndex = 0;
        showCardText(selectedDeckName);
    });
});

const front = document.getElementById('front');
const back = document.getElementById('back');
const cardInner = document.getElementById('cardInner');

let flipped = false
cardInner.addEventListener('click', () => {
    flipped = !flipped;
    cardInner.classList.toggle('flipped');
});

function showCardText(selectedDeckName) {
    const currentDeck = allDecks[selectedDeckName];
    const terms = Object.keys(currentDeck);

    const term = terms[currentCardIndex]
    const definition = currentDeck[term]
    
    front.textContent = term;
    back.textContent = definition;
}

const nextButton = document.getElementById('nextButton');

nextButton.addEventListener('click', (event) => {
    if (!currentDeckName) return;
    const currentDeck = allDecks[currentDeckName];
    const terms = Object.keys(currentDeck);
    if (currentCardIndex < terms.length - 1) {
        currentCardIndex ++;
        showCardText(currentDeckName);
    }
});

const prevButton = document.getElementById('previousButton');
prevButton.addEventListener('click', (event) => {
    if (!currentDeckName) return;
   if (currentCardIndex>0) {
        currentCardIndex--;
        const selectedDeckName = event.currentTarget.getAttribute('data-deck');
        showCardText(selectedDeckName)
   } 
});