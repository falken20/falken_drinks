// Add this function to your existing falken.js file
function selectDrink(drinkType) {
    console.log("Selected drink: " + drinkType);
    
    // Highlight the selected icon
    const icons = document.querySelectorAll('.drink-icon');
    icons.forEach(icon => {
        icon.style.transform = 'scale(1)';
        icon.querySelector('img').style.boxShadow = 'none';
    });
    
    // Find the clicked element and highlight it
    const clickedIcon = event.currentTarget;
    clickedIcon.style.transform = 'scale(1.1)';
    clickedIcon.querySelector('img').style.boxShadow = '0 0 10px rgba(255, 255, 255, 0.8)';
    
    // Set the corresponding radio button
    let radioId;
    switch(drinkType) {
        case 'Water':
            radioId = 'water';
            break;
        case 'Coffee':
            radioId = 'coffee';
            break;
        case 'Wine':
        case 'Beer':
        case 'Cocktail':
        case 'Shot':
            radioId = 'alcohol';
            break;
        default:
            radioId = 'other';
            
            // If it's "other", show the select dropdown
            const otherSelect = document.getElementById('other-drink-select');
            if (otherSelect) {
                otherSelect.style.display = 'inline-block';
                
                // Try to select the matching option if it exists
                for (let i = 0; i < otherSelect.options.length; i++) {
                    if (otherSelect.options[i].text === drinkType) {
                        otherSelect.selectedIndex = i;
                        break;
                    }
                }
            }
    }
    
    // Set the corresponding radio button
    const radioButton = document.getElementById(radioId);
    if (radioButton) {
        radioButton.checked = true;
        
        // Trigger the change event to ensure any listeners are notified
        const event = new Event('change');
        radioButton.dispatchEvent(event);
    }
    
    // Suggest an amount based on drink type
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        switch(drinkType) {
            case 'Water':
                amountInput.value = '250';
                break;
            case 'Coffee':
                amountInput.value = '200';
                break;
            case 'Wine':
                amountInput.value = '150';
                break;
            case 'Beer':
                amountInput.value = '330';
                break;
            case 'Cocktail':
                amountInput.value = '200';
                break;
            case 'Shot':
                amountInput.value = '45';
                break;
            case 'Soda':
                amountInput.value = '330';
                break;
            case 'Milk':
                amountInput.value = '250';
                break;
            case 'Energy':
                amountInput.value = '250';
                break;
            default:
                amountInput.value = '200';
        }
    }
}
