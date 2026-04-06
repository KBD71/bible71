const CACHE_NAME = 'bible-app-v2';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './back.png',
    'https://cdn.tailwindcss.com?v=3.4.0&cache-bust=20250915',
    'https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;500;600;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap'
];

self.addEventListener('install', (event) => {
    self.skipWaiting(); // 새로운 서비스 워커 즉시 활성화
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(ASSETS_TO_CACHE))
    );
});

self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    
    // HTML과 TXT 파일은 Network First 전략 (최신 콘텐츠 보장)
    if (url.pathname.endsWith('.html') || url.pathname.endsWith('.txt') || url.pathname === '/') {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    // 네트워크 응답이 정상이면 캐시 업데이트
                    if (response && response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            if (event.request.url.startsWith('http')) {
                                cache.put(event.request, responseClone);
                            }
                        });
                    }
                    return response;
                })
                .catch(() => {
                    // 네트워크 실패 시 캐시에서 반환
                    return caches.match(event.request);
                })
        );
    } else {
        // 기타 정적 리소스(이미지, CSS 등)는 Cache First 전략
        event.respondWith(
            caches.match(event.request)
                .then((response) => {
                    return response || fetch(event.request).then((fetchResponse) => {
                        if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
                            return fetchResponse;
                        }
                        const responseToCache = fetchResponse.clone();
                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                if (event.request.url.startsWith('http')) {
                                    cache.put(event.request, responseToCache);
                                }
                            });
                        return fetchResponse;
                    });
                })
        );
    }
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
        }).then(() => self.clients.claim()) // 즉시 제어권 가져오기
    );
});
