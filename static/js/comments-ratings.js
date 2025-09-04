// Comments and Ratings JavaScript functionality

class CommentsRatingsManager {
    constructor() {
        this.currentAdId = null;
        this.currentUserId = null;
        this.authToken = null;
        this.init();
    }

    init() {
        // Get auth token from localStorage or wherever it's stored
        this.authToken = localStorage.getItem('authToken');
        this.attachEventListeners();
    }

    attachEventListeners() {
        // Add comment button
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-comment-btn')) {
                this.showCommentForm(e.target.dataset.adId);
            }
            
            if (e.target.classList.contains('submit-comment-btn')) {
                this.submitComment(e.target.dataset.adId);
            }
            
            if (e.target.classList.contains('cancel-comment-btn')) {
                this.hideCommentForm();
            }
            
            if (e.target.classList.contains('edit-comment-btn')) {
                this.editComment(e.target.dataset.commentId);
            }
            
            if (e.target.classList.contains('delete-comment-btn')) {
                this.deleteComment(e.target.dataset.commentId);
            }
            
            if (e.target.classList.contains('submit-rating-btn')) {
                this.submitRating(e.target.dataset.adId);
            }
            
            if (e.target.classList.contains('star')) {
                this.handleStarClick(e.target);
            }
        });

        // Star hover effects
        document.addEventListener('mouseover', (e) => {
            if (e.target.classList.contains('star') && e.target.dataset.rating) {
                this.handleStarHover(e.target);
            }
        });

        document.addEventListener('mouseout', (e) => {
            if (e.target.classList.contains('star') && e.target.dataset.rating) {
                this.clearStarHover();
            }
        });
    }

    async loadComments(adId, page = 1) {
        try {
            const response = await fetch(`/ads/ads/${adId}/comments?page=${page}&per_page=10`);
            const data = await response.json();
            
            if (response.ok) {
                this.displayComments(data.data, data.pagination);
            } else {
                this.showError('Помилка завантаження коментарів: ' + data.error);
            }
        } catch (error) {
            this.showError('Помилка мережі при завантаженні коментарів');
        }
    }

    displayComments(comments, pagination) {
        const commentsContainer = document.getElementById('comments-list');
        if (!commentsContainer) return;

        if (comments.length === 0) {
            commentsContainer.innerHTML = '<div class="no-comments">Коментарів поки немає. Будьте першим!</div>';
            return;
        }

        const commentsHTML = comments.map(comment => `
            <div class="comment-item" data-comment-id="${comment.id}">
                <div class="comment-header">
                    <span class="comment-author">${this.escapeHtml(comment.user_email)}</span>
                    <span class="comment-date">${this.formatDate(comment.created_at)}</span>
                </div>
                <div class="comment-content">${this.escapeHtml(comment.content)}</div>
                ${comment.user_id === this.currentUserId ? `
                    <div class="comment-actions">
                        <button class="edit-comment-btn" data-comment-id="${comment.id}">Редагувати</button>
                        <button class="delete-comment-btn" data-comment-id="${comment.id}">Видалити</button>
                    </div>
                ` : ''}
            </div>
        `).join('');

        commentsContainer.innerHTML = commentsHTML;
        this.displayPagination('comments', pagination);
    }

    showCommentForm(adId) {
        this.currentAdId = adId;
        const formHTML = `
            <div class="comment-form" id="comment-form">
                <textarea class="comment-textarea" id="comment-content" placeholder="Напишіть ваш коментар..."></textarea>
                <div class="comment-form-actions">
                    <button class="submit-comment-btn" data-ad-id="${adId}">Опублікувати</button>
                    <button class="cancel-comment-btn">Скасувати</button>
                </div>
            </div>
        `;
        
        const commentsSection = document.getElementById('comments-section');
        const existingForm = document.getElementById('comment-form');
        
        if (existingForm) {
            existingForm.remove();
        }
        
        commentsSection.insertAdjacentHTML('afterbegin', formHTML);
        document.getElementById('comment-content').focus();
    }

    hideCommentForm() {
        const form = document.getElementById('comment-form');
        if (form) {
            form.remove();
        }
    }

    async submitComment(adId) {
        const content = document.getElementById('comment-content').value.trim();
        
        if (!content) {
            this.showError('Коментар не може бути порожнім');
            return;
        }

        if (!this.authToken) {
            this.showError('Для додавання коментарів потрібно увійти в систему');
            return;
        }

        try {
            const response = await fetch(`/ads/ads/${adId}/comments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify({ content })
            });

            const data = await response.json();
            
            if (response.ok) {
                this.showSuccess('Коментар додано успішно');
                this.hideCommentForm();
                this.loadComments(adId);
            } else {
                this.showError('Помилка додавання коментаря: ' + data.error);
            }
        } catch (error) {
            this.showError('Помилка мережі при додаванні коментаря');
        }
    }

    async deleteComment(commentId) {
        if (!confirm('Ви впевнені, що хочете видалити цей коментар?')) {
            return;
        }

        if (!this.authToken) {
            this.showError('Для видалення коментарів потрібно увійти в систему');
            return;
        }

        try {
            const response = await fetch(`/ads/comments/${commentId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.authToken}`
                }
            });

            const data = await response.json();
            
            if (response.ok) {
                this.showSuccess('Коментар видалено успішно');
                this.loadComments(this.currentAdId);
            } else {
                this.showError('Помилка видалення коментаря: ' + data.error);
            }
        } catch (error) {
            this.showError('Помилка мережі при видаленні коментаря');
        }
    }

    async loadUserRatings(userId, page = 1) {
        try {
            const response = await fetch(`/ads/users/${userId}/ratings?page=${page}&per_page=10`);
            const data = await response.json();
            
            if (response.ok) {
                this.displayRatings(data.data, data.statistics, data.pagination);
            } else {
                this.showError('Помилка завантаження рейтингів: ' + data.error);
            }
        } catch (error) {
            this.showError('Помилка мережі при завантаженні рейтингів');
        }
    }

    displayRatings(ratings, statistics, pagination) {
        const ratingsContainer = document.getElementById('ratings-list');
        const summaryContainer = document.getElementById('rating-summary');
        
        if (!ratingsContainer) return;

        // Display rating summary
        if (summaryContainer && statistics) {
            summaryContainer.innerHTML = `
                <div class="user-rating-summary">
                    <div class="rating-stars">
                        ${this.generateStarsDisplay(statistics.average_rating)}
                    </div>
                    <div class="rating-info">
                        <strong>${statistics.average_rating}/5</strong> 
                        (${statistics.total_ratings} ${this.pluralize(statistics.total_ratings, 'оцінка', 'оцінки', 'оцінок')})
                    </div>
                </div>
            `;
        }

        if (ratings.length === 0) {
            ratingsContainer.innerHTML = '<div class="no-ratings">Рейтингів поки немає.</div>';
            return;
        }

        const ratingsHTML = ratings.map(rating => `
            <div class="rating-item" data-rating-id="${rating.id}">
                <div class="rating-item-header">
                    <span class="rating-author">${this.escapeHtml(rating.rater_email)}</span>
                    <span class="rating-date">${this.formatDate(rating.created_at)}</span>
                </div>
                <div class="rating-stars-display">
                    ${this.generateStarsDisplay(rating.rating)}
                </div>
                ${rating.comment ? `
                    <div class="rating-comment-content">"${this.escapeHtml(rating.comment)}"</div>
                ` : ''}
            </div>
        `).join('');

        ratingsContainer.innerHTML = ratingsHTML;
        this.displayPagination('ratings', pagination);
    }

    handleStarClick(starElement) {
        const rating = parseInt(starElement.dataset.rating);
        const starsContainer = starElement.parentElement;
        
        // Update visual state
        this.updateStarsDisplay(starsContainer, rating);
        
        // Store selected rating
        starsContainer.dataset.selectedRating = rating;
    }

    handleStarHover(starElement) {
        const rating = parseInt(starElement.dataset.rating);
        const starsContainer = starElement.parentElement;
        
        this.updateStarsDisplay(starsContainer, rating, true);
    }

    clearStarHover() {
        const starsContainers = document.querySelectorAll('.rating-stars-input');
        starsContainers.forEach(container => {
            const selectedRating = parseInt(container.dataset.selectedRating) || 0;
            this.updateStarsDisplay(container, selectedRating);
        });
    }

    updateStarsDisplay(container, rating, isHover = false) {
        const stars = container.querySelectorAll('.star');
        stars.forEach((star, index) => {
            star.classList.remove('filled', 'hover');
            if (index < rating) {
                star.classList.add(isHover ? 'hover' : 'filled');
            }
        });
    }

    generateStarsDisplay(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let starsHTML = '';
        
        for (let i = 0; i < 5; i++) {
            if (i < fullStars) {
                starsHTML += '<span class="star filled">★</span>';
            } else if (i === fullStars && hasHalfStar) {
                starsHTML += '<span class="star filled">☆</span>';
            } else {
                starsHTML += '<span class="star">☆</span>';
            }
        }
        
        return starsHTML;
    }

    async submitRating(adId) {
        const ratingContainer = document.querySelector('.rating-stars-input');
        const rating = parseInt(ratingContainer.dataset.selectedRating);
        const comment = document.getElementById('rating-comment').value.trim();

        if (!rating) {
            this.showError('Будь ласка, оберіть рейтинг');
            return;
        }

        if (!this.authToken) {
            this.showError('Для оцінювання потрібно увійти в систему');
            return;
        }

        try {
            const response = await fetch(`/ads/ads/${adId}/rate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.authToken}`
                },
                body: JSON.stringify({ rating, comment })
            });

            const data = await response.json();
            
            if (response.ok) {
                this.showSuccess('Рейтинг додано успішно');
                // Reset form
                ratingContainer.dataset.selectedRating = '0';
                this.updateStarsDisplay(ratingContainer, 0);
                document.getElementById('rating-comment').value = '';
                // Reload ratings if on user profile
                if (this.currentUserId) {
                    this.loadUserRatings(this.currentUserId);
                }
            } else {
                this.showError('Помилка додавання рейтингу: ' + data.error);
            }
        } catch (error) {
            this.showError('Помилка мережі при додаванні рейтингу');
        }
    }

    displayPagination(type, pagination) {
        const paginationContainer = document.getElementById(`${type}-pagination`);
        if (!paginationContainer || pagination.pages <= 1) return;

        const paginationHTML = `
            <div class="pagination">
                <button class="pagination-btn" ${pagination.page <= 1 ? 'disabled' : ''} 
                        onclick="commentsRatingsManager.loadPage('${type}', ${pagination.page - 1})">
                    Попередня
                </button>
                <span class="pagination-info">
                    Сторінка ${pagination.page} з ${pagination.pages}
                </span>
                <button class="pagination-btn" ${pagination.page >= pagination.pages ? 'disabled' : ''} 
                        onclick="commentsRatingsManager.loadPage('${type}', ${pagination.page + 1})">
                    Наступна
                </button>
            </div>
        `;

        paginationContainer.innerHTML = paginationHTML;
    }

    loadPage(type, page) {
        if (type === 'comments' && this.currentAdId) {
            this.loadComments(this.currentAdId, page);
        } else if (type === 'ratings' && this.currentUserId) {
            this.loadUserRatings(this.currentUserId, page);
        }
    }

    showError(message) {
        this.showMessage(message, 'error');
    }

    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    showMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        messageDiv.textContent = message;
        
        const container = document.querySelector('.comments-section, .rating-section') || document.body;
        container.insertBefore(messageDiv, container.firstChild);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('uk-UA', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    pluralize(count, one, few, many) {
        if (count % 10 === 1 && count % 100 !== 11) {
            return one;
        } else if (count % 10 >= 2 && count % 10 <= 4 && (count % 100 < 10 || count % 100 >= 20)) {
            return few;
        } else {
            return many;
        }
    }

    // Public methods for external use
    setCurrentAdId(adId) {
        this.currentAdId = adId;
    }

    setCurrentUserId(userId) {
        this.currentUserId = userId;
    }

    setAuthToken(token) {
        this.authToken = token;
    }
}

// Initialize the manager
const commentsRatingsManager = new CommentsRatingsManager();

// Export for use in other scripts
window.commentsRatingsManager = commentsRatingsManager;