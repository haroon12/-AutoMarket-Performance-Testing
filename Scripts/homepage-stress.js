
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL;

if (!BASE_URL) {
    throw new Error('BASE_URL environment variable is missing!');
}

export const options = {
    scenarios: {

        // ST-01: Gradual stress testing
        ST_01: {
            executor: 'ramping-vus',
            exec: 'homepageTest',
            startVUs: 1,
            stages: [
                { duration: '30s', target: 10 },
                { duration: '1m', target: 20 },
                { duration: '1m', target: 20 },
                { duration: '30s', target: 0 },
            ],
        },

        // ST-02: Spike stress testing
        ST_02: {
            executor: 'ramping-vus',
            exec: 'homepageTest',
            startVUs: 5,
            stages: [
                { duration: '30s', target: 5 },
                { duration: '1s', target: 50 },
                { duration: '1m', target: 50 },
                { duration: '1s', target: 5 },
                { duration: '30s', target: 0 },
            ],
        },

        // ST-03: Sustained stress testing
        ST_03: {
            executor: 'constant-vus',
            exec: 'homepageTest',
            vus: 30,
            duration: '3m',
        },

        // ST-04: Recovery testing
        ST_04: {
            executor: 'ramping-vus',
            exec: 'homepageTest',
            startVUs: 5,
            stages: [
                { duration: '30s', target: 20 },
                { duration: '1m', target: 20 },
                { duration: '30s', target: 0 },
            ],
        },
    },

    thresholds: {
        http_req_duration: ['p(95)<3000'],
        http_req_failed: ['rate<0.05'],
    },
};

// Shared homepage test function
export function homepageTest() {
    const response = http.get(`${BASE_URL}/`, {
        tags: { name: 'Homepage' },
    });

    check(response, {
        'Homepage status is 200': (r) => r.status === 200,
        'Response body is not empty': (r) =>
            r.body && r.body.length > 0,
    });

    sleep(1);
}
