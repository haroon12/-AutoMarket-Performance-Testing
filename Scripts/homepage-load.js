
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL;

if (!BASE_URL) {
    throw new Error('BASE_URL environment variable is missing!');
}

export const options = {

    scenarios: {

        // LT-01: Gradual Load Testing
        LT_01: {
            executor: 'ramping-vus',
            exec: 'homepageTest',
            startVUs: 1,
            stages: [
                { duration: '30s', target: 2 },
                { duration: '1m', target: 5 },
                { duration: '2m', target: 10 },
                { duration: '30s', target: 0 },
            ],
        },

        // LT-02: Constant Load Testing
        LT_02: {
            executor: 'constant-vus',
            exec: 'homepageTest',
            vus: 10,
            duration: '3m',
        },

        // LT-03: Ramp-up Load Testing
        LT_03: {
            executor: 'ramping-vus',
            exec: 'homepageTest',
            startVUs: 1,
            stages: [
                { duration: '1m', target: 5 },
                { duration: '1m', target: 10 },
                { duration: '1m', target: 20 },
                { duration: '30s', target: 0 },
            ],
        },

        // LT-04: Peak Load Testing
        LT_04: {
            executor: 'constant-vus',
            exec: 'homepageTest',
            vus: 20,
            duration: '2m',
        },

        // LT-05: Low Load Testing
        LT_05: {
            executor: 'constant-vus',
            exec: 'homepageTest',
            vus: 2,
            duration: '1m',
        },

        // LT-06: Step Load Testing
        LT_06: {
            executor: 'ramping-vus',
            exec: 'homepageTest',
            startVUs: 1,
            stages: [
                { duration: '30s', target: 5 },
                { duration: '1m', target: 5 },
                { duration: '30s', target: 10 },
                { duration: '1m', target: 10 },
                { duration: '30s', target: 20 },
                { duration: '1m', target: 20 },
                { duration: '30s', target: 0 },
            ],
        },
    },

    thresholds: {
        http_req_duration: ['p(95)<2000'],
        http_req_failed: ['rate<0.01'],
    },
};

// Shared homepage test function
export function homepageTest() {

    const response = http.get(`${BASE_URL}/`, {
        tags: { name: 'Homepage Load Test' },
    });

    check(response, {
        'Homepage status is 200': (r) => r.status === 200,
        'Response time below 2 seconds': (r) =>
            r.timings.duration < 2000,
        'Response body is not empty': (r) =>
            r.body && r.body.length > 0,
    });

    sleep(1);
}
