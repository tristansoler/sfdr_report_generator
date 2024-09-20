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

                const startX = parentRect.left + parentRect.width / 2 - svgRect.left;
                const startY = parentRect.bottom - svgRect.top;
                const endX = nodeRect.left + nodeRect.width / 2 - svgRect.left;
                const endY = nodeRect.top - svgRect.top;

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