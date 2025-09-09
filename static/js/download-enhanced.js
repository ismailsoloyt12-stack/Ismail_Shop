// Enhanced Download System for Premium Apps
function downloadApp(appId) {
    // Show the professional download popup
    const popup = document.getElementById('downloadPopup');
    popup.style.display = 'block';
    document.body.style.overflow = 'hidden';
    
    // Reset all steps and progress
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach(step => {
        step.classList.remove('active', 'completed');
        const statusEl = step.querySelector('.step-status');
        if (statusEl) statusEl.textContent = '';
    });
    
    // Reset progress bar
    const progressFill = document.getElementById('progressFill');
    const progressPercentage = document.getElementById('progressPercentage');
    if (progressFill) progressFill.style.width = '0%';
    if (progressPercentage) progressPercentage.textContent = '0%';
    
    // Function to update progress
    function updateProgress(percent) {
        if (progressFill) progressFill.style.width = percent + '%';
        if (progressPercentage) progressPercentage.textContent = percent + '%';
    }
    
    // Function to animate steps
    function animateStep(stepNumber, statusText, callback) {
        const step = document.getElementById(`step${stepNumber}`);
        const statusEl = step.querySelector('.step-status');
        
        step.classList.add('active');
        if (statusEl && statusText) {
            statusEl.textContent = statusText;
        }
        
        // Update progress based on step
        const progressPercent = stepNumber * 25;
        updateProgress(progressPercent);
        
        setTimeout(() => {
            step.classList.add('completed');
            if (callback) callback();
        }, 800);
    }
    
    // Start the animation sequence
    setTimeout(() => {
        // Step 1: Connecting to server
        animateStep(1, 'Connected', () => {
            // Step 2: Locating file
            animateStep(2, 'File found', () => {
                // Step 3: Verifying integrity
                animateStep(3, 'Verified', () => {
                    // Step 4: Initiating download
                    animateStep(4, 'Processing...', () => {
                        // Make the actual download request
                        fetch(`/api/download/${appId}`, {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'}
                        })
                        .then(response => response.json())
                        .then(data => {
                            if(data.success) {
                                // Update download counter
                                const downloadStats = document.querySelectorAll('.stat-value');
                                downloadStats.forEach(stat => {
                                    if (stat.nextElementSibling && stat.nextElementSibling.textContent.includes('Downloads')) {
                                        stat.textContent = data.downloads;
                                    }
                                });
                                
                                // Complete progress
                                updateProgress(100);
                                
                                // If there's a real file, trigger proper download
                                if (data.has_file && data.file_url) {
                                    // For Premium apps, open in new tab/window for better compatibility
                                    window.open(data.file_url, '_blank');
                                    
                                    // Update status
                                    const step4Status = document.querySelector('#step4 .step-status');
                                    if (step4Status) {
                                        step4Status.textContent = 'Download started';
                                        step4Status.style.color = '#06ffa5';
                                    }
                                    
                                    // Show close button after a short delay
                                    setTimeout(() => {
                                        const closeBtn = document.querySelector('.close-popup-btn');
                                        if (closeBtn) closeBtn.style.display = 'block';
                                    }, 1000);
                                } else {
                                    // No real file, just show success
                                    const step4Status = document.querySelector('#step4 .step-status');
                                    if (step4Status) {
                                        step4Status.textContent = 'Ready for download';
                                        step4Status.style.color = '#06ffa5';
                                    }
                                    
                                    const closeBtn = document.querySelector('.close-popup-btn');
                                    if (closeBtn) closeBtn.style.display = 'block';
                                }
                            } else {
                                // Error occurred
                                updateProgress(100);
                                const step4Status = document.querySelector('#step4 .step-status');
                                if (step4Status) {
                                    step4Status.textContent = 'Error: Could not start download';
                                    step4Status.style.color = '#f72585';
                                }
                                
                                const closeBtn = document.querySelector('.close-popup-btn');
                                if (closeBtn) closeBtn.style.display = 'block';
                            }
                        })
                        .catch(error => {
                            console.error('Download error:', error);
                            updateProgress(100);
                            const step4Status = document.querySelector('#step4 .step-status');
                            if (step4Status) {
                                step4Status.textContent = 'Network error';
                                step4Status.style.color = '#f72585';
                            }
                            
                            const closeBtn = document.querySelector('.close-popup-btn');
                            if (closeBtn) closeBtn.style.display = 'block';
                        });
                    });
                });
            });
        });
    }, 300);
}

function closeDownloadPopup() {
    const popup = document.getElementById('downloadPopup');
    popup.style.display = 'none';
    document.body.style.overflow = 'auto';
    
    // Reset the close button
    const closeBtn = document.querySelector('.close-popup-btn');
    if (closeBtn) closeBtn.style.display = 'none';
    
    // Reset all step statuses
    const stepStatuses = document.querySelectorAll('.step-status');
    stepStatuses.forEach(status => {
        status.textContent = '';
        status.style.color = '';
    });
}
