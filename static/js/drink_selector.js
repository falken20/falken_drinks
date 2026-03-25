// Initialize all event listeners when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize time input with current time
    const drinkTimeInput = document.getElementById('drink-time');
    if (drinkTimeInput) {
        const now = new Date();
        const hh = String(now.getHours()).padStart(2, '0');
        const mm = String(now.getMinutes()).padStart(2, '0');
        drinkTimeInput.value = hh + ':' + mm;
    }

    // Restore repeat banner from sessionStorage
    const savedDrink = sessionStorage.getItem('lastDrinkData');
    if (savedDrink) {
        lastDrinkData = JSON.parse(savedDrink);
        showRepeatBanner(lastDrinkData);
    }

    // Set up the "Other" drink selection dropdown visibility
    const otherRadio = document.getElementById('other');
    const otherSelect = document.getElementById('other-drink-select');
    const drinkRadios = document.getElementsByName('drink');
    
    if (drinkRadios && otherRadio && otherSelect) {
        drinkRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (otherRadio.checked) {
                    otherSelect.style.display = 'inline-block';
                } else {
                    otherSelect.style.display = 'none';
                }
            });
        });
    }
    
    // Set up alcohol percentage select change handler
    const alcoholPercentageSelect = document.getElementById('alcohol-percentage');
    if (alcoholPercentageSelect) {
        alcoholPercentageSelect.addEventListener('change', function() {
            const customAlcoholContainer = document.getElementById('custom-alcohol-container');
            if (alcoholPercentageSelect.value === 'custom' && customAlcoholContainer) {
                customAlcoholContainer.style.display = 'flex';
                document.getElementById('custom-alcohol').focus();
            } else {
                document.getElementById('custom-alcohol-container').style.display = 'none';
            }
        });
    }
    
    // Add event listener for custom amount input to handle Enter key
    const customAmountInput = document.getElementById('custom-amount');
    if (customAmountInput) {
        customAmountInput.addEventListener('keyup', function(event) {
            if (event.key === "Enter") {
                confirmCustomAmount();
            }
        });
    }
    
    // Add event listener for custom alcohol input to handle Enter key
    const customAlcoholInput = document.getElementById('custom-alcohol');
    if (customAlcoholInput) {
        customAlcoholInput.addEventListener('keyup', function(event) {
            if (event.key === "Enter") {
                confirmCustomAlcohol();
            }
        });
    }
    
    // Set up drink radio buttons to show/hide alcohol percentage selector
    const alcoholPercentageContainer = document.getElementById('alcohol-percentage-container');
    const customAlcoholContainer = document.getElementById('custom-alcohol-container');
    
    if (drinkRadios && alcoholPercentageContainer && alcoholPercentageSelect) {
        drinkRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'Wine' || this.value === 'Beer' || this.value === 'Cocktail' || this.value === 'Shot') {
                    alcoholPercentageContainer.style.display = 'flex';
                } else {
                    alcoholPercentageContainer.style.display = 'none';
                    alcoholPercentageSelect.value = '0'; // Reset to 0% if not an alcoholic drink
                    if (customAlcoholContainer) {
                        customAlcoholContainer.style.display = 'none'; // Hide custom alcohol input
                    }
                }
            });
        });
    }
});

// Global variable for selected amount
let selectedDrink = 'Water'; // Default drink selected
let selectedAmount = 100; // Default amount
let radioId = 'water'; // Default drink type
let drinkChosen = false;  // true only after user explicitly taps a drink icon
let amountChosen = false; // true only after user explicitly taps an amount option
let lastDrinkData = null; // Stores last added drink for repeat functionality

function showCarouselError(carouselClass, message) {
    const carousel = document.querySelector('.' + carouselClass);
    if (!carousel) return;
    const wrapper = carousel.closest('div[style*="border-radius: 15px"]') || carousel.parentElement;
    let err = wrapper.querySelector('.carousel-error');
    if (!err) {
        err = document.createElement('div');
        err.className = 'carousel-error';
        err.style.cssText = 'display:inline-block; background:#dc3545; color:#fff; font-size:0.78rem; font-weight:600; padding:3px 12px; border-radius:20px; margin:4px auto 2px; text-align:center;';
        wrapper.appendChild(err);
    }
    err.textContent = message;
    setTimeout(() => { if (err) err.textContent = ''; }, 2500);
}

function clearCarouselError(carouselClass) {
    const carousel = document.querySelector('.' + carouselClass);
    if (!carousel) return;
    const wrapper = carousel.closest('div[style*="border-radius: 15px"]') || carousel.parentElement;
    const err = wrapper.querySelector('.carousel-error');
    if (err) err.textContent = '';
}

/**
 * Function to add a drink
 */
function addDrink() {
    const drinkForm = document.getElementById('drink-form');
    
    console.log("Adding drink...");
    console.log("Selected drink: " + selectedDrink);
    console.log("Selected amount: " + selectedAmount);
    console.log("Selected alcohol percentage: " + getSelectedAlcoholPercentage());
    console.log("Drink Type: " + radioId);

    let valid = true;

    if (!drinkChosen) {
        showCarouselError('drink-carousel', '⚠ Please select a drink first');
        valid = false;
    }

    const amount = selectedAmount;

    if (!amountChosen || !amount || isNaN(amount) || amount <= 0) {
        showCarouselError('amount-carousel', '⚠ Please select an amount first');
        valid = false;
    }

    if (!valid) return;

    // If "Other" is selected, get the specific drink type from the dropdown
    let drinkType = selectedDrink;
    if (selectedDrink === "Other") {
        const otherSelect = document.getElementById('other-drink-select');
        if (otherSelect && otherSelect.selectedIndex >= 0) {
            drinkType = otherSelect.options[otherSelect.selectedIndex].value;
        }
    }
    
    // Get alcohol percentage if applicable
    let alcoholPercentage = 0;
    if (['Wine', 'Beer', 'Cocktail', 'Shot'].includes(drinkType) || 
         selectedDrink === "Alcohol") {
        alcoholPercentage = getSelectedAlcoholPercentage();
        if (isNaN(alcoholPercentage) || alcoholPercentage < 0) {
            alcoholPercentage = 0;
        }
    }
    
    // Prepare data for API call
    const drinkTimeInput = document.getElementById('drink-time');
    const drinkData = {
        drink_name: drinkType,
        amount: parseInt(amount),
        alcohol_percentage: parseFloat(alcoholPercentage),
        drink_time: drinkTimeInput ? drinkTimeInput.value : null
    };
    
    console.log("Sending data to API:", drinkData);
    
    // Show loading state
    const addBtn = document.querySelector('button[onclick="addDrink()"]');
    const addBtnOrigText = addBtn ? addBtn.textContent : '';
    if (addBtn) {
        addBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Adding...';
        addBtn.classList.add('btn-adding');
    }
    
    // Make API call to save drink log
    fetch('/api/add_drink', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
        body: JSON.stringify(drinkData)
    })
    .then(response => {
        if (!response.ok) {
            // Try to get the error message from the response
            return response.json().then(errorData => {
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }).catch(() => {
                throw new Error(`HTTP error! status: ${response.status}`);
            });
        }
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Response is not JSON');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            if (alcoholPercentage > 0) {
                console.log(`Added ${amount}ml of ${drinkType} (${alcoholPercentage}% alcohol)`);
            } else {
                console.log(`Added ${amount}ml of ${drinkType}`);
            }
            
            // Store last drink data for repeat
            lastDrinkData = {
                drink_name: drinkData.drink_name,
                amount: drinkData.amount,
                alcohol_percentage: drinkData.alcohol_percentage
            };
            sessionStorage.setItem('lastDrinkData', JSON.stringify(lastDrinkData));
            showRepeatBanner(lastDrinkData);
            
            // Show success toast
            let toastMsg = `✓ Added ${amount}ml of ${drinkType}`;
            if (alcoholPercentage > 0) {
                toastMsg += ` (${alcoholPercentage}% alc.)`;
            }
            showDrinkToast(toastMsg, 'success');
            
            // Restore button
            if (addBtn) {
                addBtn.textContent = addBtnOrigText;
                addBtn.classList.remove('btn-adding');
            }
            
            // Reset form elements
            const amountInput = document.getElementById('amount');
            if (amountInput) {
                amountInput.value = '';
            }
            
            // Reset selected amount variable
            selectedAmount = 100;
            drinkChosen = false;
            amountChosen = false;
            
            // Reset amount option highlights
            document.querySelectorAll('.amount-option').forEach(option => {
                option.querySelector('div').style.background = 'rgba(13, 110, 253, 0.2)';
                option.querySelector('div').style.color = 'white';
            });
            
            // Hide custom amount container if visible
            const customAmountContainer = document.getElementById('custom-amount-container');
            if (customAmountContainer) {
                customAmountContainer.style.display = 'none';
            }
            
            // Refresh the page to update consumption display
            setTimeout(() => {
                location.reload();
            }, 3000);
        } else {
            showDrinkToast('Error: ' + data.message, 'danger');
            if (addBtn) {
                addBtn.textContent = addBtnOrigText;
                addBtn.classList.remove('btn-adding');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (addBtn) {
            addBtn.textContent = addBtnOrigText;
            addBtn.classList.remove('btn-adding');
        }
        if (error.message.includes('401')) {
            showDrinkToast('Please log in to add drinks.', 'danger');
        } else if (error.message.includes('500')) {
            showDrinkToast('Server error: ' + error.message, 'danger');
        } else {
            showDrinkToast('Failed to save drink: ' + error.message, 'danger');
        }
    });
}

/**
 * Select a drink from the drink icon carousel
 */
function selectDrink(drinkType) {
    console.log("Selected drink: " + drinkType);
    selectedDrink = drinkType;
    drinkChosen = true;
    clearCarouselError('drink-carousel');

    // Highlight the selected icon
    const icons = document.querySelectorAll('.drink-icon');
    icons.forEach(icon => {
        icon.style.transform = 'scale(1)';
        icon.querySelector('img').style.boxShadow = 'none';
        icon.querySelector('img').style.border = 'none';
    });
    
    // Find the clicked element and highlight it
    const clickedIcon = event.currentTarget;
    clickedIcon.style.transform = 'scale(1.15)';
    clickedIcon.querySelector('img').style.boxShadow = '0 0 20px rgba(255, 255, 255, 0.9)';
    clickedIcon.querySelector('img').style.border = '3px solid #fff';
    
    // Check if it's an alcoholic drink
    const isAlcoholic = ['Wine', 'Beer', 'Cocktail', 'Shot'].includes(drinkType);
    const alcoholPercentageContainer = document.getElementById('alcohol-percentage-container');
    
    // Show/hide alcohol percentage selector
    if (alcoholPercentageContainer) {
        if (isAlcoholic) {
            alcoholPercentageContainer.style.display = 'flex';
            
            // Set default alcohol percentage based on drink type
            const alcoholPercentageSelect = document.getElementById('alcohol-percentage');
            if (alcoholPercentageSelect) {
                switch(drinkType) {
                    case 'Beer':
                        alcoholPercentageSelect.value = '5';
                        break;
                    case 'Wine':
                        alcoholPercentageSelect.value = '12';
                        break;
                    case 'Cocktail':
                        alcoholPercentageSelect.value = '14';
                        break;
                    case 'Shot':
                        alcoholPercentageSelect.value = '40';
                        break;
                }
            }
        } else {
            alcoholPercentageContainer.style.display = 'none';
            // Reset to 0 for non-alcoholic drinks
            const alcoholPercentageSelect = document.getElementById('alcohol-percentage');
            if (alcoholPercentageSelect) {
                alcoholPercentageSelect.value = '0';
            }
        }
    }
    
    // Set the corresponding radio button
    // let radioId;
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

/**
 * Handle selecting a predefined amount from the amount carousel
 */
function selectAmount(amount) {
    console.log(`Selected amount: ${amount}ml`);
    selectedAmount = amount;
    amountChosen = true;
    clearCarouselError('amount-carousel');
    resetAmountOptionStyles();
    updateCustomAmountOptionLabel();
    const activeOption = document.querySelector(`.amount-option[onclick="selectAmount(${amount})"]`);
    if (activeOption) {
        highlightAmountOption(activeOption, '#0d6efd', '0 0 15px rgba(13, 110, 253, 0.8)');
    }
    
    // Hide custom amount input if it's visible
    const customAmountContainer = document.getElementById('custom-amount-container');
    if (customAmountContainer) {
        customAmountContainer.style.display = 'none';
    }
    
    // Set the amount input field value
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        amountInput.value = amount;
    }
}

/**
 * Show the custom amount input field when "Other" is clicked
 */
function selectCustomAmount() {
    console.log("Selected custom amount");
    resetAmountOptionStyles();
    
    // Find the clicked element and highlight it
    const clickedOption = event.currentTarget;
    highlightAmountOption(clickedOption, '#dc3545', '0 0 12px rgba(255, 255, 255, 0.8)');
    
    // Show custom amount container
    const customAmountContainer = document.getElementById('custom-amount-container');
    if (customAmountContainer) {
        customAmountContainer.style.display = 'flex';
        
        // Focus the input field and set default value
        const customAmountInput = document.getElementById('custom-amount');
        if (customAmountInput) {
            if (!customAmountInput.value || customAmountInput.value == 0) {
                customAmountInput.value = 200;
            }
            customAmountInput.focus();
            customAmountInput.select();
        }
    }
}

/**
 * Confirm and set the custom amount when the OK button is clicked
 */
function changeCustomAmount(delta) {
    const input = document.getElementById('custom-amount');
    const current = parseInt(input.value) || 200;
    input.value = Math.max(10, current + delta);
}

/**
 * Confirm and set the custom amount when the OK button is clicked
 */
function confirmCustomAmount() {
    const customAmountInput = document.getElementById('custom-amount');
    const amount = parseInt(customAmountInput.value);
    if (!amount || isNaN(amount) || amount <= 0) {
        showCarouselError('amount-carousel', '⚠ Please enter a valid amount');
        return;
    }
    selectedAmount = amount;
    amountChosen = true;
    clearCarouselError('amount-carousel');
    updateCustomAmountOptionLabel(amount);
    const customOption = document.querySelector('.amount-option[onclick="selectCustomAmount()"]');
    if (customOption) {
        resetAmountOptionStyles();
        highlightAmountOption(customOption, '#dc3545', '0 0 15px rgba(220, 53, 69, 0.7)');
    }
    document.getElementById('custom-amount-container').style.display = 'none';
}

function resetAmountOptionStyles() {
    document.querySelectorAll('.amount-option').forEach(option => {
        const optionContent = option.querySelector('div');
        if (!optionContent) {
            return;
        }
        option.style.transform = 'scale(1)';
        optionContent.style.background = option.getAttribute('onclick') === 'selectCustomAmount()'
            ? 'rgba(220, 53, 69, 0.2)'
            : 'rgba(13, 110, 253, 0.2)';
        optionContent.style.color = 'white';
        optionContent.style.border = 'none';
        optionContent.style.transform = 'scale(1)';
        optionContent.style.boxShadow = 'none';
    });
}

function highlightAmountOption(option, backgroundColor, boxShadow) {
    const optionContent = option && option.querySelector('div');
    if (!option || !optionContent) {
        return;
    }
    option.style.transform = 'scale(1.05)';
    optionContent.style.background = backgroundColor;
    optionContent.style.color = 'white';
    optionContent.style.border = '2px solid #fff';
    optionContent.style.transform = 'scale(1.15)';
    optionContent.style.boxShadow = boxShadow;
}

function updateCustomAmountOptionLabel(amount) {
    const customOption = document.querySelector('.amount-option[onclick="selectCustomAmount()"] div');
    if (!customOption) {
        return;
    }
    customOption.textContent = amount ? `${amount}ml` : 'Other';
}

/**
 * Confirm and set a custom alcohol percentage
 */
function confirmCustomAlcohol() {
    const customAlcoholInput = document.getElementById('custom-alcohol');
    if (!customAlcoholInput || !customAlcoholInput.value) {
        alert("Please enter an alcohol percentage.");
        return;
    }
    
    const alcoholPercentage = parseFloat(customAlcoholInput.value);
    if (isNaN(alcoholPercentage) || alcoholPercentage < 0 || alcoholPercentage > 100) {
        alert("Please enter a valid alcohol percentage between 0 and 100.");
        return;
    }
    
    console.log(`Custom alcohol percentage set to ${alcoholPercentage}%`);
    
    // Hide the custom input container
    document.getElementById('custom-alcohol-container').style.display = 'none';
    
    // Store the custom value for retrieval when adding the drink
    document.getElementById('alcohol-percentage').setAttribute('data-custom-value', alcoholPercentage);
}

/**
 * Get the current alcohol percentage (either from dropdown or custom input)
 */
function getSelectedAlcoholPercentage() {
    const alcoholPercentageSelect = document.getElementById('alcohol-percentage');
    if (!alcoholPercentageSelect) return 0;
    
    if (alcoholPercentageSelect.value === 'custom') {
        return parseFloat(alcoholPercentageSelect.getAttribute('data-custom-value') || 0);
    } else {
        return parseFloat(alcoholPercentageSelect.value);
    }
}

/**
 * Show the repeat drink banner with a summary of the last added drink
 */
function showRepeatBanner(drinkData) {
    const banner = document.getElementById('repeat-drink-banner');
    const btnLabel = document.getElementById('repeat-drink-btn');
    if (!banner || !btnLabel) return;

    btnLabel.textContent = `Add other ${drinkData.drink_name} ${drinkData.amount}ml`;
    banner.style.display = 'block';
}

/**
 * Repeat the last added drink with the current time
 */
function repeatLastDrink() {
    if (!lastDrinkData) return;

    const now = new Date();
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');

    const drinkData = {
        drink_name: lastDrinkData.drink_name,
        amount: lastDrinkData.amount,
        alcohol_percentage: lastDrinkData.alcohol_percentage,
        drink_time: hh + ':' + mm
    };

    // Show loading state on repeat button
    const repeatBtn = document.getElementById('repeat-drink-btn');
    const repeatBtnOrigText = repeatBtn ? repeatBtn.textContent : '';
    if (repeatBtn) {
        repeatBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Adding...';
        repeatBtn.classList.add('btn-adding');
    }

    console.log('Repeating drink:', drinkData);

    fetch('/api/add_drink', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify(drinkData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message || `HTTP error! status: ${response.status}`);
            }).catch(() => {
                throw new Error(`HTTP error! status: ${response.status}`);
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            let msg = `✓ Added ${lastDrinkData.amount}ml of ${lastDrinkData.drink_name}`;
            if (lastDrinkData.alcohol_percentage > 0) {
                msg += ` (${lastDrinkData.alcohol_percentage}% alc.)`;
            }
            showDrinkToast(msg, 'success');
            if (repeatBtn) {
                repeatBtn.textContent = repeatBtnOrigText;
                repeatBtn.classList.remove('btn-adding');
            }
            showRepeatBanner(lastDrinkData);
            setTimeout(() => { location.reload(); }, 3000);
        } else {
            showDrinkToast('Error: ' + data.message, 'danger');
            if (repeatBtn) {
                repeatBtn.textContent = repeatBtnOrigText;
                repeatBtn.classList.remove('btn-adding');
            }
        }
    })
    .catch(error => {
        console.error('Error repeating drink:', error);
        showDrinkToast('Failed to repeat drink: ' + error.message, 'danger');
        if (repeatBtn) {
            repeatBtn.textContent = repeatBtnOrigText;
            repeatBtn.classList.remove('btn-adding');
        }
    });
}

/**
 * Show a Bootstrap toast notification
 */
function showDrinkToast(message, type) {
    const toastEl = document.getElementById('drink-toast');
    const toastBody = document.getElementById('drink-toast-body');
    if (!toastEl || !toastBody) return;

    toastEl.className = 'toast align-items-center border-0 text-bg-' + type;
    toastBody.textContent = message;

    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

