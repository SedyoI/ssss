// Ukraine regions data
const ukraineRegions = [
    { id: 'vinnytsia', name: 'Вінницька область', center: [49.2328, 28.4816] },
    { id: 'volyn', name: 'Волинська область', center: [50.7472, 25.3254] },
    { id: 'dnipropetrovsk', name: 'Дніпропетровська область', center: [48.4647, 35.0462] },
    { id: 'donetsk', name: 'Донецька область', center: [48.0159, 37.8028] },
    { id: 'zhytomyr', name: 'Житомирська область', center: [50.2547, 28.6587] },
    { id: 'zakarpattia', name: 'Закарпатська область', center: [48.6208, 22.2879] },
    { id: 'zaporizhzhia', name: 'Запорізька область', center: [47.8388, 35.1396] },
    { id: 'ivano-frankivsk', name: 'Івано-Франківська область', center: [48.9226, 24.7111] },
    { id: 'kyiv', name: 'Київська область', center: [50.4501, 30.5234] },
    { id: 'kirovohrad', name: 'Кіровоградська область', center: [48.5132, 32.2597] },
    { id: 'luhansk', name: 'Луганська область', center: [48.5740, 39.3078] },
    { id: 'lviv', name: 'Львівська область', center: [49.8397, 24.0297] },
    { id: 'mykolaiv', name: 'Миколаївська область', center: [46.9750, 32.0598] },
    { id: 'odesa', name: 'Одеська область', center: [46.4825, 30.7233] },
    { id: 'poltava', name: 'Полтавська область', center: [49.5883, 34.5514] },
    { id: 'rivne', name: 'Рівненська область', center: [50.6199, 26.2516] },
    { id: 'sumy', name: 'Сумська область', center: [50.9077, 34.7981] },
    { id: 'ternopil', name: 'Тернопільська область', center: [49.5535, 25.5948] },
    { id: 'kharkiv', name: 'Харківська область', center: [49.9935, 36.2304] },
    { id: 'kherson', name: 'Херсонська область', center: [46.6354, 32.6169] },
    { id: 'khmelnytskyi', name: 'Хмельницька область', center: [49.4229, 26.9871] },
    { id: 'cherkasy', name: 'Черкаська область', center: [49.4444, 32.0598] },
    { id: 'chernivtsi', name: 'Чернівецька область', center: [48.2919, 25.9358] },
    { id: 'chernihiv', name: 'Чернігівська область', center: [51.4982, 31.2893] },
    { id: 'kyiv-city', name: 'м. Київ', center: [50.4501, 30.5234] }
];

class UkraineMap {
    constructor() {
        this.selectedRegion = null;
        this.currentAds = [];
        this.init();
    }

    init() {
        this.createMapHTML();
        this.attachEventListeners();
    }

    createMapHTML() {
        const mapContainer = document.getElementById('ukraine-map-container');
        if (!mapContainer) return;

        mapContainer.innerHTML = `
            <div class="ukraine-map-container">
                <h2 class="map-title">Оберіть регіон України</h2>
                
                <div class="search-controls">
                    <input type="text" id="search-input" class="search-input" placeholder="Пошук оголошень...">
                    <button id="search-btn" class="search-btn">Пошук</button>
                    <button id="clear-btn" class="clear-btn">Очистити</button>
                </div>

                <svg class="ukraine-map" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
                    <!-- Simplified Ukraine map with clickable regions -->
                    <g id="ukraine-regions">
                        <!-- Київська область -->
                        <path id="kyiv" class="region" d="M380 200 L420 200 L420 240 L380 240 Z" />
                        <text x="400" y="225" class="region-label">Київська</text>
                        
                        <!-- Львівська область -->
                        <path id="lviv" class="region" d="M200 220 L240 220 L240 260 L200 260 Z" />
                        <text x="220" y="245" class="region-label">Львівська</text>
                        
                        <!-- Харківська область -->
                        <path id="kharkiv" class="region" d="M520 200 L560 200 L560 240 L520 240 Z" />
                        <text x="540" y="225" class="region-label">Харківська</text>
                        
                        <!-- Одеська область -->
                        <path id="odesa" class="region" d="M300 380 L340 380 L340 420 L300 420 Z" />
                        <text x="320" y="405" class="region-label">Одеська</text>
                        
                        <!-- Дніпропетровська область -->
                        <path id="dnipropetrovsk" class="region" d="M440 280 L480 280 L480 320 L440 320 Z" />
                        <text x="460" y="305" class="region-label">Дніпропетровська</text>
                        
                        <!-- Донецька область -->
                        <path id="donetsk" class="region" d="M520 280 L560 280 L560 320 L520 320 Z" />
                        <text x="540" y="305" class="region-label">Донецька</text>
                        
                        <!-- Запорізька область -->
                        <path id="zaporizhzhia" class="region" d="M440 340 L480 340 L480 380 L440 380 Z" />
                        <text x="460" y="365" class="region-label">Запорізька</text>
                        
                        <!-- Полтавська область -->
                        <path id="poltava" class="region" d="M440 220 L480 220 L480 260 L440 260 Z" />
                        <text x="460" y="245" class="region-label">Полтавська</text>
                        
                        <!-- Черкаська область -->
                        <path id="cherkasy" class="region" d="M380 260 L420 260 L420 300 L380 300 Z" />
                        <text x="400" y="285" class="region-label">Черкаська</text>
                        
                        <!-- Вінницька область -->
                        <path id="vinnytsia" class="region" d="M320 260 L360 260 L360 300 L320 300 Z" />
                        <text x="340" y="285" class="region-label">Вінницька</text>
                        
                        <!-- Хмельницька область -->
                        <path id="khmelnytskyi" class="region" d="M280 220 L320 220 L320 260 L280 260 Z" />
                        <text x="300" y="245" class="region-label">Хмельницька</text>
                        
                        <!-- Тернопільська область -->
                        <path id="ternopil" class="region" d="M240 240 L280 240 L280 280 L240 280 Z" />
                        <text x="260" y="265" class="region-label">Тернопільська</text>
                        
                        <!-- Івано-Франківська область -->
                        <path id="ivano-frankivsk" class="region" d="M240 280 L280 280 L280 320 L240 320 Z" />
                        <text x="260" y="305" class="region-label">Івано-Франківська</text>
                        
                        <!-- Закарпатська область -->
                        <path id="zakarpattia" class="region" d="M180 280 L220 280 L220 320 L180 320 Z" />
                        <text x="200" y="305" class="region-label">Закарпатська</text>
                        
                        <!-- Чернівецька область -->
                        <path id="chernivtsi" class="region" d="M280 320 L320 320 L320 360 L280 360 Z" />
                        <text x="300" y="345" class="region-label">Чернівецька</text>
                        
                        <!-- Волинська область -->
                        <path id="volyn" class="region" d="M240 180 L280 180 L280 220 L240 220 Z" />
                        <text x="260" y="205" class="region-label">Волинська</text>
                        
                        <!-- Рівненська область -->
                        <path id="rivne" class="region" d="M280 180 L320 180 L320 220 L280 220 Z" />
                        <text x="300" y="205" class="region-label">Рівненська</text>
                        
                        <!-- Житомирська область -->
                        <path id="zhytomyr" class="region" d="M320 180 L360 180 L360 220 L320 220 Z" />
                        <text x="340" y="205" class="region-label">Житомирська</text>
                        
                        <!-- Чернігівська область -->
                        <path id="chernihiv" class="region" d="M420 160 L460 160 L460 200 L420 200 Z" />
                        <text x="440" y="185" class="region-label">Чернігівська</text>
                        
                        <!-- Сумська область -->
                        <path id="sumy" class="region" d="M480 160 L520 160 L520 200 L480 200 Z" />
                        <text x="500" y="185" class="region-label">Сумська</text>
                        
                        <!-- Луганська область -->
                        <path id="luhansk" class="region" d="M560 240 L600 240 L600 280 L560 280 Z" />
                        <text x="580" y="265" class="region-label">Луганська</text>
                        
                        <!-- Херсонська область -->
                        <path id="kherson" class="region" d="M380 340 L420 340 L420 380 L380 380 Z" />
                        <text x="400" y="365" class="region-label">Херсонська</text>
                        
                        <!-- Миколаївська область -->
                        <path id="mykolaiv" class="region" d="M340 340 L380 340 L380 380 L340 380 Z" />
                        <text x="360" y="365" class="region-label">Миколаївська</text>
                        
                        <!-- Кіровоградська область -->
                        <path id="kirovohrad" class="region" d="M380 300 L420 300 L420 340 L380 340 Z" />
                        <text x="400" y="325" class="region-label">Кіровоградська</text>
                        
                        <!-- м. Київ -->
                        <circle id="kyiv-city" class="region" cx="400" cy="210" r="8" />
                        <text x="410" y="215" class="region-label">Київ</text>
                    </g>
                </svg>

                <div id="selected-region-info" class="selected-region-info" style="display: none;">
                    <h3 id="selected-region-name"></h3>
                    <p>Клікніть "Пошук", щоб знайти оголошення в цьому регіоні</p>
                </div>

                <div id="ads-results" class="ads-results"></div>
            </div>
        `;
    }

    attachEventListeners() {
        // Region click handlers
        document.querySelectorAll('.region').forEach(region => {
            region.addEventListener('click', (e) => {
                this.selectRegion(e.target.id);
            });
        });

        // Search button
        const searchBtn = document.getElementById('search-btn');
        if (searchBtn) {
            searchBtn.addEventListener('click', () => {
                this.searchAds();
            });
        }

        // Clear button
        const clearBtn = document.getElementById('clear-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.clearSearch();
            });
        }

        // Enter key in search input
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.searchAds();
                }
            });
        }
    }

    selectRegion(regionId) {
        // Clear previous selection
        document.querySelectorAll('.region').forEach(r => r.classList.remove('selected'));
        
        // Select new region
        const regionElement = document.getElementById(regionId);
        if (regionElement) {
            regionElement.classList.add('selected');
            this.selectedRegion = regionId;
            
            // Find region data
            const regionData = ukraineRegions.find(r => r.id === regionId);
            if (regionData) {
                this.showRegionInfo(regionData);
            }
        }
    }

    showRegionInfo(regionData) {
        const infoDiv = document.getElementById('selected-region-info');
        const nameElement = document.getElementById('selected-region-name');
        
        if (infoDiv && nameElement) {
            nameElement.textContent = regionData.name;
            infoDiv.style.display = 'block';
        }
    }

    async searchAds() {
        const searchInput = document.getElementById('search-input');
        const resultsDiv = document.getElementById('ads-results');
        
        if (!resultsDiv) return;

        // Show loading
        resultsDiv.innerHTML = '<div class="loading">Завантаження оголошень...</div>';

        try {
            let url = '/ads/ads?page=1&per_page=20';
            
            // Add region filter if selected
            if (this.selectedRegion) {
                const regionData = ukraineRegions.find(r => r.id === this.selectedRegion);
                if (regionData) {
                    url += `&location=${encodeURIComponent(regionData.name)}`;
                }
            }

            // Add search query if provided
            const searchQuery = searchInput ? searchInput.value.trim() : '';
            if (searchQuery) {
                url = `/ads/search?query=${encodeURIComponent(searchQuery)}`;
                if (this.selectedRegion) {
                    const regionData = ukraineRegions.find(r => r.id === this.selectedRegion);
                    if (regionData) {
                        url += `&location=${encodeURIComponent(regionData.name)}`;
                    }
                }
            }

            const response = await fetch(url);
            const data = await response.json();

            if (response.ok && data.data && data.data.length > 0) {
                this.displayAds(data.data);
            } else {
                resultsDiv.innerHTML = '<div class="no-results">Оголошення не знайдені в обраному регіоні.</div>';
            }
        } catch (error) {
            console.error('Error searching ads:', error);
            resultsDiv.innerHTML = '<div class="no-results">Помилка при завантаженні оголошень.</div>';
        }
    }

    displayAds(ads) {
        const resultsDiv = document.getElementById('ads-results');
        if (!resultsDiv) return;

        const adsHTML = ads.map(ad => `
            <div class="ad-card">
                <div class="ad-title">${this.escapeHtml(ad.title)}</div>
                <div class="ad-price">${ad.price} UAH</div>
                <div class="ad-location">📍 ${this.escapeHtml(ad.location)}</div>
                <div class="ad-description">${this.escapeHtml(ad.description)}</div>
                ${ad.images && ad.images.length > 0 ? `
                    <div class="ad-images">
                        ${ad.images.map(img => `
                            <img src="${img}" alt="Фото оголошення" class="ad-image" 
                                 onerror="this.style.display='none'">
                        `).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');

        resultsDiv.innerHTML = `
            <h3>Знайдено оголошень: ${ads.length}</h3>
            ${adsHTML}
        `;
    }

    clearSearch() {
        // Clear search input
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = '';
        }

        // Clear region selection
        document.querySelectorAll('.region').forEach(r => r.classList.remove('selected'));
        this.selectedRegion = null;

        // Hide region info
        const infoDiv = document.getElementById('selected-region-info');
        if (infoDiv) {
            infoDiv.style.display = 'none';
        }

        // Clear results
        const resultsDiv = document.getElementById('ads-results');
        if (resultsDiv) {
            resultsDiv.innerHTML = '';
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize map when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new UkraineMap();
});