function clamp(value, min, max) {
    if (min !== undefined && min !== null && !isNaN(min)) value = Math.max(min, value);
    if (max !== undefined && max !== null && !isNaN(max)) value = Math.min(max, value);
    return value;
}
function toDateString(totalSeconds) {
    var minutes = parseInt(totalSeconds / 60) % 60;
    var seconds = totalSeconds % 60;
    return (minutes < 10 ? '0' + minutes : minutes) + ':' + (seconds < 10 ? '0' + seconds : seconds);
}

