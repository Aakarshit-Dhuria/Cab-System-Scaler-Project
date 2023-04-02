<template>
	<div id="app" class="w-full">
		<header
			class="h-20 bg-primary border-b border-grey flex items-stre ach px-10 justify-between top-0 w-full z-10"
		>
			<div class="mr-10 flex items-center">
				<router-link to="/home">
					<img class="w-20" src="logo.png" />
				</router-link>
			</div>

			<div>
				<nav class="h-full">
					<ul class="style-none h-full cursor-pointer flex">
						<router-link
							to="/home"
							active-class="bg-default text-primary"
							class="h-full px-4 flex items-center"
						>
							Home
						</router-link>
						<router-link
							to="/cabs"
							active-class="bg-default text-primary"
							class="h-full px-4 flex items-center"
						>
							Manage Cabs</router-link
						>
					</ul>
				</nav>
			</div>
		</header>
		<router-view />
	</div>
</template>

<style></style>

<script>
tailwind.config = {
	theme: {
		extend: {
			colors: {
				// primary: '#fbdb02',
				primary: '#f6cf16',
				default: '#000000',
				grey: '#f7f7f7',
			},
		},
	},
};
</script>
