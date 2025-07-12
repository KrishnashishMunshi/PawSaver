         dogs = [
    {'name': 'Sheru', 'x': 200, 'y': 300},
    {'name': 'Golu', 'x': 800, 'y': 400},
    {'name': 'Mitthu', 'x': 500, 'y': 600},
    {'name': 'Kaalu', 'x': 300, 'y': 700},
    {'name': 'Tinku', 'x': 600, 'y': 500},
    {'name': 'Bholu', 'x': 650, 'y': 650},
    {'name': 'Chotu', 'x': 215, 'y': 415},
    {'name': 'Jaadu', 'x': 623, 'y': 330},
    {'name': 'Pari', 'x': 900, 'y': 200},
    {'name': 'Tommy', 'x': 100, 'y': 300}
]
// Configuration
const MAP_CONFIG = {
    gridSize: 100,  // pixels per grid cell (representing 100m)
    maxRange: 1000, // maximum visible range in meters
    centerX: 600,   // canvas center X
    centerY: 400,   // canvas center Y
    colors: {
        grid: 'rgba(0, 0, 0, 0.05)',
        gridMain: 'rgba(0, 0, 0, 0.1)',
        labelText: '#374151',
        connectionLine: 'rgba(14, 165, 233, 0.2)'
    }
};

function drawGrid(ctx, canvas) {
    const { gridSize, colors } = MAP_CONFIG;
    
    // Draw grid lines
    ctx.strokeStyle = colors.grid;
    ctx.lineWidth = 1;
    
    // Vertical lines
    for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    
    // Horizontal lines
    for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    
    // Draw main axes with darker lines
    ctx.strokeStyle = colors.gridMain;
    ctx.lineWidth = 2;
    
    // Vertical center line
    ctx.beginPath();
    ctx.moveTo(MAP_CONFIG.centerX, 0);
    ctx.lineTo(MAP_CONFIG.centerX, canvas.height);
    ctx.stroke();
    
    // Horizontal center line
    ctx.beginPath();
    ctx.moveTo(0, MAP_CONFIG.centerY);
    ctx.lineTo(canvas.width, MAP_CONFIG.centerY);
    ctx.stroke();
}

function calculateDistance(x1, y1, x2, y2) {
    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
}

function drawDistanceMarkers(ctx, dogX, dogY) {
    const { centerX, centerY, colors } = MAP_CONFIG;
    const distance = calculateDistance(centerX, centerY, dogX, dogY);
    const distanceInMeters = Math.round(distance * (100 / MAP_CONFIG.gridSize)); // Convert pixels to meters
    
    // Draw arc at midpoint
    const midX = (centerX + dogX) / 2;
    const midY = (centerY + dogY) / 2;
    
    // Draw distance label
    ctx.fillStyle = colors.labelText;
    ctx.font = '12px Arial';
    ctx.fillText(`${distanceInMeters}m`, midX + 5, midY - 5);
}

function drawDogMarker(ctx, dog, healthStatus = 'Healthy') {
    // Define colors based on health status
    const statusColors = {
        'Healthy': ['#10B981', '#059669'],
        'At Risk': ['#F59E0B', '#D97706'],
        'Danger': ['#EF4444', '#DC2626']
    };
    
    const colors = statusColors[healthStatus] || statusColors['Healthy'];
    
    // Create gradient for dog marker
    const dogGradient = ctx.createRadialGradient(dog.x, dog.y, 0, dog.x, dog.y, 12);
    dogGradient.addColorStop(0, colors[0]);
    dogGradient.addColorStop(1, colors[1]);
    
    // Draw dog marker
    ctx.fillStyle = dogGradient;
    ctx.beginPath();
    ctx.arc(dog.x, dog.y, 10, 0, 2 * Math.PI);
    ctx.fill();
    
    // Draw dog name and status
    ctx.fillStyle = MAP_CONFIG.colors.labelText;
    ctx.font = 'bold 14px Arial';
    ctx.fillText(dog.name, dog.x + 15, dog.y);
    ctx.font = '12px Arial';
    ctx.fillText(healthStatus, dog.x + 15, dog.y + 15);
}

function drawMap() {
    const canvas = document.getElementById("mapCanvas");
    const ctx = canvas.getContext("2d");
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    drawGrid(ctx, canvas);
    
    // Draw user position (center)
    const { centerX, centerY } = MAP_CONFIG;
    
    // Draw user marker with gradient
    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 15);
    gradient.addColorStop(0, '#ec4899');
    gradient.addColorStop(1, '#db2777');
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(centerX, centerY, 12, 0, 2 * Math.PI);
    ctx.fill();
    
    // Draw "You" label
    ctx.fillStyle = MAP_CONFIG.colors.labelText;
    ctx.font = '14px Arial';
    ctx.fillText("You", centerX + 20, centerY);
    
    // Draw compass rose
    drawCompassRose(ctx, 50, 50);
    
    // Draw scale indicator on canvas
    drawScaleIndicator(ctx, canvas.width - 150, canvas.height - 40);
    
    // Draw dogs with different health statuses for demo
    const dogStatuses = {
        'Sheru': 'Healthy',
        'Golu': 'At Risk',
        'Mitthu': 'Healthy',
        'Kaalu': 'Healthy',
        'Tinku': 'At Risk',
        'Bholu': 'Healthy',
        'Chotu': 'Healthy',
        'Jaadu': 'At Risk',
        'Pari': 'Danger',
        'Tommy': 'Healthy'
    };
    
    dogs.forEach(dog => {
        // Draw connection line
        ctx.beginPath();
        ctx.strokeStyle = MAP_CONFIG.colors.connectionLine;
        ctx.lineWidth = 2;
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(dog.x, dog.y);
        ctx.stroke();
        
        // Draw distance marker
        drawDistanceMarkers(ctx, dog.x, dog.y);
        
        // Draw dog with health status
        drawDogMarker(ctx, dog, dogStatuses[dog.name]);
    });
}

function drawCompassRose(ctx, x, y) {
    const size = 40;
    const directions = ['N', 'E', 'S', 'W'];
    
    ctx.save();
    ctx.translate(x, y);
    
    // Draw circle
    ctx.beginPath();
    ctx.arc(0, 0, size, 0, 2 * Math.PI);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fill();
    ctx.strokeStyle = '#374151';
    ctx.stroke();
    
    // Draw direction letters
    ctx.fillStyle = '#374151';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    directions.forEach((dir, i) => {
        const angle = (i * Math.PI) / 2;
        const textX = Math.sin(angle) * (size - 15);
        const textY = -Math.cos(angle) * (size - 15);
        ctx.fillText(dir, textX, textY);
    });
    
    ctx.restore();
}

function drawScaleIndicator(ctx, x, y) {
    const scaleLength = MAP_CONFIG.gridSize; // 100m in pixels
    
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillRect(x - 10, y - 25, scaleLength + 20, 35);
    
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + scaleLength, y);
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    ctx.fillStyle = '#374151';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('100m', x + scaleLength/2, y - 8);
}

// Initial draw
document.addEventListener('DOMContentLoaded', drawMap);

// Optional: Add window resize handler
window.addEventListener('resize', () => {
    const canvas = document.getElementById("mapCanvas");
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    drawMap();
});