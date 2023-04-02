<template>
	<div class="home">
		<div class="w-full">
			<!-- Home Section -->

			<div class="bg-primary min-h-screen py-20">
				<div
					class="grid grid-cols-5 justify-between items-center max-w-7xl mt-10 m-auto"
				>
					<div class="col-span-2 pl-10">
						<div class="uppercase">
							Reach your
							<span class="font-semibold">Destinations</span>
						</div>
						<div class="text-8xl font-medium mt-10">
							LET'S
							<div
								class="inline-block bg-default text-primary rounded-full py-6 px-3 ml-2"
							>
								Go
							</div>
						</div>
						<div class="uppercase text-3xl font-light">
							Start At <span class="font-medium">₹5</span>
							<sup class="font-medium text-lg">/min</sup>
						</div>
						<button
							class="shadow-lg bg-white px-4 py-2 mt-20"
							@click="goTo('booking-section')"
						>
							Book Now
						</button>
					</div>
					<div class="col-span-3">
						<img class="w-full" src="hero-taxi.png" />
					</div>
				</div>
			</div>

			<!-- Booking Section -->

			<div
				id="booking-section"
				class="bg-grey min-h-screen flex items-center justify-center"
			>
				<div class="max-w-7xl bg-white shadow-lg w-full flex">
					<div class="p-6 w-2/5">
						<div class="text-3xl">
							<span class="font-bold">Book</span> A CAB
						</div>
						<div class="text-4xl leading-10 mt-4">
							Always the ride you want
						</div>
						<div class="mt-2 text-sm">
							Request a ride, hop in, and relax.
						</div>
						<div
							class="border-l-2 border-primary pl-4 text-sm py-1 italic mt-8"
						>
							Our standards help to create safe connections and
							positive interactions with everyone. Learn how our
							guidelines apply to you.
						</div>
					</div>
					<div class="py-12 px-16 w-3/5 bg-primary">
						<form
							class="w-full"
							@submit="bookCab"
							id="booking-form"
						>
							<div class="flex gap-8 mb-4">
								<div class="w-1/2">
									<!-- <label>Pick up location</label> -->
									<select
										@change="getTime()"
										name="type"
										id="type"
										class="block w-full py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
										v-model="formDetails.source"
										placeholder="Pick up location"
									>
										<option
											value=""
											disabled
											selected
											hidden
										>
											Source
										</option>
										<option
											:disabled="
												formDetails.destination === city
											"
											v-for="city in cities"
											v-bind:value="city"
										>
											{{ city }}
										</option>
									</select>
								</div>
								<div class="w-1/2">
									<select
										@change="getTime()"
										name="type"
										id="type"
										class="block w-full py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
										v-model="formDetails.destination"
									>
										<option
											value=""
											disabled
											selected
											hidden
										>
											Destination
										</option>
										<option
											:disabled="
												formDetails.source === city
											"
											v-for="city in cities"
											v-bind:value="city"
										>
											{{ city }}
										</option>
									</select>
								</div>
							</div>
							<div class="mb-4">
								<input
									placeholder="Email"
									class="block w-full py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
									v-model="formDetails.userEmail"
								/>
							</div>
							<div v-if="availableCabs" class="flex mt-4">
								<div
									@click="selectedCab = cab"
									v-for="cab in this.availableCabs"
									class="p-2"
									:class="
										selectedCab?.cabName === cab.cabName
											? 'bg-black text-white'
											: 'bg-white'
									"
								>
									<div class="text-base">
										{{ cab.cabName }}
									</div>
									<div class="font-bold text-2xl">
										₹{{ cab.pricePerMinute
										}}<sup class="text-sm font-normal"
											>/min</sup
										>
									</div>
									<div
										class="mt-2 text-sm"
										v-if="cab.tripPrice"
									>
										Trip Cost ₹{{ cab.tripPrice }}
									</div>
								</div>
							</div>
							<div v-else>
								<h1>No cab is available right now.</h1>
							</div>
							<h6 v-if="tripTime && availableCabs">
								Estimated Time : {{ tripTime }} minutes
							</h6>
							<button
								type="submit"
								class="shadow-lg bg-white px-4 py-2 mt-10"
							>
								Book Now
							</button>
							<button
								class="shadow-lg bg-black text-white px-4 py-2 mt-10 ml-4"
								@click="resetBookingForm"
							>
								Reset
							</button>
						</form>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import ApiUrl from '../config';
export default {
	name: 'HomeView',
	data() {
		return {
			formDetails: {
				userEmail: '',
				source: '',
				destination: '',
			},
			availableCabs: [],
			errorMessage: '',
			selectedCab: '',
			tripTime: '',
			cities: [],
		};
	},
	methods: {
		async getTime() {
			if (!this.formDetails.source || !this.formDetails.destination)
				return;

			try {
				let response = await fetch(`${ApiUrl}/get-time`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify(this.formDetails),
					redirect: 'follow',
				});

				let result = await response.json();
				if (response.ok) {
					this.tripTime = result.time;
					this.calculateTripPrice(result.time);
				} else if (response.status == 400) {
					this.errorMessage = result.message;
				}
			} catch (error) {
				this.errorMessage = 'Internal Server Error.';
			}
		},

		async bookCab(event) {
			event.preventDefault();
			if (!this.selectedCab) {
				this.errorMessage = 'Please select the cab you want to book.';
				return;
			}

			try {
				let response = await fetch(`${ApiUrl}/add-booking`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						cabId: this.selectedCab.cabId,
						tripTime: this.tripTime,
						...this.formDetails,
					}),
					redirect: 'follow',
				});

				if (response.ok) {
					alert('Booking Successful.');
					this.resetBookingForm();
				} else if (response.status == 400) {
					alert('You already have a cab booking.');
				}
			} catch (error) {
				this.errorMessage = 'Internal Server Error.';
			}
		},

		resetBookingForm() {
			this.formDetails.userEmail = '';
			this.formDetails.source = '';
			this.formDetails.destination = '';
			this.tripTime = '';

			this.getAvailableCabs();
		},

		goTo(refName) {
			document
				.getElementById(refName)
				.scrollIntoView({ behavior: 'smooth' });
		},

		calculateTripPrice(tripTime) {
			const updated = this.availableCabs.map((cab) => {
				cab.tripPrice = tripTime * cab.pricePerMinute;
				return cab;
			});
			this.availableCabs = [...updated];
		},

		async getCities() {
			let response = await fetch(`${ApiUrl}/get-cities`, {
				method: 'GET',
				headers: {
					'content-type': 'application/json',
				},
			});

			if (response.ok) {
				let result = await response.json();
				this.cities = result;
			} else {
				this.cities = null;
			}

			console.log(this.cities);
		},

		async getAvailableCabs() {
			let response = await fetch(`${ApiUrl}/available-cabs`, {
				method: 'GET',
				headers: {
					'content-type': 'application/json',
				},
			});

			if (response.ok) {
				let result = await response.json();
				this.availableCabs = result;
			} else {
				this.availableCabs = null;
			}
		},
	},

	async beforeMount() {
		await this.getCities();
		await this.getAvailableCabs();
	},
};
</script>

<style></style>
