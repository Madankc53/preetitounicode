/**
 * search-engine.js
 * Powerful fuzzy search engine with autocomplete
 * Uses Levenshtein distance for typo tolerance
 */

class SearchEngine {
    constructor(database = []) {
        this.database = database;
        this.cache = new Map();
        this.maxResults = 10;
        this.minScore = 0;
    }

    /**
     * Levenshtein Distance Algorithm
     * Calculates the minimum edits needed to transform one string to another
     */
    levenshteinDistance(a, b) {
        const aLen = a.length;
        const bLen = b.length;
        const matrix = Array(bLen + 1)
            .fill(null)
            .map(() => Array(aLen + 1).fill(0));

        for (let i = 0; i <= aLen; i++) matrix[0][i] = i;
        for (let j = 0; j <= bLen; j++) matrix[j][0] = j;

        for (let j = 1; j <= bLen; j++) {
            for (let i = 1; i <= aLen; i++) {
                const indicator = a[i - 1] === b[j - 1] ? 0 : 1;
                matrix[j][i] = Math.min(
                    matrix[j][i - 1] + 1,
                    matrix[j - 1][i] + 1,
                    matrix[j - 1][i - 1] + indicator
                );
            }
        }
        return matrix[bLen][aLen];
    }

    /**
     * Calculate relevance score for a database item
     */
    calculateScore(item, query) {
        const q = query.toLowerCase().trim();
        const title = item.title.toLowerCase();
        const category = item.category.toLowerCase();
        const keywords = (item.keywords || []).map(k => k.toLowerCase());

        let score = 0;

        // Exact match (highest priority)
        if (title === q) return 1000;

        // Starts with query
        if (title.startsWith(q)) score += 300;

        // Contains full query as word boundary
        if (` ${title}`.includes(` ${q}`)) score += 250;

        // Contains query
        if (title.includes(q)) score += 150;

        // Partial word match
        const titleWords = title.split(/[\s\-_/]/);
        titleWords.forEach(word => {
            if (word.startsWith(q)) score += 100;
            if (word.includes(q)) score += 50;
        });

        // Category match
        if (category.includes(q)) score += 100;
        if (category.startsWith(q)) score += 80;

        // Keyword matches
        keywords.forEach(keyword => {
            if (keyword === q) score += 200;
            if (keyword.startsWith(q)) score += 120;
            if (keyword.includes(q)) score += 80;
        });

        // Levenshtein distance (typo tolerance)
        const distance = this.levenshteinDistance(q, title);
        if (distance <= 2) score += 100 - distance * 20;
        if (distance <= 3) score += 50 - distance * 10;

        // Character sequence matching
        let charIndex = 0;
        for (let char of title) {
            if (char === q[charIndex]) {
                charIndex++;
                score += 5;
            }
        }
        if (charIndex > 1) score += charIndex * 10;

        return score;
    }

    /**
     * Main search function with fuzzy matching
     */
    search(query, maxResults = this.maxResults) {
        const q = query.trim();
        
        // Check cache
        if (this.cache.has(q)) {
            return this.cache.get(q);
        }

        if (q.length === 0) return [];

        // Score all database items
        const scored = this.database
            .map(item => ({
                ...item,
                score: this.calculateScore(item, q),
                relevance: this.calculateRelevance(item, q)
            }))
            .filter(item => item.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, maxResults);

        // Cache result
        this.cache.set(q, scored);
        
        return scored;
    }

    /**
     * Calculate additional relevance metrics
     */
    calculateRelevance(item, query) {
        const q = query.toLowerCase();
        const title = item.title.toLowerCase();
        
        if (title === q) return 'exact';
        if (title.startsWith(q)) return 'prefix';
        if (title.includes(q)) return 'contains';
        return 'fuzzy';
    }

    /**
     * Get suggestions as user types
     */
    getAutocompleteSuggestions(query, limit = 5) {
        return this.search(query, limit);
    }

    /**
     * Clear cache to free memory
     */
    clearCache() {
        this.cache.clear();
    }

    /**
     * Update database
     */
    updateDatabase(newDatabase) {
        this.database = newDatabase;
        this.clearCache();
    }

    /**
     * Get search statistics
     */
    getStats() {
        return {
            databaseSize: this.database.length,
            cacheSize: this.cache.size,
            categories: [...new Set(this.database.map(item => item.category))]
        };
    }
}

/**
 * Initialize global search engine
 */
window.searchEngine = new SearchEngine(window.siteSearchDatabase || []);

// Export for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SearchEngine;
}
