
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL;

if (!BASE_URL) {
    throw new Error('BASE_URL environment variable is missing!');
}

export const options = {
    scenarios: {
        // Phase 1: Normal baseline traffic
        baseline: {
            executor: 'constant-vus',
            exec: 'baselineTest',
            vus: 1,
            duration: '1m',
            startTime: '0s',
            gracefulStop: '0s',
        },

        // Phase 2: Simulate high traffic
        high_load: {
            executor: 'constant-vus',
            exec: 'highLoadTest',
            vus: 20,
            duration: '1m',
            startTime: '1m',
            gracefulStop: '0s',
        },

        // Phase 3: Monitor recovery
        recovery: {
            executor: 'constant-vus',
            exec: 'recoveryTest',
            vus: 1,
            duration: '2m',
            startTime: '2m',
            gracefulStop: '0s',
        },
    },

    thresholds: {
        'http_req_duration{phase:recovery}': [
            'p(95)<2000',
        ],
        'http_req_failed{phase:recovery}': [
            'rate<0.01',
        ],
    },
};

function homepageTest(phase) {
    const response = http.get(`${BASE_URL}/`, {
        tags: {
            name: 'Homepage Recovery Test',
            phase: phase,
        },
    });

    check(response, {
        'Homepage status is 200': (r) => r.status === 200,
        'Response body is not empty': (r) =>
            r.body && r.body.length > 0,
    });

    sleep(1);
}

export function baselineTest() {
    homepageTest('baseline');
}

export function highLoadTest() {
    homepageTest('high_load');
}

export function recoveryTest() {
    homepageTest('recovery');
}
