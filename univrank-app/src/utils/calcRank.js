/**
 * Calculate the median of an array of numbers.
 * Ignores null/undefined/NaN values.
 */
export const calculateMedian = (numbers) => {
    const validNumbers = numbers
        .filter(n => n !== null && n !== undefined && !isNaN(n))
        .sort((a, b) => a - b);
    
    if (validNumbers.length === 0) return null;
    
    const middle = Math.floor(validNumbers.length / 2);
    
    if (validNumbers.length % 2 !== 0) {
        return validNumbers[middle];
    }
    
    // Average of two middle numbers, rounded to nearest int
    return Math.round((validNumbers[middle - 1] + validNumbers[middle]) / 2);
};

/**
 * Normalizes scores from different platforms if needed, 
 * but for this task, the user specified Median Rank.
 */
export const getUNIVrank = (university) => {
    const ranks = [
        university.qs_rank,
        university.the_rank,
        university.arwu_rank, // Added ARWU
        university.scimago_rank,
        university.webometrics_rank,
        university.studyportals_rank,
        university.uniranks_rank
    ];
    
    return calculateMedian(ranks);
};
