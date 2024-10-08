// flowchart-script.js
document.addEventListener("DOMContentLoaded", function() {
    const svg = document.querySelector('.flowchart-lines');
    const nodes = document.querySelectorAll('.node');

    nodes.forEach(node => {
        const parentID = node.getAttribute('data-parent');
        if (parentID) {
            const parentNode = document.getElementById(parentID);
            if (parentNode) {
                // Create a polyline instead of a line
                const polyline = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');

                const parentRect = parentNode.getBoundingClientRect();
                const nodeRect = node.getBoundingClientRect();
                const svgRect = svg.getBoundingClientRect();

                // Calculate start and end points
                const startX = parentRect.right - svgRect.left; // Right edge of parent node
                const startY = parentRect.top + parentRect.height / 2 - svgRect.top; // Vertical center of parent

                const endX = nodeRect.left - svgRect.left; // Left edge of child node
                const endY = nodeRect.top + nodeRect.height / 2 - svgRect.top; // Vertical center of child

                // Calculate intermediate points to create angled lines
                const midX = (startX + endX) / 2;

                // Define points for the polyline (right-angle connection)
                const points = [
                    `${startX},${startY}`,    // Starting point at parent node
                    `${midX},${startY}`,      // Horizontal line to midX
                    `${midX},${endY}`,        // Vertical line to align with child node
                    `${endX},${endY}`         // Horizontal line to child node
                ].join(' ');

                // Set attributes for the polyline
                polyline.setAttribute('points', points);
                polyline.setAttribute('fill', 'none');
                polyline.setAttribute('stroke', 'black');
                polyline.setAttribute('stroke-width', '1'); // Thinner line

                // Append the polyline to the SVG
                svg.appendChild(polyline);

            }
        }
    });
});