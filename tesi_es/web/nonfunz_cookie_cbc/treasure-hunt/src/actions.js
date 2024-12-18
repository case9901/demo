const { ITEMS } = require('./constants');

function move(state, direction) {
    const newState = { ...state };

    switch (direction) {
        case 'up':
            newState.y = Math.max(0, newState.y - 1);
            break;
        case 'down':
            newState.y = Math.min(newState.gridHeight - 1, newState.y + 1);
            break;
        case 'left':
            newState.x = Math.max(0, newState.x - 1);
            break;
        case 'right':
            newState.x = Math.min(newState.gridWidth - 1, newState.x + 1);
            break;
        default:
            break;
    }

    // Ensure onMapItems exists and is an array
    newState.onMapItems = newState.onMapItems || [];

    // Check if the new position has a locked door or treasure
    const blockingItem = newState.onMapItems.find(item => item.x === newState.x && item.y === newState.y);
    if (blockingItem) {
        if (blockingItem.item === ITEMS.LOCKED_DOOR && !newState.inventory.includes(ITEMS.KEY)) {
            // Block movement if there's a locked door and the player doesn't have a key
            return state;
        } else if (blockingItem.item === ITEMS.TREASURE && !newState.inventory.includes(ITEMS.KEY)) {
            // Block movement if there's a treasure and the player doesn't have a key
            return state;
        }
    }

    // Remove key from the map if player steps on it
    newState.onMapItems = newState.onMapItems.filter(item => {
        if (item.x === newState.x && item.y === newState.y && item.item === ITEMS.KEY) {
            newState.inventory.push(ITEMS.KEY);
            return false;
        }
        return true;
    });

    return newState;
}

module.exports = { move };



