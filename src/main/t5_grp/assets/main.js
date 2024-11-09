/*
This module is responsible for dynamically drawing arrows between job elements in a web application's pipeline visualization. It waits for the DOM content to be fully loaded before executing the main functionality.

Functions:
    drawArrow(fromElement, toElement):
Draws an arrow from `fromElement` to `toElement` within the SVG context.

    Event Listeners:
    DOMContentLoaded:
        - Logs when the DOM is fully loaded.
- Selects the SVG element meant to contain the arrows.
- Iterates through each job element, checking for dependencies specified in the 'data-needs' attribute.
- Draws arrows between dependent job elements.
*/
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded");
    
    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.querySelector('.arrows');
    console.log("SVG element:", svg); // Check if SVG element is found
    if (!svg) {
        console.error("SVG element not found");
        return;
    }

    function updateSvgSize() {
        const container = document.querySelector('.stages-container');
        if (!container) {
            console.error("Container not found");
            return;
        }
        const rect = container.getBoundingClientRect();
        svg.setAttribute('width', rect.width);
        svg.setAttribute('height', rect.height);
    }
    
    updateSvgSize();
    window.addEventListener('resize', updateSvgSize);

    function drawArrow(fromElement, toElement) {
        console.log("Drawing arrow from:", fromElement);
        console.log("Drawing arrow to:", toElement);
        const fromRect = fromElement.getBoundingClientRect();
        const toRect = toElement.getBoundingClientRect();
        const svgRect = svg.getBoundingClientRect();

        // Check if the elements are in the same stage
        const fromStage = fromElement.closest('.stage');
        const toStage = toElement.closest('.stage');
        const inSameStage = fromStage === toStage;

        let fromX, fromY, toX, toY;

        if (inSameStage) {
            // Arrow within the same stage
            // Starting point: bottom center of the above job
            fromX = fromRect.left - svgRect.left + fromRect.width / 2;
            fromY = fromRect.top - svgRect.top;

            // Ending point: bottom center of the above job
            toX = toRect.left - svgRect.left + toRect.width / 2;
            toY = toRect.bottom - svgRect.top;

            // Create a curved path, using shorter control point distances
            const path = document.createElementNS(svgNS, 'path');
            const distance = Math.abs(toY - fromY);  // Use absolute value to ensure positive distance
            const controlPoint1X = fromX;
            const controlPoint1Y = fromY - distance * 0.1; // Curve upwards
            const controlPoint2X = toX;
            const controlPoint2Y = toY + distance * 0.1; // Curve upwards

            path.setAttribute('d', `M ${fromX},${fromY} C ${controlPoint1X},${controlPoint1Y} ${controlPoint2X},${controlPoint2Y} ${toX},${toY}`);
            path.setAttribute('marker-end', 'url(#arrowhead)');
            path.setAttribute('class', 'pipeline-arrow');
            svg.appendChild(path);
        } else {
            fromX = fromRect.right - svgRect.left;
            fromY = fromRect.top + (fromRect.height / 2) - svgRect.top;
            toX = toRect.left - svgRect.left;
            toY = toRect.top + (toRect.height / 2) - svgRect.top;

            const path = document.createElementNS(svgNS, 'path');
            const distance = toX - fromX;
            path.setAttribute('d', `M ${fromX},${fromY} C ${fromX + distance * 2},${fromY} ${toX - distance * 2},${toY} ${toX},${toY}`);
            path.setAttribute('marker-end', 'url(#arrowhead)');
            path.setAttribute('class', 'pipeline-arrow');

            svg.appendChild(path);
        }
    }

    const jobs = document.querySelectorAll('.job');
    jobs.forEach(job => {
        const needs = job.getAttribute('data-needs');
        if (needs && needs.trim() !== '') {
            console.log(`Processing job with needs: ${needs}`);
            const needsList = needs.split(',');
            needsList.forEach(need => {
                const fromJob = document.getElementById(`job_${need.trim()}`);
                if (fromJob) {
                    console.log(`Drawing arrow from ${need.trim()} to ${job.id}`);
                    drawArrow(fromJob, job);
                }
            });
        }
    });
});