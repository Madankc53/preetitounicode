// INR to NPR Converter - External JS (deferred)
(function() {
    const RATE = 1.60;
    const REVERSE = 1 / RATE; // 0.625

    let isUpdating = false;

    function showToast(msg) {
        const toast = document.getElementById('toastMessage');
        if (!toast) return;
        toast.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 1800);
    }

    function updateFromINR(inrInput, nprInput, nprDisplay) {
        if (isUpdating) return;
        isUpdating = true;
        let inrVal = parseFloat(inrInput.value);
        if (isNaN(inrVal)) inrVal = 0;
        inrVal = Math.max(0, inrVal);
        const nprVal = inrVal * RATE;
        nprDisplay.textContent = nprVal.toFixed(2) + ' NPR';
        if (document.activeElement !== nprInput) {
            nprInput.value = nprVal.toFixed(2);
        }
        isUpdating = false;
    }

    function updateFromNPR(inrInput, nprInput, inrDisplay) {
        if (isUpdating) return;
        isUpdating = true;
        let nprVal = parseFloat(nprInput.value);
        if (isNaN(nprVal)) nprVal = 0;
        nprVal = Math.max(0, nprVal);
        const inrVal = nprVal * REVERSE;
        inrDisplay.textContent = inrVal.toFixed(2) + ' INR';
        if (document.activeElement !== inrInput) {
            inrInput.value = inrVal.toFixed(2);
        }
        isUpdating = false;
    }

    // Expanded table with 25,000 and 50,000 INR
    function buildTable() {
        const tbody = document.getElementById('conversionTableBody');
        if (!tbody) return;
        const amounts = [1, 5, 10, 50, 100, 500, 1000, 5000, 10000, 25000, 50000];
        tbody.innerHTML = '';
        for (let inr of amounts) {
            const npr = (inr * RATE).toFixed(2);
            const row = `<tr><td>${inr.toLocaleString()} INR</td><td>${npr} NPR</td></tr>`;
            tbody.insertAdjacentHTML('beforeend', row);
        }
    }

    function setupCopy(buttonId, textGetter) {
        const btn = document.getElementById(buttonId);
        if (!btn) return;
        btn.addEventListener('click', async () => {
            const text = textGetter();
            try {
                await navigator.clipboard.writeText(text);
                showToast(`✅ Copied: ${text}`);
            } catch {
                showToast(`⚠️ Press Ctrl+C to copy`);
            }
        });
    }

    // Corrected swap logic: exchange the two input values, preserve focus
    function swapValues(inrInput, nprInput, nprDisplay, inrDisplay) {
        if (isUpdating) return;
        isUpdating = true;
        const tempINR = inrInput.value;
        const tempNPR = nprInput.value;
        inrInput.value = tempNPR;
        nprInput.value = tempINR;
        updateFromINR(inrInput, nprInput, nprDisplay);
        updateFromNPR(inrInput, nprInput, inrDisplay);
        isUpdating = false;
    }

    function resetValues(inrInput, nprInput, nprDisplay, inrDisplay) {
        if (isUpdating) return;
        isUpdating = true;
        inrInput.value = '1';
        nprInput.value = '1.60';
        updateFromINR(inrInput, nprInput, nprDisplay);
        updateFromNPR(inrInput, nprInput, inrDisplay);
        isUpdating = false;
        showToast('↻ Reset to 1 INR = 1.60 NPR');
    }

    function initializeConverter() {
        const inrInput = document.getElementById('inrInput');
        const nprInput = document.getElementById('nprInput');
        const nprDisplay = document.getElementById('nprDisplay');
        const inrDisplay = document.getElementById('inrDisplay');

        if (!inrInput || !nprInput) return;

        // Event listeners
        inrInput.addEventListener('input', () => updateFromINR(inrInput, nprInput, nprDisplay));
        nprInput.addEventListener('input', () => updateFromNPR(inrInput, nprInput, inrDisplay));

        // Buttons
        const swapBtn = document.getElementById('swapButton');
        if (swapBtn) swapBtn.addEventListener('click', () => swapValues(inrInput, nprInput, nprDisplay, inrDisplay));

        const resetBtn = document.getElementById('resetButton');
        if (resetBtn) resetBtn.addEventListener('click', () => resetValues(inrInput, nprInput, nprDisplay, inrDisplay));

        // Copy buttons
        setupCopy('copyNprBtn', () => nprDisplay.textContent);
        setupCopy('copyInrBtn', () => inrDisplay.textContent);

        // Build table
        buildTable();

        // Initial updates
        updateFromINR(inrInput, nprInput, nprDisplay);
        updateFromNPR(inrInput, nprInput, inrDisplay);
    }

    // Only use DOMContentLoaded if document is not already loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeConverter);
    } else {
        initializeConverter();
    }
})();
