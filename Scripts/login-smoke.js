
import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL;
const LOGIN_USERNAME = __ENV.LOGIN_USERNAME;
const LOGIN_PASSWORD = __ENV.LOGIN_PASSWORD;

if (!BASE_URL || !LOGIN_USERNAME || !LOGIN_PASSWORD) {
    throw new Error('Missing environment variables');
}

export const options = {
    vus: 1,
    iterations: 1,
};

export default function () {

    // Step 1: Establish a fresh session
    const homeResponse = http.get(`${BASE_URL}/`, {
        timeout: '30s',
    });

    const homepagePassed = check(homeResponse, {
        'Homepage returns 200': (r) => r.status === 200,
    });

    if (!homepagePassed || !homeResponse.body) {
        console.error(
            `Homepage request failed. Status: ${homeResponse.status}`
        );
        return;
    }

    // Step 2: Extract CSRF token from homepage
    const csrfMatch = homeResponse.body.match(
        /<meta\s+name=["']csrf-token["']\s+content=["']([^"']+)["']/i
    );

    if (!csrfMatch) {
        console.error('CSRF token not found in homepage');
        return;
    }

    const csrfToken = csrfMatch[1];
    console.log('CSRF token extracted successfully');

    // Step 3: Prepare login form
    const payload = {
        username: LOGIN_USERNAME,
        password: LOGIN_PASSWORD,
        web_login: '1',
    };

    // Step 4: Submit login request
    const loginResponse = http.post(
        `${BASE_URL}/login-with-email`,
        payload,
        {
            headers: {
                'Content-Type':
                    'application/x-www-form-urlencoded; charset=UTF-8',
                'X-CSRF-Token': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': BASE_URL,
                'Referer': `${BASE_URL}/`,
            },
            redirects: 0,
            tags: {
                name: 'Login API',
            },
            timeout: '30s',
        }
    );

    // Step 5: Log response details
    console.log(`Login HTTP Status: ${loginResponse.status}`);
    console.log(
        `Login Response Time: ${loginResponse.timings.duration} ms`
    );

    if (loginResponse.status === 200 && loginResponse.body) {
        console.log(
            `Login response body: ${loginResponse.body}`
        );
    } else {
        console.error('Login request did not return a valid response body');
    }

    // Step 6: Validate login response
    check(loginResponse, {
        'Login returned HTTP 200': (r) => r.status === 200,

        'Login response body is not empty': (r) =>
            !!r.body && r.body.length > 0,

        'Login response contains redirect instruction': (r) =>
            !!r.body &&
            /window\.location\.href\s*=\s*["']https:\/\/www\.pakwheels\.com\/["']/.test(r.body),
    });
}
