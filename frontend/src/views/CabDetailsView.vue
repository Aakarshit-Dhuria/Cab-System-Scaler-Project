<template>
	<div class="text-center">
		<div class="shadow-md max-w-6xl mx-auto mt-8">
			<table class="w-full text-sm text-left">
				<thead class="text-xs bg-grey uppercase">
					<tr>
						<th scope="col" class="px-6 py-3">Cab Name</th>
						<th scope="col" class="px-6 py-3">Price Per Minute</th>
						<th scope="col" class="px-6 py-3">Availability</th>
						<th scope="col" class="px-6 py-3">Edit</th>
						<th scope="col" class="px-6 py-3">Delete</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="cab in cabsList" class="border-b">
						<td scope="row" class="px-6 py-4 font-medium">
							{{ cab.cabName }}
						</td>
						<td class="px-6 py-4">{{ cab.pricePerMinute }}</td>
						<td class="px-6 py-4">
							{{ cab.available === true ? 'Yes' : 'No' }}
						</td>
						<td class="px-6 py-4">
							<a
								href="#"
								class="font-medium underline"
								@click="
									storeCabDetails(cab);
									$modal.show('edit-modal');
								"
								>Edit</a
							>
						</td>
						<td class="px-6 py-4">
							<a
								href="#"
								class="font-medium underline"
								@click="deleteCab(cab.cabId)"
								>Delete</a
							>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<button
			class="px-4 py-2 shadow bg-primary text-white mx-auto mt-4"
			@click="$modal.show('add-modal')"
			type="button"
		>
			Add Cab
		</button>

		<t-modal ref="modal" name="add-modal">
			<div class="px-6 py-6 lg:px-8">
				<h3
					class="mb-4 text-xl font-medium text-gray-900 dark:text-white"
				>
					Add a new Cab
				</h3>
				<form class="space-y-6" @submit="addCab">
					<div>
						<input
							type="text"
							name="cabName"
							id="cabName"
							class="w-full rounded border border-gray-300 py-3 bg-gray-50 text-sm"
							placeholder="Enter Cab Name"
							v-model="formDetails.cabName"
							required
						/>
					</div>
					<div>
						<input
							type="number"
							name="pricePerMinute"
							id="pricePerMinute"
							placeholder="Enter Price per minute"
							class="w-full rounded border border-gray-300 py-3 bg-gray-50 text-sm"
							v-model="formDetails.pricePerMinute"
							required
						/>
					</div>
					<div class="flex justify-between">
						<button
							type="submit"
							class="bg-primary w-full text-white rounded py-2"
						>
							Add Cab
						</button>
					</div>
				</form>
			</div>
		</t-modal>

		<t-modal ref="editModal" name="edit-modal">
			<div class="px-6 py-6 lg:px-8">
				<h3
					class="mb-4 text-xl font-medium text-gray-900 dark:text-white"
				>
					Edit Cab
				</h3>
				<form class="space-y-6" @submit="editCab">
					<div>
						<input
							type="text"
							name="cabName"
							id="cabName"
							class="w-full rounded border border-gray-300 py-3 bg-gray-50 text-sm"
							placeholder="Enter Cab Name"
							v-model="formDetails.cabName"
							required
						/>
					</div>
					<div>
						<input
							type="number"
							name="pricePerMinute"
							id="pricePerMinute"
							placeholder="Enter Price per minute"
							class="w-full rounded border border-gray-300 py-3 bg-gray-50 text-sm"
							v-model="formDetails.pricePerMinute"
							required
						/>
					</div>
					<div class="flex justify-between">
						<button
							type="submit"
							class="bg-primary w-full text-white rounded py-2"
						>
							Edit Cab
						</button>
					</div>
				</form>
			</div>
		</t-modal>
		</div>
	</div>
</template>

<script>
import ApiUrl from '../config';

export default {
	name: 'CabDetailsView',
	data() {
		return {
			formDetails: {
				cabId: '',
				cabName: '',
				pricePerMinute: '',
			},

			cabsList: [],
		};
	},
	methods: {
		async getCabs() {
			await fetch(`${ApiUrl}/cabs`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
			})
				.then((response) => response.json())
				.then((data) => (this.cabsList = data));
		},
		async addCab(event) {
			event.preventDefault();

			let response = await fetch(`${ApiUrl}/cabs`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(this.formDetails),
			});

			if (response.ok) {
				alert('Cab added successfully.');
			}

			this.getCabs();
			this.formDetails.cabName = '';
			this.formDetails.pricePerMinute = '';
			this.$refs.modal.hide();
		},
		storeCabDetails(cab) {
			this.formDetails.cabId = cab.cabId;
			this.formDetails.cabName = cab.cabName;
			this.formDetails.pricePerMinute = cab.pricePerMinute;
		},
		async editCab(event) {
			event.preventDefault();
			let cabId = this.formDetails.cabId;
			console.log(cabId, this.formDetails);

			await fetch(`${ApiUrl}/cabs/${cabId}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(this.formDetails),
			})
				.then((response) => response.json())
				.then((response) => console.log(response));
			alert('Cab updated successfully');
			this.getCabs();
			this.$refs.editModal.hide();
		},
		async deleteCab(cabId) {
			await fetch(`${ApiUrl}/cabs/${cabId}`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
				},
			})
				.then((response) => response.json())
				.then((response) => console.log(response));
			alert('Cab deleted successfully');
			this.getCabs();
		},
	},
	beforeMount() {
		this.getCabs();
	},
};
</script>
