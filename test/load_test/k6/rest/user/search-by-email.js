import {describe} from "https://jslib.k6.io/functional/0.0.3/index.js"
import {Httpx} from "https://jslib.k6.io/httpx/0.1.0/index.js"
import {check} from "k6"

const session = new Httpx({baseURL: __ENV.K6_TARGET_HOST, timeout: 20000})
session.addHeader("Content-Type", "application/json")

export const options = {
	thresholds: {
		checks: [{threshold: "rate == 1.00", abortOnFail: true}],
	},
	duration: "30s",
	vus: 30,
}

export default function testSuite() {
	const apiPath = "/rest/user/search-by-email"
	const payload = JSON.stringify({email: "pedro.perez@correo.com.co"})

	describe("search by email load test", () => {
		const response = session.get(apiPath, payload)
		check(response, {"is status 200": (response) => response.status === 200})
	})
}
