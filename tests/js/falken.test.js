/**
 * Unit tests for static/js/falken.js
 * Tests: toggleVisibility, activeVisibility
 */

const fs = require('fs');
const path = require('path');

// Load the script under test into the global (jsdom) context so that
// function declarations become globally accessible in tests.
const scriptPath = path.resolve(__dirname, '../../static/js/falken.js');
const scriptContent = fs.readFileSync(scriptPath, 'utf-8');
(0, eval)(scriptContent);

beforeEach(() => {
    // Reset DOM before each test
    document.body.innerHTML = '';
});

describe('toggleVisibility', () => {
    test('hides a visible element', () => {
        document.body.innerHTML = '<div id="box" style="visibility: visible;"></div>';
        toggleVisibility('box');
        expect(document.getElementById('box').style.visibility).toBe('hidden');
    });

    test('shows a hidden element', () => {
        document.body.innerHTML = '<div id="box" style="visibility: hidden;"></div>';
        toggleVisibility('box');
        expect(document.getElementById('box').style.visibility).toBe('visible');
    });

    test('toggles back to hidden after two calls', () => {
        document.body.innerHTML = '<div id="box" style="visibility: visible;"></div>';
        toggleVisibility('box');
        toggleVisibility('box');
        expect(document.getElementById('box').style.visibility).toBe('visible');
    });

    test('shows an element with no initial visibility style', () => {
        document.body.innerHTML = '<div id="box"></div>';
        toggleVisibility('box');
        // Element without explicit visibility is treated as not "visible", so it becomes "visible"
        expect(document.getElementById('box').style.visibility).toBe('visible');
    });
});

// ─── activeVisibility ────────────────────────────────────────────────────────

describe('activeVisibility', () => {
    test('shows target element when checkbox is checked', () => {
        document.body.innerHTML = `
            <input type="checkbox" id="drinks" checked>
            <div id="drinks_icon" style="visibility: hidden;"></div>
        `;
        activeVisibility('drinks', 'drinks_icon');
        expect(document.getElementById('drinks_icon').style.visibility).toBe('visible');
    });

    test('hides target element when checkbox is unchecked', () => {
        document.body.innerHTML = `
            <input type="checkbox" id="drinks">
            <div id="drinks_icon" style="visibility: visible;"></div>
        `;
        activeVisibility('drinks', 'drinks_icon');
        expect(document.getElementById('drinks_icon').style.visibility).toBe('hidden');
    });

    test('does nothing when status element does not exist', () => {
        document.body.innerHTML = '<div id="drinks_icon" style="visibility: visible;"></div>';
        // Should not throw
        expect(() => activeVisibility('nonexistent', 'drinks_icon')).not.toThrow();
        // Element stays unchanged
        expect(document.getElementById('drinks_icon').style.visibility).toBe('visible');
    });

    test('does nothing when target element does not exist', () => {
        document.body.innerHTML = '<input type="checkbox" id="drinks" checked>';
        expect(() => activeVisibility('drinks', 'nonexistent')).not.toThrow();
    });

    test('does nothing when both elements are missing', () => {
        document.body.innerHTML = '';
        expect(() => activeVisibility('missing_status', 'missing_target')).not.toThrow();
    });
});
