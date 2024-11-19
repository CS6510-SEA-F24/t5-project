/*
Pipeline Visualization Arrow Generator
====================================

This module manages the dynamic generation and rendering of dependency arrows in a pipeline visualization interface.
It creates SVG-based arrows connecting job elements based on their dependencies, with different styles for
same-stage and cross-stage connections.

Key Features:
- Dynamic arrow path generation
- Automatic routing around intermediate jobs
- Different arrow styles for same-stage and cross-stage dependencies
- Responsive arrow updates on window resize
- Support for multiple dependencies per job

Main Components:
1. Arrow Markers: Defines arrowhead styles for different directions
2. Path Generation: Creates smooth  for arrow paths
3. Job Detection: Identifies intermediate jobs for path routing
4. Event Handling: Manages window resize and DOM updates
*/
document.addEventListener('DOMContentLoaded', function() {
    const stages = document.querySelectorAll('.stage-wrapper');
    document.documentElement.style.setProperty('--stage-count', String(stages.length));

    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.querySelector('.arrows');

    if (!svg) {
        console.error("SVG element not found");
        return;
    }

    /**
     * Creates and configures SVG arrow markers for the pipeline visualization
     * Defines two types of markers:
     * 1. Downward-pointing arrow for cross-stage connections
     * 2. Upward-pointing arrow for same-stage connections
     */
    function createArrowMarkers() {
        let defs = document.querySelector('defs');
        if (!defs) {
            defs = document.createElementNS(svgNS, 'defs');
            svg.appendChild(defs);
        }

        // Clear existing markers
        defs.innerHTML = '';

        // Configure downward-pointing arrow (for cross-stage connections)
        const downArrow = document.createElementNS(svgNS, 'marker');
        downArrow.setAttribute('id', 'arrowhead-down');
        downArrow.setAttribute('markerWidth', '10');
        downArrow.setAttribute('markerHeight', '8');
        downArrow.setAttribute('refX', '9');
        downArrow.setAttribute('refY', '4');
        downArrow.setAttribute('orient', 'auto');

        const downPolygon = document.createElementNS(svgNS, 'polygon');
        downPolygon.setAttribute('points', '0 0, 10 4, 0 8');
        downPolygon.setAttribute('fill', 'var(--arrow-fill)');
        downArrow.appendChild(downPolygon);

        // Configure upward-pointing arrow (for same-stage connections)）
        const upArrow = document.createElementNS(svgNS, 'marker');
        upArrow.setAttribute('id', 'arrowhead-up');
        upArrow.setAttribute('markerWidth', '10');
        upArrow.setAttribute('markerHeight', '8');
        upArrow.setAttribute('refX', '9');
        upArrow.setAttribute('refY', '4');
        upArrow.setAttribute('orient', 'auto-start-reverse');

        const upPolygon = document.createElementNS(svgNS, 'polygon');
        upPolygon.setAttribute('points', '0 0, 10 4, 0 8');
        upPolygon.setAttribute('fill', 'var(--arrow-fill)');
        upArrow.appendChild(upPolygon);

        defs.appendChild(downArrow);
        defs.appendChild(upArrow);
    }

    /**
     * Calculates the start and end points for an arrow between two job elements
     * @param {DOMRect} fromRect - Bounding rectangle of source job element
     * @param {DOMRect} toRect - Bounding rectangle of target job element
     * @param {DOMRect} svgRect - Bounding rectangle of SVG container
     * @param {boolean} inSameStage - Whether the jobs are in the same stage
     * @returns {number[]} Array of [fromX, fromY, toX, toY] coordinates
     */
    function calculateArrowPoints(fromRect, toRect, svgRect, inSameStage) {
        if (inSameStage) {
            return [
                fromRect.left - svgRect.left + fromRect.width / 2,
                fromRect.top - svgRect.top,
                toRect.left - svgRect.left + toRect.width / 2,
                toRect.bottom - svgRect.top
            ];
        }
        return [
            fromRect.right - svgRect.left,
            fromRect.top + (fromRect.height / 2) - svgRect.top,
            toRect.left - svgRect.left,
            toRect.top + (toRect.height / 2) - svgRect.top
        ];
    }

    /**
     * Creates an SVG path for an arrow between two jobs
     * @param {number} fromX - Starting X coordinate
     * @param {number} fromY - Starting Y coordinate
     * @param {number} toX - Ending X coordinate
     * @param {number} toY - Ending Y coordinate
     * @param {number} fromStage - Source stage index
     * @param {number} toStage - Target stage index
     * @param {number} dependencyIndex - Index of current dependency
     * @param {number} totalDependencies - Total number of dependencies
     */
    function createArrowPath(fromX, fromY, toX, toY, fromStage, toStage, dependencyIndex, totalDependencies) {
        const path = document.createElementNS(svgNS, 'path');
        const stageDistance = Math.abs(toStage - fromStage);
        const endPointOffset = -24;
        const actualToX = toX + endPointOffset;
        path.setAttribute('marker-end',
            stageDistance === 0 ? 'url(#arrowhead-up)' : 'url(#arrowhead-down)'
        );

        let pathData;
        const horizontalGap = actualToX - fromX;
        const verticalGap = toY - fromY;

        // Handle same-stage arrows
        if (stageDistance === 0) {
            const curveHeight = Math.min(Math.abs(verticalGap) * 0.3, 40);
            const horizontalOffset = 15 * (dependencyIndex - (totalDependencies - 1) / 2);
            pathData = `M${fromX},${fromY} 
                   C${fromX + horizontalOffset},${fromY - curveHeight} 
                    ${toX + horizontalOffset},${toY + curveHeight} 
                    ${toX},${toY}`;
        }
        // Handle multi-stage crossing arrows
        else if (stageDistance > 1) {
            const intermediateJobs = getIntermediateJobs(fromStage, toStage);
            const boundingBoxes = intermediateJobs.map(job => job.getBoundingClientRect());

            if (boundingBoxes.length > 0) {
                const shouldGoBelow = shouldRouteBelowJobs(boundingBoxes, fromY, toY);
                const verticalOffset = shouldGoBelow ? 40 : -40;
                const maxBottom = Math.max(...boundingBoxes.map(box => box.bottom));
                const minTop = Math.min(...boundingBoxes.map(box => box.top));

                pathData = shouldGoBelow ?
                    `M${fromX},${fromY}
                     C${fromX + horizontalGap * 0.2},${fromY + verticalOffset}
                      ${fromX + horizontalGap * 0.5},${maxBottom + 20}
                      ${actualToX},${toY}` :
                    `M${fromX},${fromY}
                     C${fromX + horizontalGap * 0.2},${fromY - verticalOffset}
                      ${fromX + horizontalGap * 0.5},${minTop - 20}
                      ${actualToX},${toY}`;
            } else {
                const midPointOffset = Math.min(Math.abs(verticalGap) * 0.3, 60);
                const sign = verticalGap >= 0 ? 1 : -1;
                pathData = `M${fromX},${fromY}
                       C${fromX + horizontalGap * 0.2},${fromY}
                        ${fromX + horizontalGap * 0.5},${fromY + sign * midPointOffset}
                        ${actualToX},${toY}`;
            }
        }
        // Handle adjacent stage arrows
        else {
            const verticalOffset = 15 * (dependencyIndex - (totalDependencies - 1) / 2);
            const curveStrength = 0.3;
            pathData = `M${fromX},${fromY} 
                   C${fromX + horizontalGap * curveStrength},${fromY} 
                    ${actualToX - horizontalGap * curveStrength},${toY + verticalOffset} 
                    ${actualToX},${toY}`;
        }

        path.setAttribute('d', pathData.trim().replace(/\s+/g, ' '));
        path.setAttribute('class', 'pipeline-arrow');

        if (stageDistance > 0) {
            path.classList.add('cross-stage');
        }

        svg.appendChild(path);
    }

    /**
     * Gets all jobs between two stages for path routing
     * @param {number} fromStage - Source stage index
     * @param {number} toStage - Target stage index
     * @returns {Element[]} Array of intermediate job elements
     */
    function getIntermediateJobs(fromStage, toStage) {
        const stages = Array.from(document.querySelectorAll('.stage'));
        const intermediateStages = stages.slice(
            Math.min(fromStage, toStage) + 1,
            Math.max(fromStage, toStage)
        );

        return intermediateStages.flatMap(stage =>
            Array.from(stage.querySelectorAll('.job'))
        );
    }

    /**
     * Determines if arrow path should route below intermediate jobs
     * @param {DOMRect[]} boundingBoxes - Bounding boxes of intermediate jobs
     * @param {number} fromY - Start Y coordinate
     * @param {number} toY - End Y coordinate
     * @returns {boolean} True if path should go below
     */
    function shouldRouteBelowJobs(boundingBoxes, fromY, toY) {
        if (boundingBoxes.length === 0) return false;

        const middleY = (fromY + toY) / 2;
        const boxesMiddleY = boundingBoxes.reduce((sum, box) =>
            sum + (box.top + box.bottom) / 2, 0
        ) / boundingBoxes.length;

        return middleY > boxesMiddleY;
    }

    /**
     * Draws an arrow connecting two job elements
     * @param {Element} fromElement - Source job element
     * @param {Element} toElement - Target job element
     * @param {number} dependencyIndex - Index of current dependency
     * @param {number} totalDependencies - Total number of dependencies
     */
    function drawArrow(fromElement, toElement, dependencyIndex, totalDependencies) {
        const fromRect = fromElement.getBoundingClientRect();
        const toRect = toElement.getBoundingClientRect();
        const svgRect = svg.getBoundingClientRect();

        const fromStageIndex = getStageIndex(fromElement);
        const toStageIndex = getStageIndex(toElement);

        const [fromX, fromY, toX, toY] = calculateArrowPoints(
            fromRect, toRect, svgRect,
            fromStageIndex === toStageIndex
        );

        createArrowPath(
            fromX, fromY, toX, toY,
            fromStageIndex, toStageIndex,
            dependencyIndex, totalDependencies
        );
    }

    /**
     * Updates the SVG container size to match the stages container
     * Ensures arrows are properly positioned within the viewport
     */
    function updateSvgSize() {
        const container = document.querySelector('.stages-container');
        if (!container) {
            console.error('Container not found');
            return;
        }
        const rect = container.getBoundingClientRect();
        svg.setAttribute('width', String(rect.width));
        svg.setAttribute('height', String(rect.height));
    }

    /**
     * Gets the stage index for a given job element
     * @param {Element} element - Job element to find stage index for
     * @returns {number} Index of the stage containing the element
     */
    function getStageIndex(element) {
        const stages = Array.from(document.querySelectorAll('.stage'));
        return stages.indexOf(element.closest('.stage'));
    }

    /**
     * Removes all existing arrows from the SVG container
     * Used before redrawing arrows to prevent duplicates
     */
    function clearArrows() {
        const arrows = svg.querySelectorAll('.pipeline-arrow');
        arrows.forEach(arrow => arrow.remove());
    }

    /**
     * Draws all dependency arrows for the pipeline
     * Processes each job's dependencies and creates corresponding arrows
     */
    function drawAllArrows() {
        clearArrows();
        const jobs = document.querySelectorAll('.job');

        jobs.forEach(job => {
            const needs = job.getAttribute('data-needs');
            if (needs) {
                const dependencies = needs.split(',').filter(dep => dep);
                dependencies.forEach((dep, index) => {
                    const fromElement = document.getElementById(`job_${dep}`);
                    if (fromElement) {
                        drawArrow(fromElement, job, index, dependencies.length);
                    }
                });
            }
        });
    }

    // Initialize pipeline visualization
    createArrowMarkers();
    updateSvgSize();
    drawAllArrows();

    // Add window resize handler
    window.addEventListener('resize', () => {
        requestAnimationFrame(() => {
            updateSvgSize();
            drawAllArrows();
        });
    });
});