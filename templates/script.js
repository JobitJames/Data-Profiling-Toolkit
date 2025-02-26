// In your existing script section, replace the form submit handler with:
document.querySelector('.upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const submitBtn = e.target.querySelector('button');
    
    try {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Analyzing...';
        
        const response = await fetch('/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Unknown error');
        }
        
        const data = await response.json();
        showSuccess();
        
        // Trigger download after showing success
        setTimeout(() => {
            window.location.href = data.downloadUrl;
        }, 2000);
        
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Analyze Dataset';
    }
});

// Modify showSuccess function to auto-close after download
function showSuccess() {
    const overlay = document.querySelector('.success-overlay');
    const progress = document.querySelector('.progress');
    overlay.innerHTML = "<p>Report generated successfully! Your download will start soon.</p>";
    overlay.style.display = 'flex';
    setTimeout(() => {
        progress.style.width = '100%';
    }, 100);

    // Keep overlay visible until download completes
    // Reset when user comes back
    window.addEventListener('focus', () => {
        overlay.style.display = 'none';
        progress.style.width = '0';
    }, { once: true });
}
