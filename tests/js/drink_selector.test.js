/**
 * Unit tests for static/js/drink_selector.js
 * Tests: addDrink, selectAmount, confirmCustomAmount,
 *        confirmCustomAlcohol, getSelectedAlcoholPercentage
 *
 * NOTE: drink_selector.js uses module-scope `let` variables (selectedDrink,
 * selectedAmount) that are only accessible via their public functions.
 * Tests manipulate state through selectAmount() and the DOM, not direct
 * assignment.
 */

const fs = require('fs');
const path = require('path');

const scriptPath = path.resolve(__dirname, '../../static/js/drink_selector.js');
const scriptContent = fs.readFileSync(scriptPath, 'utf-8');

// Load the script ONCE into the global (jsdom) context so function
// declarations become globally accessible in tests.
(0, eval)(scriptContent);

// ─── Build minimal DOM ────────────────────────────────────────────────────────

function buildDOM() {
    document.body.innerHTML = `
        <form id="drink-form">
            <input type="radio" name="drink" id="water" value="Water">
            <input type="radio" name="drink" id="coffee" value="Coffee">
            <input type="radio" name="drink" id="alcohol" value="Alcohol">
            <input type="radio" name="drink" id="other" value="Other">

            <select id="other-drink-select" style="display: none;">
                <option value="Juice">Juice</option>
                <option value="Soda">Soda</option>
            </select>

            <div id="alcohol-percentage-container" style="display: none;">
                <select id="alcohol-percentage">
                    <option value="0">0%</option>
                    <option value="5">5%</option>
                    <option value="12">12%</option>
                    <option value="14">14%</option>
                    <option value="40">40%</option>
                    <option value="custom">Custom</option>
                </select>
            </div>

            <div id="custom-alcohol-container" style="display: none;">
                <input type="number" id="custom-alcohol">
            </div>

            <div class="amount-option" onclick="selectAmount(100)"><div>100ml</div></div>
            <div class="amount-option" onclick="selectAmount(250)"><div>250ml</div></div>
            <div class="amount-option" onclick="selectAmount(500)"><div>500ml</div></div>

            <div id="custom-amount-container" style="display: none;">
                <input type="number" id="custom-amount">
            </div>

            <input type="number" id="amount" value="250">
        </form>
    `;
}

beforeEach(() => {
    buildDOM();
    global.alert   = jest.fn();
    global.confirm = jest.fn(() => true);
    global.fetch   = jest.fn();
    global.location = { reload: jest.fn() };
    jest.clearAllMocks();
    // Reset selectedAmount to default via selectAmount()
    selectAmount(100);
});

// ─── getSelectedAlcoholPercentage ─────────────────────────────────────────────

describe('getSelectedAlcoholPercentage', () => {
    test('returns numeric value from select', () => {
        document.getElementById('alcohol-percentage').value = '12';
        expect(getSelectedAlcoholPercentage()).toBe(12);
    });

    test('returns 0 when select value is 0', () => {
        document.getElementById('alcohol-percentage').value = '0';
        expect(getSelectedAlcoholPercentage()).toBe(0);
    });

    test('returns custom value when select is set to "custom"', () => {
        const sel = document.getElementById('alcohol-percentage');
        const customOpt = document.createElement('option');
        customOpt.value = 'custom';
        sel.appendChild(customOpt);
        sel.value = 'custom';
        sel.setAttribute('data-custom-value', '22');
        expect(getSelectedAlcoholPercentage()).toBe(22);
    });

    test('returns 0 when alcohol-percentage element is absent', () => {
        document.getElementById('alcohol-percentage').remove();
        expect(getSelectedAlcoholPercentage()).toBe(0);
    });
});

// ─── selectAmount ─────────────────────────────────────────────────────────────

describe('selectAmount', () => {
    test('sets the amount input value', () => {
        selectAmount(500);
        expect(document.getElementById('amount').value).toBe('500');
    });

    test('hides the custom amount container', () => {
        document.getElementById('custom-amount-container').style.display = 'flex';
        selectAmount(250);
        expect(document.getElementById('custom-amount-container').style.display).toBe('none');
    });

    test('does not throw when amount-option elements are absent', () => {
        document.querySelectorAll('.amount-option').forEach(el => el.remove());
        expect(() => selectAmount(100)).not.toThrow();
    });
});

// ─── confirmCustomAmount ──────────────────────────────────────────────────────

describe('confirmCustomAmount', () => {
    test('sets amount input and hides container for valid input', () => {
        document.getElementById('custom-amount').value = '350';
        document.getElementById('custom-amount-container').style.display = 'flex';
        confirmCustomAmount();
        expect(document.getElementById('custom-amount-container').style.display).toBe('none');
        expect(document.getElementById('amount').value).toBe('350');
    });

    test('alerts when amount is empty', () => {
        document.getElementById('custom-amount').value = '';
        confirmCustomAmount();
        expect(global.alert).toHaveBeenCalledWith('Please enter a valid amount.');
    });

    test('alerts when amount is non-numeric', () => {
        document.getElementById('custom-amount').value = 'abc';
        confirmCustomAmount();
        expect(global.alert).toHaveBeenCalledWith('Please enter a valid amount.');
    });

    test('alerts when amount is zero', () => {
        document.getElementById('custom-amount').value = '0';
        confirmCustomAmount();
        expect(global.alert).toHaveBeenCalledWith('Please enter a valid amount.');
    });

    test('alerts when amount is negative', () => {
        document.getElementById('custom-amount').value = '-100';
        confirmCustomAmount();
        expect(global.alert).toHaveBeenCalledWith('Please enter a valid amount.');
    });
});

// ─── confirmCustomAlcohol ─────────────────────────────────────────────────────

describe('confirmCustomAlcohol', () => {
    test('hides container and stores value for valid input', () => {
        document.getElementById('custom-alcohol').value = '15';
        document.getElementById('custom-alcohol-container').style.display = 'flex';
        confirmCustomAlcohol();
        expect(document.getElementById('custom-alcohol-container').style.display).toBe('none');
        expect(document.getElementById('alcohol-percentage').getAttribute('data-custom-value')).toBe('15');
        expect(global.alert).not.toHaveBeenCalled();
    });

    test('alerts when input is empty', () => {
        document.getElementById('custom-alcohol').value = '';
        confirmCustomAlcohol();
        expect(global.alert).toHaveBeenCalledWith('Please enter an alcohol percentage.');
    });

    test('alerts when percentage is above 100', () => {
        document.getElementById('custom-alcohol').value = '150';
        confirmCustomAlcohol();
        expect(global.alert).toHaveBeenCalledWith(
            'Please enter a valid alcohol percentage between 0 and 100.'
        );
    });

    test('alerts when percentage is negative', () => {
        document.getElementById('custom-alcohol').value = '-5';
        confirmCustomAlcohol();
        expect(global.alert).toHaveBeenCalledWith(
            'Please enter a valid alcohol percentage between 0 and 100.'
        );
    });

    test('accepts 0% alcohol', () => {
        document.getElementById('custom-alcohol').value = '0';
        confirmCustomAlcohol();
        expect(global.alert).not.toHaveBeenCalled();
    });

    test('accepts 100% alcohol', () => {
        document.getElementById('custom-alcohol').value = '100';
        confirmCustomAlcohol();
        expect(global.alert).not.toHaveBeenCalled();
    });
});

// ─── addDrink ─────────────────────────────────────────────────────────────────

describe('addDrink – validation', () => {
    // default selectedDrink = 'Water', selectedAmount = 100 (set by beforeEach)

    test('alerts when amount is zero (via selectAmount)', () => {
        selectAmount(0);
        addDrink();
        expect(global.alert).toHaveBeenCalledWith('Please enter a valid amount.');
    });

    test('calls fetch with correct payload when input is valid', () => {
        global.fetch = jest.fn(() => Promise.resolve({
            ok: true,
            headers: { get: () => 'application/json' },
            json: () => Promise.resolve({ success: true })
        }));

        selectAmount(250);
        addDrink();

        expect(global.fetch).toHaveBeenCalledWith(
            '/api/add_drink',
            expect.objectContaining({
                method: 'POST',
                body: expect.stringContaining('"drink_name":"Water"')
            })
        );
    });

    test('sends amount as integer in fetch payload', () => {
        global.fetch = jest.fn(() => Promise.resolve({
            ok: true,
            headers: { get: () => 'application/json' },
            json: () => Promise.resolve({ success: true })
        }));

        selectAmount(500);
        addDrink();

        expect(global.fetch).toHaveBeenCalledWith(
            '/api/add_drink',
            expect.objectContaining({
                body: expect.stringContaining('"amount":500')
            })
        );
    });

    test('sends credentials same-origin in fetch call', () => {
        global.fetch = jest.fn(() => Promise.resolve({
            ok: true,
            headers: { get: () => 'application/json' },
            json: () => Promise.resolve({ success: true })
        }));

        selectAmount(250);
        addDrink();

        expect(global.fetch).toHaveBeenCalledWith(
            '/api/add_drink',
            expect.objectContaining({ credentials: 'same-origin' })
        );
    });
});
