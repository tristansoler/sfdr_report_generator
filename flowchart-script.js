// flowchart-script.js
document.addEventListener("DOMContentLoaded", function() {
    const svg = document.querySelector('.flowchart-lines');
    const nodes = document.querySelectorAll('.node');

    nodes.forEach(node => {
        const parentID = node.getAttribute('data-parent');
        if (parentID) {
            const parentNode = document.getElementById(parentID);
            if (parentNode) {
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                
                const parentRect = parentNode.getBoundingClientRect();
                const nodeRect = node.getBoundingClientRect();
                const svgRect = svg.getBoundingClientRect();

                // Adjusted calculations for horizontal layout
                const startX = parentRect.right - svgRect.left; // Right edge of parent node
                const startY = parentRect.top + parentRect.height / 2 - svgRect.top; // Vertical center of parent
                const endX = nodeRect.left - svgRect.left; // Left edge of child node
                const endY = nodeRect.top + nodeRect.height / 2 - svgRect.top; // Vertical center of child


                line.setAttribute('x1', startX);
                line.setAttribute('y1', startY);
                line.setAttribute('x2', endX);
                line.setAttribute('y2', endY);
                line.setAttribute('stroke', 'black');
                line.setAttribute('stroke-width', '2');
                svg.appendChild(line);
            }
        }
    });
});