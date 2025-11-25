const CACHE_NAME = 'bible-app-v1';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './back.png',
    'https://cdn.tailwindcss.com?v=3.4.0&cache-bust=20250915',
    'https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;500;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(ASSETS_TO_CACHE))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // 캐시된 응답이 있으면 반환, 없으면 네트워크 요청
                return response || fetch(event.request).then((fetchResponse) => {
                    // 유효한 응답인지 확인
                    if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
                        return fetchResponse;
                    }
                    
                    // 응답을 복제하여 캐시에 저장 (동적 캐싱)
                    const responseToCache = fetchResponse.clone();
                    caches.open(CACHE_NAME)
                        .then((cache) => {
                            // file:// 프로토콜이나 외부 도메인 일부는 캐시되지 않을 수 있음
                            if (event.request.url.startsWith('http')) {
                                cache.put(event.request, responseToCache);
                            }
                        });
                        
                    return fetchResponse;
                });
            })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
