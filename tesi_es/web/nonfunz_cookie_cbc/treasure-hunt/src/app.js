const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const exphbs = require('express-handlebars');
const { encryptToken, decryptToken } = require('./util');
const { ITEMS } = require('./constants');
const { move } = require('./actions');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

// Configure Handlebars
app.engine('handlebars', exphbs({ defaultLayout: 'main' }));
app.set('view engine', 'handlebars');
app.set('views', __dirname + '/views');

app.use(express.static(__dirname + '/../public'));

app.get('/register', (req, res) => {
    res.render('register');
});

app.post('/register', (req, res) => {
    const { username } = req.body;

    // Definisci la griglia per la prima stanza
    const room1Grid = Array.from({ length: 10 }, () => Array(10).fill({ class: 'ground' }));
    // Posiziona la chiave nella prima stanza
    room1Grid[2][8] = { class: 'key' };

    // Definisci la griglia per il corridoio
    const hallwayGrid = Array.from({ length: 10 }, () => Array(5).fill({ class: 'ground' }));
    // Posiziona la porta nel corridoio
    hallwayGrid[5][2] = { class: 'door' };

    // Definisci la griglia per la seconda stanza
    const room2Grid = Array.from({ length: 10 }, () => Array(10).fill({ class: 'ground' }));
    // Posiziona il tesoro nella seconda stanza
    room2Grid[2][7] = { class: 'treasure' };

    // Unisci le griglie delle stanze e del corridoio
    const fullGrid = [];
    for (let i = 0; i < 10; i++) {
        fullGrid.push([...room1Grid[i], ...hallwayGrid[i], ...room2Grid[i]]);
    }

    const newToken = encryptToken({
        username,
        x: 2, // Posizione iniziale nella prima stanza
        y: 2, // Posizione iniziale nella prima stanza
        inventory: [],
        gridWidth: 25, // Larghezza della griglia completa
        gridHeight: 10, // Altezza della griglia completa
        onMapItems: [
            { item: ITEMS.KEY, x: 8, y: 2 }, // Chiave nella prima stanza
            { item: ITEMS.LOCKED_DOOR, x: 12, y: 5 }, // Porta nel corridoio
            { item: ITEMS.TREASURE, x: 22, y: 2 } // Tesoro nella seconda stanza
        ]
    });
    res.cookie('game-token', newToken);
    return res.redirect('/');
});

app.get('/', (req, res) => {
    const token = req.cookies['game-token'];
    if (!token) {
        return res.redirect('/register');
    }

    let state;
    try {
        state = decryptToken(token);
    } catch (error) {
        console.error('Error decrypting token:', error);
        return res.redirect('/register');
    }

    // Ensure onMapItems is defined
    if (!state.onMapItems) {
        state.onMapItems = [];
    }

    // Generate cells for the game grid
    const cells = Array.from({ length: state.gridWidth * state.gridHeight }, (_, index) => {
        const x = index % state.gridWidth;
        const y = Math.floor(index / state.gridWidth);
        const cell = { class: 'ground' };

        if (x === state.x && y === state.y) {
            cell.class = 'player';
        } else {
            const item = state.onMapItems.find(item => item.x === x && item.y === y);
            if (item) {
                cell.class = item.item.toLowerCase();
            }
        }

        return cell;
    });

    console.log('State:', state);
    console.log('Cells:', cells);

    res.render('home', { state, cells });
});

app.post('/move', (req, res) => {
    const token = req.cookies['game-token'];
    if (!token) {
        return res.redirect('/register');
    }

    let state;
    try {
        state = decryptToken(token);
    } catch (error) {
        console.error('Error decrypting token:', error);
        return res.redirect('/register');
    }

    const newState = move(state, req.body.direction);

    const newToken = encryptToken(newState);
    res.cookie('game-token', newToken);
    return res.redirect('/');
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});












