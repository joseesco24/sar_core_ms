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
	const apiPath = "/rest/collect-request/create"
	const payload = JSON.stringify({
		request: {
			collectDate: "12/12/2024",
			productionCenterId: 123456789,
		},
		waste: [
			{
				description: "nuclear wastes",
				note: "this is a note",
				packaging: 4,
				type: 1,
				volumeInL: 19,
				weightInKg: 18.2,
			},
			{
				description: "bone scan wastes",
				packaging: 4,
				type: 2,
				volumeInL: 18.4,
				weightInKg: 18.9,
			},
		],
	})

	describe("create new collect requests load test", () => {
		const response = session.post(apiPath, payload)
		check(response, {"is status 200": (response) => response.status === 200})
	})
}
