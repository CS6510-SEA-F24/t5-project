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
document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM loaded");
    const svg = document.querySelector('.arrows');
    console.log("SVG element:", svg);

    const jobs = document.querySelectorAll('.job');
    jobs.forEach(job => {
        const needs = job.getAttribute('data-needs');
        console.log(`Job ${job.id} needs:`, needs);
        if (needs) {
            needs.split(',').forEach(need => {
                const fromJob = document.getElementById(`job_${need.trim()}`);
                console.log(`From job element:`, fromJob);
                if (fromJob) {
                    console.log(`Drawing arrow from ${fromJob.id} to ${job.id}`);
                    drawArrow(fromJob, job);
                }
            });
        }
    });

    function drawArrow(fromElement, toElement) {
        const svg = document.querySelector('.arrows');
        const svgRect = svg.getBoundingClientRect();
        const fromRect = fromElement.getBoundingClientRect();
        const toRect = toElement.getBoundingClientRect();

        // Calculate coordinates relative to the SVG
        const startX = fromRect.right - svgRect.left;
        const startY = fromRect.top + (fromRect.height / 2) - svgRect.top;
        const endX = toRect.left - svgRect.left;
        const endY = toRect.top + (toRect.height / 2) - svgRect.top;

        // Create a path element to represent the arrow
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        const midX = (startX + endX) / 2;
        // Define the path using cubic Bezier curve
        const d = `
        M ${startX},${startY}
        C ${midX},${startY}
          ${midX},${endY}
          ${endX},${endY}
    `;
        // Set path attributes like stroke color, width, and arrowhead marker
        path.setAttribute("d", d);
        path.setAttribute("stroke", "#000");
        path.setAttribute("stroke-width", "2");
        path.setAttribute("marker-end", "url(#arrowhead)");
        path.setAttribute("fill", "none");
        // Append the path to the SVG element
        svg.appendChild(path);
    }
});