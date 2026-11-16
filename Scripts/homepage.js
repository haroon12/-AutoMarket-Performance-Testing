
import http from 'k6/http';
import { check, sleep } from 'k6';

// Read Base URL from environment variable
const BASE_URL = __ENV.BASE_URL;

// Validate environment variable
if (!BASE_URL) {
    throw new Error('BASE_URL environment variable is missing!');
}

// Test configuration
export const options = {
    vus: 1,
    iterations: 1,

    thresholds: {
        http_req_duration: ['p(95)<1000'],
        http_req_failed: ['rate<0.01'],
    },
};

// Homepage smoke test
export default function () {

    const response = http.get(`${BASE_URL}/`, {
        tags: { name: 'Homepage' },
    });

    check(response, {
        'Homepage status is 200': (r) => r.status === 200,
        'Homepage response time below 1000ms':
            (r) => r.timings.duration < 1000,
        'Homepage response body is not empty':
            (r) => r.body && r.body.length > 0,
    });

    sleep(1);
}
