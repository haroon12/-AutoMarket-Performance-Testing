
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL;

if (!BASE_URL) {
    throw new Error('BASE_URL environment variable is missing!');
}

export const options = {
    scenarios: {
        BP_01: {
            executor: 'ramping-vus',
            startVUs: 10,
            stages: [
                { duration: '1m', target: 10 },
                { duration: '1m', target: 20 },
                { duration: '1m', target: 30 },
                { duration: '1m', target: 40 },
                { duration: '1m', target: 50 },
                { duration: '2m', target: 0 },
            ],
        },
    },

    thresholds: {
        http_req_duration: ['p(95)<2000'],
        http_req_failed: ['rate<0.01'],
    },
};

export default function () {
    const response = http.get(`${BASE_URL}/`, {
        tags: { name: 'Homepage Breakpoint Test' },
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
